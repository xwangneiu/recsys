# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 17:41:58 2019

@author: jonathan
"""
import numpy as np
import math

#PEARSON CORRELATION FUNCTION
def pearson(col1, col2):
    #Finds corated values by checking each element of each array for non-NaN status and performing AND on the results
    col1_rated = np.logical_not(np.isnan(col1))
    #print(col1_rated[0:25])
    col2_rated = np.logical_not(np.isnan(col2))
    #print(col2_rated[0:25])
    corated = np.logical_and(col1_rated, col2_rated)
    #print(corated[0:25])
    #print(col1_rated[0:25])
    
    #if there are no corated values, return 0 to save time
    if np.sum(corated) == 0: #this is a sum of True values (each True == 1)
        return 0
    
    sum_product_distances_from_mean = 0
    sum_squared_col1_distances_from_mean = 0
    sum_squared_col2_distances_from_mean = 0
    #get mean values of columns before removing non-corated user ratings
    col1_mean = np.nanmean(col1) #mean excluding nans
    col2_mean = np.nanmean(col2)
    
    for i in range(0, len(col1)):

        if corated[i]:
            #numerator of formula
            col1_distance_from_mean = col1[i] - col1_mean
            col2_distance_from_mean = col2[i] - col2_mean
            sum_product_distances_from_mean += col1_distance_from_mean * col2_distance_from_mean
            #denominator of formula
            sum_squared_col1_distances_from_mean += (col1[i] - col1_mean) ** 2
            sum_squared_col2_distances_from_mean += (col2[i] - col2_mean) ** 2
        
    corr = sum_product_distances_from_mean / ((math.sqrt(sum_squared_col1_distances_from_mean) * math.sqrt(sum_squared_col2_distances_from_mean)) + 0.0000001)
    return corr    