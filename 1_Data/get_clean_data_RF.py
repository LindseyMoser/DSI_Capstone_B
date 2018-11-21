#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 15:23:05 2018

@author: moserfamily
"""
import pandas as pd
import numpy as np
import psycopg2
import json

def get_data():
    
    '''
    Executes SQL query to retrieve data
    Input:  None
    Output: Pandas DF
    
    '''
    with open('form5500_data/config.json') as f:
        conf = json.load(f)
        host = conf['host']
        database = conf['database']
        user = conf['user']
        passw = conf['passw']
    conn_str = "host={} dbname={} user={} password={}".format(host, database, user, passw)
    conn = psycopg2.connect(conn_str)
    
    query = '''SELECT sb.SB_FNDNG_SHORT_IND, 
       sb.SB_PR_YR_FNDNG_PRCNT, sb.SB_PLAN_TYPE_CODE, 
       f.BUSINESS_CODE, sb.SB_FNDNG_TGT_PRCNT 
       FROM sb_full sb 
       LEFT JOIN f5500_full f 
       ON sb.SB_EIN = f.SPONS_DFE_EIN AND sb.SB_PN = f.SPONS_DFE_PN 
       WHERE sb.SB_PLAN_YEAR_BEGIN_DATE BETWEEN '2017-01-01' AND '2017-12-31';'''
    
    df = pd.read_sql(query, con=conn)
    conn.close()
    return df

def clean_data(df, train=False):
    
    '''
    Cleans data for model
    Input:  Pandas DF, train=True if model is being trained
    Output: cleaned Pandas DF, target array y if model is being trained
    
    '''
    #This is all the data "cleaning" for now...will revisit after further EDA
    df_clean = df.copy()

    #Create buckets for funded status - apply to current year and prior year
    buckets = pd.IntervalIndex.from_tuples([(-100, 60), (60, 80), (80, 90), (90, 100), (100, 999.)])
    
    df_clean['py_ft_bucket'] = pd.cut(df_clean['sb_pr_yr_fndng_prcnt'], buckets)
    df_clean['ft_bucket'] = pd.cut(df_clean['sb_fndng_tgt_prcnt'], buckets)
    
    df_clean = pd.get_dummies(data=df_clean, columns=['py_ft_bucket'], drop_first=True)
    
    #create new column for sector and make dummies    
    df_clean['sector'] = df_clean['business_code'].str[:2]
    df_clean = pd.concat([df_clean, pd.get_dummies(df_clean['sector'].values, prefix_sep='sect_', drop_first=True)],axis=1)

    
    #drop un-needed columns
    drop_list=['business_code', 'sector', 'sb_pr_yr_fndng_prcnt', 'sb_fndng_tgt_prcnt']    
    #drop_list=['business_code', 'sector']
    df_clean.drop(drop_list, inplace=True, axis=1)
 
    df_clean.dropna(inplace=True)
       
    if train:
        y = df_clean['ft_bucket'].values
        df_clean.drop('ft_bucket', inplace=True, axis=1)
        return df_clean, y
    else:
        return df_clean