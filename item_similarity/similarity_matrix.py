# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 19:08:25 2019

@author: jonathan
"""
import numpy as np
import pandas as pd
import math
import sys
sys.path.insert(0, '../../')
import os
import datasets

temp = datasets.Dataset()
def build_item_pearson_sim(dataset = temp, source_filename = 'not_entered', dest_filename):
    
    #if a Dataset object is passed as a parameter
    if dataset is not temp and source_filename == 'not_entered':
        source_filename = dataset.item_utility_source
        if dataset.item_utility_df is None:
            dataset.build_item_utility_df()
    #if utility matrix not built yet
    if dataset.item_utility_df is None and source_filename == 'not_entered':
        print("You must provide either an object containing a source utility matrix, or the location of the source itself")
    else:
        utility_np = dataset.item_utility_df.to_numpy()
        similarity_np = np.zeros((len(utility_np[0]), len(utility_np[0])), dtype=float) 
        
        #PEARSON CORRELATION FUNCTION
        def pearson_corr(col1, col2):
            #get mean values of columns before removing non-corated user ratings
            col1_mean = np.nanmean(col1) #mean excluding nans
            col2_mean = np.nanmean(col2)

            #Finds corated values by checking each element of each array for non-NaN status and performing AND on the results
            col1_rated = np.logical_not(np.isnan(col1))
            #print(col1_rated[0:25])
            col2_rated = np.logical_not(np.isnan(col2))
            #print(col2_rated[0:25])
            corated = np.logical_and(col1_rated, col2_rated)
            #print(corated[0:25])
            #print(col1_rated[0:25])
            
            sum_product_distances_from_mean = 0
            sum_squared_col1_distances_from_mean = 0
            sum_squared_col2_distances_from_mean = 0
            
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
        
        #ITERATE OVER DATA
        for i in range(len(similarity_np)):
            print("Item " + str(i))
            for j in range(len(similarity_np[i])):
                if similarity_np[j][i] != 0:
                    similarity_np[i][j] = similarity_np[j][i]
                else:
                    similarity_np[i][j] = pearson_corr(utility_np[:, i], utility_np[:, j])
        
        #EXPORT COMPLETED SIMILARITY MATRIX
        similarity = pd.DataFrame(similarity_np, index = dataset.item_utility_df.columns, columns = dataset.item_utility_df.columns)
        similarity.to_csv(dest_filename)
        dataset.item_pearson_sim_source = dest_filename
        dataset.item_pearson_sim_df = similarity
        
        
        print("My Pearson")
        print(similarity)

def main():
    

if __name__ == '__main__':
    main()
