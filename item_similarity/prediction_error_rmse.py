"""
Created on Tue Jun 25 10:32:29 2019

@author: Sana Kanwal
"""
import numpy as np
import pandas as pd
import math
import sys
sys.path.insert(0, '../')
import os
import datasets

def calculate_rmse(dataframe):
    #dataframe has 'user', 'item', 'observed' columns
    #Function that Calculate Root Mean Square
    print(dataframe)
    dataframe= dataframe.dropna()
    dataframe['error'] = dataframe['observed'] - dataframe['prediction']
    error_arr = dataframe.error.to_numpy()

    def rmsValue(arr, n):
        square = 0
        mean = 0.0
        root = 0.0

        # Calculate square
        for i in range(0, n):
            square += (arr[i] ** 2)

            # Calculate Mean
        mean = (square / (float)(n))

        # Calculate Root
        root = math.sqrt(mean)

        return root

    return rmsValue(error_arr, len(error_arr))

    #Driver code
def main():
    #load MovieLens u1 dataset
    #had to change directory, so we can run the called function in recsys/ rather than recsys/item_similarity/
    os.chdir('..')
    ml_u1 = datasets.load_ml_u1()
    os.chdir('item_similarity')
    print(calculate_rmse(ml_u1.test.predictions_df))
    #calculate_rmse(ml_u1.test.predictions_df)


    
    

if __name__ == '__main__':
    arr = [10, 4, 6, 8]
    n = len(arr)
    #print(rmsValue(arr, n))
    # returns one number, a float
    main()
    