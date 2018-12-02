#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import statsmodels.api as sm
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import json
import psycopg2

from get_clean_data_LinReg import get_data, clean_data, get_feats, get_target, partition_feats_by_ptp_cnt, partition_more_feats_by_ptp_cnt

import pickle

class OLS_Model(object):
    
    def __init__(self, train_year, partition_list):
        self.train_year = train_year
        self.partition_list = partition_list
        self.prediction_dict = {}
        self.model_dict = {}

    def fit(self, cleaned_dictionary_of_df_split_by_size):
        '''
        Fit Decision Tree Regressor with training data
        '''
        for i in partition_list:
            X, y = cleaned_dictionary_of_df_split_by_size[i]
            self.model_dict[i] = sm.OLS(y, X, hasconst=False).fit()
    
    def predict(self, partitioned_data):
        '''
        Returns predicted Funding Target
        '''
        for i in self.partition_list:
            X, y = partitioned_data[i]
            self.prediction_dict[i] = self.model_dict[i].predict(X)
        return
    

if __name__ == '__main__':
    partition_list = [(0,300),(300,500),(500,800),(800,1500),(1500,2500),(2500,5000),(5000,10000),(10000,50000),(50000,100000),(100000,500000)]
    
    train_year = 2013
    print("Getting data for training year {}\n".format(train_year))
    training_data_dictionary = partition_feats_by_ptp_cnt(train_year)      

    print("Fitting model with {} data\n".format(train_year))
    model = OLS_Model(train_year, partition_list)     
    model.fit(training_data_dictionary)
    
    predict_year_list = [2015,2016]
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
            combined[i] = pd.concat([full_data[i][0], pd.DataFrame(model.prediction_dict[i]).rename(columns={0:'predicted_fndng_tgt_'.format(year)})], axis=1, join='inner')
            #combined[i] = pd.concat([combined[i], full_data[i][1]], axis=1, join='inner')
            df.append(combined[i])
        print("Writing to csv for year {}\n".format(year))
        df.to_csv('combined_data_predictions_actual_{}'.format(year))
#        with open('1_Data/form5500_data/config.json') as f:
#            conf = json.load(f)
#            host = conf['host']
#            database = conf['database']
#            user = conf['user']
#            passw = conf['passw']
#        conn_str = "host={} dbname={} user={} password={}".format(host, database, user, passw)
#        conn = psycopg2.connect(conn_str)
#
#        df.to_sql('combined_data_predictions_actual_{}'.format(year),con=conn)
#        
#        conn.close()
    
    #with open('model.pkl', 'wb') as f:
        # Write the model to a file.
    #    pickle.dump(model, f)
    
    