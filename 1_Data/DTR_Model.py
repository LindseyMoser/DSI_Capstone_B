#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn.tree import DecisionTreeRegressor

from get_clean_data_DTR import get_data, clean_data, get_feats, get_target

import pickle

class DTR(object):
    
    def __init__(self, predict_year):
        self.predict_year = predict_year
    
    def fit(self, X, y):
        '''
        Fit Decision Tree Regressor with training data
        '''
        self.model = DecisionTreeRegressor(max_depth=4)
        self.model.fit(X, y)
         
    def predict(self, X):
        '''
        Returns predicted Funding Target
        '''
        return self.model.predict(X)
    

if __name__ == '__main__':
    predict_year = 2015
    data_year = predict_year-1
    raw_df = get_data(data_year)
    df = clean_data(raw_df, data_year)
    X = get_feats(df, data_year)
    y = get_target(df, data_year)
    
    model = DTR(predict_year)

    model.fit(X, y)
    
    with open('model.pkl', 'wb') as f:
        # Write the model to a file.
        pickle.dump(model, f)
    
    