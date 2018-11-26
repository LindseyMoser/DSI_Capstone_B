#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn.tree import DecisionTreeRegressor

from get_clean_data_DTR import get_data, clean_data, get_feats
from sklearn.ensemble import GradientBoostingClassifier
import pickle

class DTR(object):
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.columns = None
    
    def get_data(self):      
        '''
        Create dataframe from raw json file
        Create features set X
        Create targets set y
        '''
        raw_df = create_df(self.data_path)
        df = clean_data(raw_df, False)
        X = create_features_df(df)
        self.columns = X.columns
        y = df['fraud'].values
        return X, y
            
    def fit(self, X_train, y_train):
        '''
        Fit Gradient Boosted Classifier with training data
        '''
        self.model = GradientBoostingClassifier(n_estimators=500, max_depth=8, subsample=0.5, 
                                                    max_features='auto', learning_rate=0.05)
        self.model.fit(X_train, y_train)
     
    def predict_proba(self, X_test):
        '''
        Returns predicted probabilities for not fraud / fraud
        '''
        return self.model.predict_proba(X_test)[:,1]
    
    def predict(self, X_test):
        '''
        Returns predicted class ( 0= not fraud / 1 = fraud)
        '''
        return self.model.predict(X_test)
    

if __name__ == '__main__':
    data_path = "../data/data.json"
    model = FraudModel(data_path)
    X, y = model.get_data()
    model.fit(X, y)
    
    with open('model.pkl', 'wb') as f:
        # Write the model to a file.
        pickle.dump(model, f)
    
    