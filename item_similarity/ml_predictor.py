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

def predict(dataset, dest_filename):
    #similarity of all items to active item. INDICES OK
    
    sim = dataset.training.sm_df.to_numpy()
    utility = dataset.training.um_df.to_numpy()
    results = pd.DataFrame(dataset.test.og_df)
    users_and_items = dataset.test.user_item_pairs_df.to_numpy()
    predictions = np.zeros(len(users_and_items), dtype=float)
    
    #this loop produces a prediction for each user/item in the users_and_items_np list
    for i in range(len(users_and_items)):
        print('Predicting user/item pair ' + str(i + 1))
        user = users_and_items[i][0] - 1 #have to subtract 1 to match numpy zero-based indexing
        item = users_and_items[i][1] - 1 #have to subtract 1 to match numpy zero-based indexing
        user_ratings = utility[user, :]
        sim_item = sim[item, :]
        
        #print(sim_item)
        
        #remove unrated items from similarity list
        user_rating_nan = np.isnan(user_ratings)
        for j in range(len(sim_item)):
            if user_rating_nan[j]:
                sim_item[j] = math.nan        

        #gets np array of tuples of top 30 most similar items to active item
        dtype = [('index', int), ('similarity', float)]
        sim_item_index = np.zeros(len(sim_item), dtype=dtype)
        for j in range(len(sim_item)):
            if math.isnan(sim_item[j]) or item == j: #ensures active item itself, if already rated by user, is eliminated
                continue;
            else:
                sim_item_index[j][0] = j
                sim_item_index[j][1] = sim_item[j]
        sim_item_index = np.sort(sim_item_index, kind='heapsort', order='similarity')[::-1] #sort by similarity (descending), then reverse with [::-1] so ascending
        top_30_sim_items = sim_item_index[:30]
        dtype = [('index', int), ('rating', float)]
        ratings_top_30 = np.zeros(30, dtype=dtype)
        
        #collects np array of tuples of ratings of top 30 most similar items to active item
        for j in range(len(ratings_top_30)):
            ratings_top_30[j][0] = top_30_sim_items[j][0]
            ratings_top_30[j][1] = user_ratings[ratings_top_30[j][0]]
        
        weighted_top_30 = np.array(ratings_top_30)
        #gets weighted ratings of the top 30
        for j in range(len(top_30_sim_items)):
            weighted_top_30[j][1] = top_30_sim_items[j][1] * ratings_top_30[j][1]
        
        #gets sum of the absolute values of the top 30 most similar items' correlation coefficients
        #also gets sum of the weighted ratings of the top 30
        sum_abs_correlations = 0
        sum_weighted_ratings = 0
        for j in range(len(ratings_top_30)):
            sum_abs_correlations += abs(top_30_sim_items[j][1])
            sum_weighted_ratings += weighted_top_30[j][1]
        
        prediction = sum_weighted_ratings / sum_abs_correlations
        
        print('Top 30 similar:')
        print(top_30_sim_items)
        time.sleep(3)
        print('Top 30 ratings:' )
        print(ratings_top_30)
        time.sleep(3)
        print('Top 30 ratings, weighted:' )
        print(weighted_top_30)
        time.sleep(3)
        print('PREDICTION for user ' + str(user + 1) + ' on item ' + str(item + 1) + ': ' + str(prediction))
        time.sleep(3)

        predictions[i] = prediction
        predictions = pd.Series(predictions)
        
    results['prediction'] = predictions
    results.to_csv(dest_filename)
    return results

#adds a prediction to a test set object
    
def main():
    #load MovieLens dataset
    
    #had to change directory, so we can run the called function in recsys/ rather than recsys/item_similarity/
    os.chdir('..')
    #ml_100k = datasets.load_ml_100k()
    ml_u1 = datasets.load_ml_u1()
    os.chdir('item_similarity')
    prediction = predict(ml_u1, 'filename')
    print(prediction)
    
    #print(ml_u1.test.predictions_df)
    #ml_u1.test.save_test_results('ml_u1_2019_06_24_test_results.csv')
    
    
    
    
if __name__ == '__main__':
    main()