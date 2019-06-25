# -*- coding: utf-8 -*-
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
    
    #returns one number, a float

def main():
    #load MovieLens u1 dataset
    #had to change directory, so we can run the called function in recsys/ rather than recsys/item_similarity/
    os.chdir('..')
    ml_u1 = datasets.load_ml_u1()
    os.chdir('item_similarity')
    print(calculate_rmse(ml_u1.test.predictions_df))
    

if __name__ == '__main__':
    main()
    
    