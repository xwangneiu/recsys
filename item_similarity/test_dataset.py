# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 14:06:47 2019

@author: jonathan
"""
import numpy as np
import pandas as pd
import movielens_predictor_item as mlp_item

#takes Pandas Dataframes from a training set and a test set

def import_test_set(test_set_csv):
    #import u.data file
    test_set = pd.read_csv(test_set_csv, sep='\t', names=['user', 'movie', 'rating', 'timestamp'])

    #remove timestamp -- not needed
    del test_set['timestamp']
    
    print(test_set)
    return test_set

#takes Pandas Dataframes from a training set and a test set; returns test set with added columns for predicted ratings and difference
def test_dataset(utility, similarity, test_set):
    predicted_ratings = np.zeros(test_set.shape[0], dtype=float)
    for i in range(len(predicted_ratings)):
        print('Predicting row ' + str(i))
        predicted_ratings[i] = mlp_item.predict(utility, similarity, int(test_set.iat[i, 0]), int(test_set.iat[i, 1]))
    predicted_ratings = pd.Series(predicted_ratings)
    test_results = test_set
    test_results['predicted_ratings'] = predicted_ratings
    '''
    error = np.zeros(test_set.shape[0], dtype=float)
    
    for i in range(test_set.shape[0]):
        test_results test_results.iat[i, 3] 
    '''
    
    print(test_results)
        
def main():
    utility = mlp_item.build_matrices_from_training_set('../datasets/ml-100k/u1.base')
    test_set = import_test_set('../datasets/ml-100k/u1.test')
    test_dataset(utility, similarity, test_set)
    
    
    
if __name__ == '__main__':
    main()
    