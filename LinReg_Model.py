#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import statsmodels.api as sm
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import json
from sqlalchemy import create_engine

from get_clean_data_LinReg import get_data, clean_data, get_feats, get_target, partition_feats_by_ptp_cnt, partition_more_feats_by_ptp_cnt

import pickle

class OLS_Model(object):
    
    def __init__(self, train_year, partition_list):
        '''
        train_year          = int, year the model is trained on
        partition_list      = list of tuples on which the data is partitioned (currently by participant count)
        model_dict          = dictionary of models trained on each partition (keys = partition)
        prediction_dict     = dictionary of predictions from partition model for each plan within partition (keys = partition)
        '''
        self.train_year = train_year
        self.partition_list = partition_list
        self.prediction_dict = {}
        self.model_dict = {}

    def fit(self, cleaned_dictionary_of_df_split_by_size):
        '''
        Fit Ordinary Least Squares Linear Regression with training data
        '''
        for i in partition_list:
            X, y = cleaned_dictionary_of_df_split_by_size[i]
            self.model_dict[i] = sm.OLS(y, X, hasconst=False).fit()
    
    def predict(self, partitioned_data):
        '''
        Returns predicted Funding Target from partition model
        '''
        for i in self.partition_list:
            X, y = partitioned_data[i]
            self.prediction_dict[i] = self.model_dict[i].predict(X)
        return
    

if __name__ == '__main__':
    partition_list = [(0,300),(300,500),(500,800),(800,1500),(1500,2500),(2500,5000),(5000,10000),(10000,50000),(50000,100000),(100000,500000)]
    
    train_year = 2015
    print("Getting data for training year {}\n".format(train_year))
    training_data_dictionary = partition_feats_by_ptp_cnt(train_year)      

    print("Fitting model with {} data\n".format(train_year))
    model = OLS_Model(train_year, partition_list)     
    model.fit(training_data_dictionary)
    
    predict_year_list = [2016]
    
    engine = create_engine('postgresql://moserfamily:cats@localhost:5432/capstone')
    
    for year in predict_year_list:
        print("Getting data for prediction year {}\n".format(year))
        prediction_data_dictionary = partition_feats_by_ptp_cnt(year-1)
        full_data = partition_more_feats_by_ptp_cnt(year-1)
        print("Getting predictions for year {}\n".format(year))
        model.predict(prediction_data_dictionary)
        df = pd.DataFrame()
        combined = {}
        print("Combining data and predictions for year {}\n".format(year))
        for i in partition_list:
            combined[i] = pd.concat([full_data[i][0], pd.DataFrame(data=model.prediction_dict[i], columns=['predicted_fndng_tgt_{}'.format(year)]), full_data[i][1]], axis=1)
            df = pd.concat([df, combined[i]],axis=0)
        df.reset_index(drop=True)
        print("Writing to postgres database for year {}\n".format(year))
#        df.to_csv('combined_data_predictions_actual_{}'.format(year))

#        data_types = {'eir': float, 'fndng_tgt_{}'.format(year): int, 'tgt_nrml_cost_2016': int, 'pmts_to_part_2016': int, '}
        df.to_sql(name='predictions_{}_trained_{}'.format(year, train_year),con=engine,if_exists='replace')
        
    
    #with open('model.pkl', 'wb') as f:
        # Write the model to a file.
    #    pickle.dump(model, f)
    
    