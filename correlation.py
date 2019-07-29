# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 17:41:58 2019

@author: jonathan
"""
import numpy as np
import math
import timeit


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

    #multiplies both columns by one another, then divides by one of them (this makes all non-corated elements into nan)
    col1_new = (col1 * col2) / col2
    col2_new = (col2 * col1) / col1
    col1 = col1_new
    col2 = col2_new
    
    #removes nans from both columns, leaving only corated items
    col1 = col1[~np.isnan(col1)]
    col2 = col2[~np.isnan(col2)]    
    
    #if there are no corated values, return 0 to save time
    if len(col1) == 0: #this is a sum of True values (each True == 1)
        return 0
    
    sum_product_distances_from_mean = 0
    sum_squared_col1_distances_from_mean = 0
    sum_squared_col2_distances_from_mean = 0
    
    #get mean values of columns before removing non-corated user ratings
    col1_mean = np.mean(col1) #mean excluding nans
    col2_mean = np.mean(col2)

    for i in range(len(col1)):
        if col1[i] != math.nan:
            #numerator of formula
            col1_distance_from_mean = col1[i] - col1_mean
            col2_distance_from_mean = col2[i] - col2_mean
            sum_product_distances_from_mean += col1_distance_from_mean * col2_distance_from_mean
            #denominator of formula
            sum_squared_col1_distances_from_mean += (col1_distance_from_mean) ** 2
            sum_squared_col2_distances_from_mean += (col2_distance_from_mean) ** 2
            
        
    corr = sum_product_distances_from_mean / ((math.sqrt(sum_squared_col1_distances_from_mean) * math.sqrt(sum_squared_col2_distances_from_mean)) + 0.0000001)
    return corr        

#Parameters: two numpy 1-dimensional arrays (item/user vectors)
def cosine(col1, col2):
    
    col1_new = (col1 * col2) / col2
    col2_new = (col2 * col1) / col1
    col1 = col1_new
    col2 = col2_new
    #removes nans from both columns, leaving only corated items
    col1 = col1[~np.isnan(col1)]
    col2 = col2[~np.isnan(col2)]

    
    #if there are no corated values, return 0 to save time
    if len(col1) == 0: #this is a sum of True values (each True == 1)
        return 0
    '''
    dot_col1_col2 = np.nansum(col1 * col2)
    norm_col1 = math.sqrt(np.nansum(np.power(col1, [2])))
    norm_col2 = math.sqrt(np.nansum(np.power(col2, [2])))
    return dot_col1_col2 / (norm_col1 * norm_col2)
    '''
    return np.dot(col1, col2) / (np.linalg.norm(col1, ord=2) * np.linalg.norm(col2, ord=2))

def cos_old(col1, col2):
    
    col1 = np.nan_to_num(col1)
    col2 = np.nan_to_num(col2)
    '''
    dot_col1_col2 = np.nansum(col1 * col2)
    norm_col1 = math.sqrt(np.nansum(np.power(col1, [2])))
    norm_col2 = math.sqrt(np.nansum(np.power(col2, [2])))
    return dot_col1_col2 / (norm_col1 * norm_col2)
    '''
    return np.dot(col1, col2) / (np.linalg.norm(col1, ord=2) * np.linalg.norm(col2, ord=2))

#testing using timeit to improve performance: this code may be reused
def operation_time():
    t = timeit.Timer(stmt='''
col1 = col1 * corated
col2 = col2 * corated
col1_mean = np.nanmean(col1) #mean excluding nans
col2_mean = np.nanmean(col2)
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
sum_product_distances_from_mean = 0
sum_squared_col1_distances_from_mean = 0
sum_squared_col2_distances_from_mean = 0
''', setup='''import numpy as np
import math
import datasets
ml_u1 = datasets.load_ml_u1()
col1 = ml_u1.training.um_df['1'].to_numpy()
col2 = ml_u1.training.um_df['2'].to_numpy()
col1_rated = np.logical_not(np.isnan(col1))
#print(col1_rated[0:25])
col2_rated = np.logical_not(np.isnan(col2))
#print(col2_rated[0:25])
corated = np.logical_and(col1_rated, col2_rated)
#print(corated[0:25])
#print(col1_rated[0:25])

#if there are no corated values, return 0 to save time
sum_product_distances_from_mean = 0
sum_squared_col1_distances_from_mean = 0
sum_squared_col2_distances_from_mean = 0
def remove_non_corated(col):
    for i in range(len(col)):
        if corated[i] == False:
            col[i] = math.nan
    return col
    ''')
    tests = 500
    print(str(t.timeit(number=tests) * (1000/tests)) + ' ms per operation')
    #only for testing formulas

def main():
    #print("nothing to see here")
    operation_time()
    
    


if __name__ == '__main__':
    main()