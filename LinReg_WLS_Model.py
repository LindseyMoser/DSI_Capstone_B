#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import statsmodels.api as sm
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import json
from sqlalchemy import create_engine

from get_clean_data_LinReg import get_data, clean_data, get_feats, get_target, partition_feats_by_ptp_cnt, partition_more_feats_by_ptp_cnt

class WLS_Model(object):
    
    '''
    Weighted Least Squares Linear Regression model
    Trained on 20XX data, gets predictions for 20XX+1 funding target
    
    '''
    
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
        Fit Weighted Least Squares Linear Regression with training data
        '''
        for i in partition_list:
            X, y = cleaned_dictionary_of_df_split_by_size[i]
            self.model_dict[i] = sm.WLS(y, X, hasconst=False).fit()
    
    def predict(self, partitioned_data):
        '''
        Returns predicted Funding Target from partition model
        '''
        for i in self.partition_list:
            X, y = partitioned_data[i]
            self.prediction_dict[i] = self.model_dict[i].predict(X)
        return
    

if __name__ == '__main__':
    
    '''
    Partition data in train_year based on partition_list (currently partitioning on plan participant count)
    Train Weighted Least Squares model on train_year data to predict subsequent year funding target
        (e.g. model trained on 2015 data will predict 2016 funding target)
    Make predictions of funding target for years in predict_year_list
    Store predictions, features and other data into postgres database
    '''
    
    partition_list = [(0,300),(300,500),(500,800),(800,1500),(1500,2500),(2500,5000),(5000,10000),(10000,50000),(50000,100000),(100000,500000)]
    
    train_year = 2012
    print("Getting data for training year {}\n".format(train_year))
    training_data_dictionary = partition_feats_by_ptp_cnt(train_year)      

    print("Fitting model with {} data\n".format(train_year))
    model = WLS_Model(train_year, partition_list)     
    model.fit(training_data_dictionary)
    
    predict_year_list = [2013, 2014]
    
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
            combined[i] = pd.concat([full_data[i][0], \
                                    pd.DataFrame(data=model.prediction_dict[i], columns=['predicted_fndng_tgt_{}'.format(year)]), \
                                    full_data[i][1]], axis=1)
            combined[i]['partition'] = str(i)
            df = pd.concat([df, combined[i]],axis=0)
        df.reset_index(drop=True)
        
        print("Writing to postgres database for year {}\n".format(year))
        df.to_sql(name='predictions_{}_trained_{}_wls'.format(year, train_year),con=engine,if_exists='replace')
    print("Program complete!")
        
    