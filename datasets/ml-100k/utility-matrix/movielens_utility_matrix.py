# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 11:09:01 2019

@author: jonathan
"""
def utility_matrix(data_csv, output_csv):
    import numpy as np
    import pandas as pd
    
    #import u.data file
    df = pd.read_csv('../u.data', sep='\t', names=['user', 'movie', 'rating', 'timestamp'])
    
    #remove timestamp -- not needed
    del df['timestamp']
    
    #create utility matrix using pivot table
    utility_matrix = df.pivot_table(index='user', columns='movie', values='rating')
    
    #export as csv
    utility_matrix.to_csv(output_csv)

def main():
    utility_matrix('../u.data', 'movielens_utility_matrix.csv')

if __name__ == '__main__':
    main()