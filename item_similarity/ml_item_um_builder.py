# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 16:53:52 2019

@author: jonathan
"""

import numpy as np
import pandas as pd
import sys
sys.path.insert(0, '../')
import os
import datasets

def build(df, output_file):
    #if passing in an og dataframe
    df = df.pivot_table(index='user', columns='movie', values='rating')
    df.to_csv(output_file)
    print("Confirmed: item-based UM built")
    return df


def main():
    os.chdir('..')
    ml_u1 = datasets.load_ml_u1_item_pearson()
    os.chdir('item_similarity')
    build(ml_u1.training.og_df, 'deletethis.csv')
    
if __name__ == '__main__':
    main()
    