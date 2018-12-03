#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
plt.rcParams.update({'font.size': 16})

colors = itertools.cycle(["c", "m", "y"])

def plot_results(y_true, y_pred, group_size, pred_year, train_year):
    '''
    Produces a scatterplot of actual target vs. predicted target values
    Input:  True values and predicted values of target variable
    Output: Scatterplot
    
    '''
    plt.figure(figsize=(20,8))
    xx = np.linspace(0, len(y_true), len(y_true))
    plt.scatter(xx, y_true, color='cyan', label='Actual Funding Target')
    plt.scatter(xx, y_pred, color='magenta', label='Predicted Funding Target' )
    plt.xlabel("Plan number")
    plt.ylabel("{} Funding Target".format(pred_year))
    plt.title("Predicting {} Funding Target from Linear Regression trained on {} data: Participant Count {}".format(pred_year, train_year, group_size))
    plt.legend()
    plt.show()
    return

def plot_residuals(y_true, y_pred, group_size, pred_year, train_year):
    '''
    Produces a scatterplot of residuals (difference of true value over predicted value)
    Input:  True values and predicted values of target variable
    Output: Scatterplot of residuals    
    
    '''    
    resid = y_true - y_pred

    plt.figure(figsize=(20,8))
    xx = np.linspace(0, len(y_true), num=len(y_true))
    plt.scatter(xx, resid, s=20, c="blue", label="residuals")
    plt.xlabel("data")
    plt.ylabel("residual")
    plt.title("Residuals of {} Predictions vs Actuals (train year {}): Participant Count: {}".format(pred_year, train_year, group_size))
    plt.legend()
    plt.show()
    return

def plot_residuals_2(resid, group_size, pred_year, train_year):
    '''
    Produces a scatterplot of residuals (difference of true value over predicted value)
    Input:  True values and predicted values of target variable
    Output: Scatterplot of residuals    
    
    '''    
    plt.figure(figsize=(20,8))
    xx = np.linspace(0, len(resid), num=len(resid))
    plt.scatter(xx, resid, s=20, c="blue", label="residuals")
    plt.xlabel("data")
    plt.ylabel("residual")
    plt.title("Residuals of {} Predictions vs Actuals (train year {}): Participant Count: {}".format(pred_year, train_year, group_size))
    plt.legend()
    plt.show()
    return

def plot_student_residuals(student_resids, group_size, pred_year, train_year):
    '''
    Produces a scatterplot of residuals (difference of true value over predicted value)
    Input:  True values and predicted values of target variable
    Output: Scatterplot of residuals    
    
    '''    
    plt.figure(figsize=(20,8))
    xx = np.linspace(0, len(student_resids), num=len(student_resids))
    plt.scatter(xx, student_resids, s=20, c="blue", label="residuals")
    plt.xlabel("data")
    plt.ylabel("residual")
    plt.title("Studentized Residuals of {} Predictions vs Actuals (train year {}): Participant Count {}".format(pred_year, train_year, group_size))
    plt.legend()
    plt.show()
    return