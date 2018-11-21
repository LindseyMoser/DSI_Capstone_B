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
    
    query = "SELECT sb.SB_EIN, sb.SB_PN, sb.SB_TOT_PARTCP_CNT, sb.SB_EFF_INT_RATE_PRCNT, sb.SB_FNDNG_SHORT_IND, \
       sb.SB_PR_YR_FNDNG_PRCNT, sb.SB_PLAN_TYPE_CODE, \
       f.BUSINESS_CODE, f.SCH_SB_ATTACHED_IND, sb.SB_FNDNG_TGT_PRCNT \
       FROM sb_full sb \
       LEFT JOIN f5500_full f \
       ON sb.SB_EIN = f.SPONS_DFE_EIN AND sb.SB_PN = f.SPONS_DFE_PN \
       WHERE sb.SB_PLAN_YEAR_BEGIN_DATE BETWEEN '2017-01-01' AND '2017-12-31';"
    
    return pd.read_sql(query, con=conn)

def clean_data(df, train=False):
    
    '''
    Cleans data for model
    Input:  Pandas DF, train=True if model is being trained
    Output: cleaned Pandas DF, target array y if model is being trained
    
    '''
    #This is all the data "cleaning" for now...will revisit after further EDA
       
    df_clean = df.dropna().copy()
    
    #convert string values to integers where appropriate
    df_clean['sb_tot_partcp_cnt'] = pd.to_numeric(df_clean['sb_tot_partcp_cnt'])
    df_clean['sb_fndng_short_ind'] = pd.to_numeric(df_clean['sb_fndng_short_ind'])
    
    #create new column for sector and make dummies
    df_clean['sector'] = pd.to_numeric(df_clean['business_code'].str[:2])
    df_clean = pd.concat([df_clean, pd.get_dummies(df_clean['sector'].values, prefix_sep='_')],axis=1)
    
    #drop un-needed columns
    df_clean.drop('sch_sb_attached_ind', inplace=True, axis=1)
    df_clean.drop('sb_ein', inplace=True, axis=1)
    df_clean.drop('sb_pn', inplace=True, axis=1)
    df_clean.drop('business_code', inplace=True, axis=1)
    df_clean.drop('sb_plan_type_code', inplace=True, axis=1)
    df_clean.drop('sector', inplace=True, axis=1)
    
    
    if train:
        y = df_clean['sb_fndng_tgt_prcnt'].values
        df_clean.drop('sb_fndng_tgt_prcnt', inplace=True, axis=1)
        return df_clean, y
    else:
        return df_clean