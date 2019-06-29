# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 13:01:47 2019

@author: jonathan
"""

import numpy as np
import pandas as pd
import math
import sys
sys.path.insert(0, '../')
import os
import datasets
import time
import random

def predict(dataset, dest_filename):
    #similarity of all items to active item. INDICES OK
    
    print(dataset.training.sm_df)
    sm = dataset.training.sm_df.to_numpy()
    um = dataset.training.um_df.to_numpy()
    sm_indices = dataset.training.sm_df.index.to_numpy()
    sm_indices = [int(x) for x in sm_indices]
    print(sm_indices)
    um_indices = dataset.training.um_df.index.to_numpy()
    um_indices = [int(x) for x in um_indices]
    print(um_indices)
    
    #need to make dictionary such that keys are actual IDs, and values are positional.
    sm_a2p_ix = {} #similarity matrix actual index -> positional index
    sm_p2a_ix = {} #similarity matrix positional index -> actual index
    for i in range(len(sm_indices)):
        sm_a2p_ix[sm_indices[i]] = i
        sm_p2a_ix[i] = sm_indices[i]
    um_a2p_ix = {} #utility matrix actual index -> positional index
    um_p2a_ix = {} #utility matrix positional index -> actual index
    for i in range(len(um_indices)):
        um_a2p_ix[um_indices[i]] = i
        um_p2a_ix[i] = um_indices[i]

    

    results = pd.DataFrame(dataset.test.og_df)
    users_and_items = dataset.test.user_item_pairs_df.to_numpy()
    predictions = np.zeros(len(users_and_items), dtype=float)
    
    def rnd():
        return random.uniform(1.0, 5.0)
    for i in range(len(predictions)):
        predictions[i] = rnd()
        
    predictions = pd.Series(predictions)
        
    results['prediction'] = predictions
    print(results)
    results.to_csv(dest_filename)
    return results

#adds a prediction to a test set object
    
def main():
    #load MovieLens dataset
    
    #had to change directory, so we can run the called function in recsys/ rather than recsys/item_similarity/
    os.chdir('..')
    #ml_100k = datasets.load_ml_100k()
    ml_u1 = datasets.load_ml_u1_user_pearson()
    print(ml_u1.training.um_df)
    os.chdir('user_similarity')
    prediction = predict(ml_u1, 'filename')
    print(prediction)
    
    #print(ml_u1.test.predictions_df)
    #ml_u1.test.save_test_results('ml_u1_2019_06_24_test_results.csv')
    
    
    
    
if __name__ == '__main__':
    main()