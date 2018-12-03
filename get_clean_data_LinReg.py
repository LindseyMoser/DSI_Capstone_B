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
    with open('1_Data/form5500_data/config.json') as f:
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
                sb2.SB_EFF_INT_RATE_PRCNT AS EIR_{1},
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
    Cleans data for model:
            - Cast Participant Count to number
            - Divide Effective Interest Rate by 100 if greater than 100 (correction for observed data entry variation)
            - Add boolean columns to indicate if plan is pay related, cash balance, frozen, taken over by PBGC, not qualified
            - Drop filings with $0 funding target and filings of non-qualified plans
            - Drop nas
            - Drop largest plan
            
    Input:  Pandas DF, year 
    Output: cleaned Pandas DF, target array y if model is being trained
    
    '''
     #drop duplicates
    df_clean = df.drop_duplicates()
    
    clean_list = ['part_cnt_{}'.format(year), 'part_cnt_{}'.format(year+1)]
    for col in clean_list:
        df_clean[col] = pd.to_numeric(df_clean[col])

    df_clean['eir'] = np.where(df_clean['eir']>100, df_clean['eir']/100**2, df_clean['eir']/100)   
    df_clean['eir_{}'.format(year+1)] = np.where(df_clean['eir_{}'.format(year+1)]>100, df_clean['eir_{}'.format(year+1)]/100**2, df_clean['eir_{}'.format(year+1)]/100)
    
    #Pension Benefit Code gives informaiton on types of benefits provided by plan
    
    df_clean['pay_related'] = df_clean['type_pension_bnft_code'].str.contains('1A')
    df_clean['cash_bal'] = df_clean['type_pension_bnft_code'].str.contains('1C')
    df_clean['frozen'] = df_clean['type_pension_bnft_code'].str.contains('1I')
    df_clean['pbgc_takeover'] = df_clean['type_pension_bnft_code'].str.contains('1H')
    df_clean['not_qual'] = df_clean['type_pension_bnft_code'].str.contains('3B','3C')
    
     
    df_clean = df_clean[(df_clean['fndng_tgt_{}'.format(year)] > 0) & (df_clean['fndng_tgt_{}'.format(year+1)] > 0) &\
              (df_clean['not_qual'] == False)]
    
    df_clean.dropna(inplace=True)
    
    #drop largest plan by ptp cnt
    df_clean = df_clean.loc[df_clean['part_cnt_{}'.format(year)] != df_clean['part_cnt_{}'.format(year)].max()]
    
    #add length of pension_bft_code field to determine duplicates
    df_clean['bnft_code_length'] = df_clean['type_pension_bnft_code'].str.len()
    df_clean_no_dupes = df_clean.sort_values('bnft_code_length', ascending=False).groupby(['ein', 'pn']).head(1)
    
    return df_clean_no_dupes

def get_feats(df, year):
    
    '''
    Returns features dataframe for model
    Input:  Pandas DF of cleaned data
    Output: Pandas DF of features only
    
    '''
    feat_list = ['eir', 'part_cnt_{}'.format(year), 'fndng_tgt_{}'.format(year), 'tgt_nrml_cost_{}'.format(year),'pmts_to_part_{}'.format(year)]
    X = df[feat_list].copy()
    X['eir_ft'] = (1 + X['eir']) * X['fndng_tgt_{}'.format(year)]
    X['eir_tnc'] = (1 + X['eir']) * X['tgt_nrml_cost_{}'.format(year)]
    X['eir_pmt'] = (1 + X['eir']/2) * X['pmts_to_part_{}'.format(year)]
    
    #prelim OLS results indicate not important features:
    X.drop(['eir','fndng_tgt_{}'.format(year), 'tgt_nrml_cost_{}'.format(year),'pmts_to_part_{}'.format(year)], axis=1, inplace=True)
    
    return X

def get_more_feats(df, year):
    
    '''
    Returns features dataframe for model
    Input:  Pandas DF of cleaned data
    Output: Pandas DF of features with plan name, sponsor name, ein, pn, pension benefit code
    
    '''
    feat_list = ['eir', 'part_cnt_{}'.format(year), 'fndng_tgt_{}'.format(year), 'tgt_nrml_cost_{}'.format(year),'pmts_to_part_{}'.format(year)]

    more_feats = ['ein', 'pn', 'plan_name', 'sponsor_dfe_name', 'type_pension_bnft_code', 'eir_{}'.format(year+1)]
    
    feat_list += more_feats
    
    X = df[feat_list].copy()
    X['eir_ft'] = (1 + X['eir']) * X['fndng_tgt_{}'.format(year)]
    X['eir_tnc'] = (1 + X['eir']) * X['tgt_nrml_cost_{}'.format(year)]
    X['eir_pmt'] = (1 + X['eir']/2) * X['pmts_to_part_{}'.format(year)]
    X['diff_eir'] = X['eir_{}'.format(year+1)] - X['eir']
        
    return X

def get_target(df, year):
    
    '''
    Returns target for training model
    Input:  Pandas DF
    Output: Target only
    
    '''
    target = df['fndng_tgt_{}'.format(year+1)]
    
    return target

def partition_feats_by_ptp_cnt(year):
    
    #partition_list = [0,50,300,500,800,1500,2500,5000,10000,50000,100000,500000]
    partition_list = [(0,300),(300,500),(500,800),(800,1500),(1500,2500),(2500,5000),(5000,10000),(10000,50000),(50000,100000),(100000,500000)]
    part_dict = {}
    
    prelim_df = get_data(year)
    df = clean_data(prelim_df, year)
    df.reset_index(drop=True, inplace=True)
    
    X = get_feats(df, year)
    y = get_target(df, year)
    
    for i in partition_list[0:len(partition_list)]:
        min_count = i[0]
        max_count = i[1]
        X_part = X[(X['part_cnt_{}'.format(year)] > min_count) & (X['part_cnt_{}'.format(year)] <= max_count)].reset_index(drop=True)
        y_part = y[(X['part_cnt_{}'.format(year)] > min_count) & (X['part_cnt_{}'.format(year)] <= max_count)].reset_index(drop=True)
        #part_dict["part_cnt" + str(i)] = (X_part,y_part)
        #X_part.reset_index(drop=True)
        #y_part.reset_index(drop=True)
        X_part.drop('part_cnt_{}'.format(year), axis=1, inplace=True)
        part_dict[i] = (X_part,y_part)
        
    return part_dict
    
def partition_more_feats_by_ptp_cnt(year):
    
    #partition_list = [0,50,300,500,800,1500,2500,5000,10000,50000,100000,500000]
    partition_list = [(0,300),(300,500),(500,800),(800,1500),(1500,2500),(2500,5000),(5000,10000),(10000,50000),(50000,100000),(100000,500000)]
    part_dict = {}
    
    prelim_df = get_data(year)
    df = clean_data(prelim_df, year)
    df.reset_index(drop=True, inplace=True)
    
    X = get_more_feats(df, year)
    y = get_target(df, year)
    
    for i in partition_list[0:len(partition_list)]:
        min_count = i[0]
        max_count = i[1]
        X_part = X[(X['part_cnt_{}'.format(year)] > min_count) & (X['part_cnt_{}'.format(year)] <= max_count)].reset_index(drop=True)
        y_part = y[(X['part_cnt_{}'.format(year)] > min_count) & (X['part_cnt_{}'.format(year)] <= max_count)].reset_index(drop=True)
        #part_dict["part_cnt" + str(i)] = (X_part,y_part)
        #X_part.drop('part_cnt_{}'.format(year), axis=1, inplace=True)
        #X_part.reset_index(drop=True)
        #y_part.reset_index(drop=True)
        part_dict[i] = (X_part,y_part)
        
    return part_dict
