# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 09:13:22 2019

@author: jonathan
"""
import math
import numpy as np
import pandas as pd
import scipy

from sklearn.decomposition import NMF

#get utility matrix (pandas dataframe)
#convert to numpy

def build(um_df, output_file):
    
    print("converting UM to np.array")
    r = um_df.to_numpy()
    
    print("creating matrix W")
    #create a new matrix with 1 for observed values in r and 0 otherwise
    def observed(num):
        if math.isnan(num):
            return 0
        elif num == 0.0:
            return 0
        else:
            return 1
    
    w = [[observed(j) for j in i] for i in r]
    
    #change NaNs in r to zero
    r = np.nan_to_num(r)
    
    
    print(w)
    print(r)
        
    #print(stats.zscore(um[row]))
    

def main():
    print("loading um")
    um = pd.read_csv('../datasets/ml-100k/utility-matrix/ml_u1_item_um.csv', index_col=0)
    
    pm = build(um, 'wnmf_test.csv')
    
    
if __name__ == '__main__':
    main()
        
        
        