#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
                sb.SB_TOT_PARTCP_CNT AS PART_CNT_{0}, 
                sb.SB_TOT_FNDNG_TGT_AMT AS FNDNG_TGT_{0}, 
                sb.SB_TGT_NRML_COST_01_AMT AS TGT_NRML_COST_{0}, 
                sb2.SB_TOT_FNDNG_TGT_AMT AS FNDNG_TGT_{1},
                sb2.SB_TOT_PARTCP_CNT AS PART_CNT_{1}, 
                f.TYPE_PENSION_BNFT_CODE, 
                f.PLAN_NAME, 
                f.SPONSOR_DFE_NAME,
                h.DISTRIB_DRT_PARTCP_AMT AS PMTS_TO_PART_{0}, 
                h.TOT_DISTRIB_BNFT_AMT AS TOT_PMTS_{0}
                FROM sb_full sb
                LEFT JOIN sb_full sb2
                ON sb.SB_EIN = sb2.SB_EIN AND sb.SB_PN = sb2.SB_PN
                LEFT JOIN f5500_full f
                ON sb.SB_EIN = f.SPONS_DFE_EIN AND sb.SB_PN = f.SPONS_DFE_PN
                LEFT JOIN h_full h
                ON sb.SB_EIN = h.SCH_H_EIN AND sb.SB_PN = h.SCH_H_PN
                WHERE sb.SB_PLAN_TYPE_CODE = '1'
                AND sb.SB_PLAN_YEAR_BEGIN_DATE = '{0}-01-01'
                AND sb2.SB_PLAN_YEAR_BEGIN_DATE = '{1}-01-01'
                AND h.SCH_H_PLAN_YEAR_BEGIN_DATE = '{0}-01-01';
                '''.format(year, year+1)

    df = pd.read_sql(query, con=conn)
    conn.close()
    df['data_year'] = year
    return df
    
def clean_data(df, year):
    
    '''
    Cleans data for model
    Input:  Pandas DF, train=True if model is being trained
    Output: cleaned Pandas DF, target array y if model is being trained
    
    '''
    df_clean = df.copy()
    
    clean_list = ['part_cnt_{}'.format(year), 'part_cnt_{}'.format(year+1)]
    for col in clean_list:
        df_clean[col] = pd.to_numeric(df_clean[col])

    df_clean['eir'] = np.where(df_clean['eir']>100, df_clean['eir']/100, df_clean['eir'])   
    
    #Pension Benefit Code gives informaiton on types of benefits provided by plan
    
    df_clean['pay_related'] = df_clean['type_pension_bnft_code'].str.contains('1A')
    df_clean['cash_bal'] = df_clean['type_pension_bnft_code'].str.contains('1C')
    df_clean['frozen'] = df_clean['type_pension_bnft_code'].str.contains('1I')
    df_clean['pbgc_takeover'] = df_clean['type_pension_bnft_code'].str.contains('1H')
    df_clean['not_qual'] = df_clean['type_pension_bnft_code'].str.contains('3B','3C')
    
     # Restrict analysis to plans with between 100 and 300,000 participants
     
    df_clean = df_clean[(df_clean['fndng_tgt_{}'.format(year)] > 0) & (df_clean['fndng_tgt_{}'.format(year+1)] > 0) &\
              (df_clean['part_cnt_{}'.format(year)] < 300000) & (df_clean['part_cnt_{}'.format(year)] > 100) & \
              (df_clean['not_qual'] == False)]
    
    df_clean.dropna(inplace=True)
       
    return df_clean

def get_feats(df, year):
    
    '''
    Returns features dataframe for model
    Input:  Pandas DF
    Output: Features only
    
    '''
    feat_list = ['eir', 'part_cnt_{}'.format(year), 'fndng_tgt_{}'.format(year), 'tgt_nrml_cost_{}'.format(year),'pmts_to_part_{}'.format(year)]
    df_feat = df[feat_list]
    
    return df_feat

def get_target(df, year):
    
    '''
    Returns target for training model
    Input:  Pandas DF
    Output: Target only
    
    '''
    target = df['fndng_tgt_{}'.format(year+1)]
    
    return target
       
    
