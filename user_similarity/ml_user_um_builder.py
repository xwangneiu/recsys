# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 16:53:52 2019

@author: jonathan
"""

import numpy as np
import pandas as pd
import math
import sys
sys.path.insert(0, '../')
import os
import datasets

def build(df, output_file):
    #if passing in an og dataframe
    df = df.pivot_table(index='user', columns='movie', values='rating').T
    '''
    df_np = df.to_numpy()
    df_np = df_np.T
    data = pd.DataFrame(df_np)
    '''
    df.to_csv(output_file)
    print("Confirmed: User-based utility matrix built")
    return df

def main():
    #load MovieLens u1 dataset
    #had to change directory, so we can run the called function in recsys/ rather than recsys/item_similarity/
    os.chdir('..')
    og_df = pd.read_csv('datasets/ml-100k/u1.base', sep='\t', names=['user', 'movie', 'rating', 'timestamp'])
    del og_df['timestamp']
    print("Original MovieLens data file ready (og_df)")
    print("og_df")
    print(og_df)
    #ml_u1 = datasets.load_ml_u1_user_pearson()
    os.chdir('user_similarity')
    print(build(og_df, 'deletethis.csv'))
        
if __name__ == '__main__':
    main()
    
    