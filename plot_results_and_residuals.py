#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
plt.rcParams.update({'font.size': 16})


def plot_results(y_true, y_pred, group_size, year, train_year):
    '''
    Produces a scatterplot of actual target vs. predicted target values
    Input:  True values and predicted values of target variable
    Output: Scatterplot
    
    '''
    plt.figure(figsize=(20,8))
    xx = np.linspace(0, len(y_true), len(y_true))
    plt.scatter(xx, y_true, label='Actual Funding Target')
    plt.scatter(xx, y_pred, label='Predicted Funding Target' )
    plt.xlabel("Plan number".format(year))
    plt.ylabel("{} Funding Target".format(year))
    plt.title("Predicting {} Funding Target from Linear Regression trained on {} data: Participant Count {}".format(year, train_year, group_size))
    plt.legend()
    plt.show()
    return

def plot_results_bars(y_true, y_pred, group_size, start, num, year, train_year):
    start = start
    num_to_plot = min(num, len(y_true))
    #y_true = df_15_full['fndng_tgt_2016'][0:num_to_plot-1]
    #y_pred = df_15_full['Predicted_FT_2016'][0:num_to_plot-1]
    y_true_plot = y_true[start:start+num_to_plot-1]
    y_pred_plot = y_pred[start:start+num_to_plot-1]
    xx = np.linspace(0,num_to_plot-1,num_to_plot-1)
    plt.figure(figsize=(20,8))
    plt.bar(xx, y_pred_plot, label='Predicted {} Funding Target'.format(year), width=.35 )
    plt.bar(xx+.35, y_true_plot, label='Actual {} Funding Target'.format(year), width=.35)
    #plt.scatter(y_true,y_pred, s=20, color=next(colors), label="data")
    plt.xlabel("plan")
    plt.ylabel("Funding Target")
    plt.title("Predicting {} Funding Target from Linear Regression trained on {} data, Participant Count: {}".format(year, train_year, group_size))
    plt.legend()
    plt.show()
    return

def plot_results_bars_compare(y_true, y_pred, y_pred_w, group_size, start, num, year, train_year):
    start = start
    num_to_plot = min(num, len(y_true))
    #y_true = df_15_full['fndng_tgt_2016'][0:num_to_plot-1]
    #y_pred = df_15_full['Predicted_FT_2016'][0:num_to_plot-1]
    y_true_plot = y_true[start:start+num_to_plot-1]
    y_pred_plot = y_pred[start:start+num_to_plot-1]
    y_pred_plot_w = y_pred_w[start:start+num_to_plot-1]
    xx = np.linspace(0,num_to_plot-1,num_to_plot-1)
    plt.figure(figsize=(20,8))
    plt.bar(xx, y_pred_plot, label='Predicted {} Funding Target'.format(year), width=.25 )
    plt.bar(xx+.33, y_pred_plot_w, label='Predicted {} Funding Target'.format(year), width=.25 )   
    plt.bar(xx+.66, y_true_plot, label='Actual {} Funding Target'.format(year), width=.25)
    plt.xlabel("plan")
    plt.ylabel("Funding Target")
    plt.title("Predicting {} Funding Target from Linear Regression trained on {} data, Participant Count: {}".format(year, train_year, group_size))
    plt.legend()
    plt.show()
    return

def plot_residuals(y_true, y_pred, group_size, year, train_year):
    '''
    Produces a scatterplot of residuals (difference of true value over predicted value)
    Input:  True values and predicted values of target variable
    Output: Scatterplot of residuals    
    
    '''    
    resid = y_true - y_pred

    plt.figure(figsize=(20,8))
    xx = np.linspace(0, len(y_true), num=len(y_true))
    plt.scatter(xx, resid, s=20, label="residuals")
    plt.xlabel("plan")
    plt.ylabel("residual")
    plt.title("Residuals of {} Predictions vs Actuals (trained on {} data): Participant Count {}".format(year, train_year, group_size))
    plt.legend()
    plt.show()
    return

def plot_student_residuals(student_resids, group_size, year, train_year):
    '''
    Produces a scatterplot of residuals (difference of true value over predicted value)
    Input:  True values and predicted values of target variable
    Output: Scatterplot of residuals    
    
    '''    
    plt.figure(figsize=(20,8))
    xx = np.linspace(0, len(student_resids), num=len(student_resids))
    plt.scatter(xx, student_resids, s=20, label="residuals")
    plt.xlabel("plan")
    plt.ylabel("residual")
    plt.title("Studentized Residuals of {} Predictions vs Actuals (trained on {} data): Participant Count {}".format(year, train_year, group_size))
    plt.legend()
    plt.show()
    return