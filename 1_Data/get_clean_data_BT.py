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

def get_data(year):
    
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
    
    query = '''SELECT sb.SB_EIN AS EIN, 
                sb.SB_PN AS PN, 
                sb.SB_EFF_INT_RATE_PRCNT AS EIR, 
                sb.SB_PLAN_TYPE_CODE,
                sb.SB_TOT_PARTCP_CNT AS PART_CNT_PY, 
                sb.SB_TOT_FNDNG_TGT_AMT AS FNDNG_TGT_PY, 
                sb.SB_TGT_NRML_COST_01_AMT AS TGT_NRML_COST_PY, 
                sb2.SB_TOT_FNDNG_TGT_AMT AS FNDNG_TGT_CY,
                sb2.SB_TOT_PARTCP_CNT AS PART_CNT_CY, 
                f.TYPE_PENSION_BNFT_CODE, 
                f.PLAN_NAME, 
                f.SPONSOR_DFE_NAME,
                h.DISTRIB_DRT_PARTCP_AMT AS PMTS_TO_PART, 
                h.TOT_DISTRIB_BNFT_AMT AS TOT_PMTS
                FROM sb_full sb
                LEFT JOIN sb_full sb2
                ON sb.SB_EIN = sb2.SB_EIN AND sb.SB_PN = sb2.SB_PN
                LEFT JOIN f5500_full f
                ON sb.SB_EIN = f.SPONS_DFE_EIN AND sb.SB_PN = f.SPONS_DFE_PN
                LEFT JOIN h_full h
                ON sb.SB_EIN = h.SCH_H_EIN AND sb.SB_PN = h.SCH_H_PN
                WHERE sb.SB_PLAN_TYPE_CODE = '1'
                AND sb.SB_PLAN_YEAR_BEGIN_DATE = '2016-01-01'
                AND sb2.SB_PLAN_YEAR_BEGIN_DATE = '2017-01-01'
                AND h.SCH_H_PLAN_YEAR_BEGIN_DATE = '2016-01-01';
                '''

    df = pd.read_sql(query, con=conn)
    conn.close()
    df['data_year'] = year
    return df
    
def clean_data(df):
    
    '''
    Cleans data for model
    Input:  Pandas DF, train=True if model is being trained
    Output: cleaned Pandas DF, target array y if model is being trained
    
    '''
    df_clean = df.copy()
    
    clean_list = ['part_cnt_PY', 'part_cnt_CY']
    for col in clean_list:
        df_clean[col] = pd.to_numeric(df_clean[col])

    df_clean['eir'] = np.where(df_clean['eir']>100, df_clean['eir']/100, df_clean['eir'])   
        
    df_clean['pay_related'] = df_clean['type_pension_bnft_code'].str.contains('1A')
    df_clean['cash_bal'] = df_clean['type_pension_bnft_code'].str.contains('1C')
    df_clean['frozen'] = df_clean['type_pension_bnft_code'].str.contains('1I')
    df_clean['pbgc_takeover'] = df_clean['type_pension_bnft_code'].str.contains('1H')
    df_clean['not_qual'] = df_clean['type_pension_bnft_code'].str.contains('3B','3C')
    
    df_clean = df_clean[(df_clean['fndng_tgt_py'] > 0) & (df_clean['fndng_tgt_cy'] > 0) &\
              (df_clean['part_cnt_cy'] < 300000) & (df_clean['part_cnt_cy'] > 100) & \
              (df_clean['not_qual'] == False)]
    
    df_clean.dropna(inplace=True)
       
    return df_clean

def get_feats(df):
    
    '''
    Returns features dataframe for model
    Input:  Pandas DF
    Output: Features only
    
    '''
    df_feat = df.copy()
    
    #drop un-needed columns
    drop_list=['business_code', 'sector', 'sb_pr_yr_fndng_prcnt']    
    #drop_list=['business_code', 'sector']
    df_feat.drop(drop_list, inplace=True, axis=1)
 
