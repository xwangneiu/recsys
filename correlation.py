# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 17:41:58 2019

@author: jonathan
"""
import numpy as np
import math

#PEARSON CORRELATION FUNCTION
#Parameters: two numpy 1-dimensional arrays (item/user vectors)
def pearson_meanall(col1, col2):
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
    def remove_non_corated(col):
        for i in range(len(col)):
            if corated[i] == False:
                col[i] = math.nan
        return col
    col1 = remove_non_corated(col1)
    col2 = remove_non_corated(col2)
    col1_mean = np.nanmean(col1) #mean excluding nans
    col2_mean = np.nanmean(col2)
    
    
    for i in range(len(col1)):

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

#Parameters: two numpy 1-dimensional arrays (item/user vectors)
def cosine(col1, col2):
    
    col1 = np.nan_to_num(col1)
    col2 = np.nan_to_num(col2)
    '''
    dot_col1_col2 = np.nansum(col1 * col2)
    norm_col1 = math.sqrt(np.nansum(np.power(col1, [2])))
    norm_col2 = math.sqrt(np.nansum(np.power(col2, [2])))
    return dot_col1_col2 / (norm_col1 * norm_col2)
    '''
    return np.dot(col1, col2) / (np.linalg.norm(col1, ord=2) * np.linalg.norm(col2, ord=2))
    
def main():
    #only for testing formulas
    print(cosine(np.array([1,2,math.nan,4,5]), np.array([1,math.nan,3,9,10])))
    print(cosine(np.array([1,2,math.nan,4,5]), np.array([1,math.nan,3,9,10])))

if __name__ == '__main__':
    main()