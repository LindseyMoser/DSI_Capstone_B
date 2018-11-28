#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')


colors = itertools.cycle(["c", "m", "y"])

def plot_results(y_true, y_pred):
    '''
    Produces a scatterplot of actual target vs. predicted target values
    Input:  True values and predicted values of target variable
    Output: Scatterplot
    
    '''
    plt.figure(figsize=(20,8))
    plt.scatter(y_true,y_pred, s=20, color=next(colors), label="data")
    plt.xlabel("data")
    plt.ylabel("Funding Target")
    plt.title("Predicting Funding Target from Linear Regression trained on 2014 data")
    plt.legend()
    plt.show()
    return

def plot_residuals(y_true, y_pred):
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
    plt.title("Residuals of Predictions vs Actuals (Linear Regerssion)")
    plt.legend()
    plt.show()
    return