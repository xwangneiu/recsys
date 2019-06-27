# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 13:00:58 2019

@author: jonathan
"""

import numpy as np
import pandas as pd
import math
import sys
sys.path.insert(0, '../')
import os
import datasets

def predict(dataset, users_and_items):
    utility = dataset.training.um_df #utility matrix from MovieLens dataset
    print(utility)
    
    
    #we want this to return a pandas dataframe with the results, for now

    
def main():
    os.chdir('..')
    #ml_100k = datasets.load_ml_100k()
    ml_u1 = datasets.load_ml_u1_for_wnmf()
    os.chdir('wnmf')
    predict(ml_u1, ml_u1.test.user_item_pairs_df)
    

if __name__ == '__main__':
    main()