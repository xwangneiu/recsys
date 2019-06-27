# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 10:32:29 2019

@author: Chen Tang
"""
import numpy as np
import pandas as pd
import math
import sys
sys.path.insert(0, '../')
import os
import datasets




def calculate_mae(dataframe):
    
    dataset = dataframe.to_numpy()
    datasetcov = dataset[~np.isnan(dataset).any(axis=1)]
    a = datasetcov[:,2]
    b = datasetcov[:,3]
    
    mae = sum(abs((a-b))/len(datasetcov))
    rmse = math.sqrt((sum((a-b)**2))/len(datasetcov))
    print(rmse)
    return mae
    #dataframe has 'user', 'item', 'observed' columns
    #returns one number, a float
    

def main():
    #load MovieLens u1 dataset
    #had to change directory, so we can run the called function in recsys/ rather than recsys/item_similarity/
    os.chdir('..')
    ml_u1 = datasets.load_ml_u1()
    os.chdir('item_similarity')
    print(calculate_mae(ml_u1.test.predictions_df))
    

if __name__ == '__main__':
    main()
    
    