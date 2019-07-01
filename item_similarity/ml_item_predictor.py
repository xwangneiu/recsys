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
    print(sm_a2p_ix)
    print(sm_p2a_ix)
    um_a2p_ix = {} #utility matrix actual index -> positional index
    um_p2a_ix = {} #utility matrix positional index -> actual index
    for i in range(len(um_indices)):
        um_a2p_ix[um_indices[i]] = i
        um_p2a_ix[i] = um_indices[i]

    
    '''
    results = pd.DataFrame(dataset.test.og_df)
    users_and_items = dataset.test.user_item_pairs_df.to_numpy()
    predictions = np.zeros(len(users_and_items), dtype=float)
    
    #this loop produces a prediction for each user/item in the users_and_items_np list
    for i in range(len(users_and_items)):
        print('Predicting user/item pair ' + str(i + 1))
        
        user = users_and_items[i][0]
        item = users_and_items[i][1]
        prediction = None
        print("User: " + str(user) + " Item: " + str(item))
        #if predictions are requested on items/users not in training set
        user_ratings = None
        if user not in um_a2p_ix:
            prediction = math.nan
        else:
            user_ratings = um[um_a2p_ix[user], :]
            
            #process into dictionary ratings
            #ratings keys are ACTUAL 
            ratings = {}
            for j in range(len(user_ratings)):
                if not np.isnan(user_ratings[j]):
                    ratings[sm_p2a_ix[j]] = user_ratings[j]
            #print(ratings)
            #print(user_ratings)
            sim_item = None
            if user not in sm_a2p_ix:
                prediction = math.nan
            else:     
                sim_item = sm[sm_a2p_ix[item], :]
                
                similarities = {}
                for j in range(len(sim_item)):
                    if not np.isnan(sim_item[j]):
                        if sm_p2a_ix[j] in ratings:
                            similarities[sm_p2a_ix[j]] = sim_item[j]
                #print(similarities)
                
                #get top 30 most similar
                #gets np array of tuples of top 30 most similar (items|users) to active item
                dtype = [('index', int), ('similarity', float)]
                sim_index = np.zeros(len(similarities), dtype=dtype)
                j = 0
                for index, similarity in similarities.items():
                    sim_index[j][0] = index
                    sim_index[j][1] = similarity
                    j += 1
                sim_index = np.sort(sim_index, kind='heapsort', order='similarity')[::-1] #sort by similarity (descending), then reverse with [::-1] so ascending
                top_30_most_sim = sim_index[1:31]
                
                
                dtype = [('index', int), ('rating', float)]
                
                ratings_top_30 = np.zeros(30, dtype=dtype)
                for j in range(len(top_30_most_sim)):
                    ratings_top_30[j][0] = top_30_most_sim[j][0]
                    ratings_top_30[j][1] = ratings[top_30_most_sim[j][0]]
            
                
                weighted_top_30 = np.array(ratings_top_30)
            
        
                #gets weighted ratings of the top 30
                for j in range(len(top_30_most_sim)):
                    weighted_top_30[j][1] = top_30_most_sim[j][1] * ratings_top_30[j][1]
                
                print('Top 30 similar:')
                print(top_30_most_sim)
                #time.sleep(3)
                print('Top 30 ratings:' )
                print(ratings_top_30)
                #time.sleep(3)
                print('Top 30 ratings, weighted:' )
                print(weighted_top_30)
                #time.sleep(3)
                
                #gets sum of the absolute values of the top 30 most similar items' correlation coefficients
                #also gets sum of the weighted ratings of the top 30
                sum_abs_correlations = 0
                sum_weighted_ratings = 0
                
        #        if sum_abs_correlations == 0 or sum_weighted_ratings == 0:
        #            predictions[i] = math.nan
        #            continue
        
                for j in range(len(top_30_most_sim)):
                    if not np.isnan(top_30_most_sim[j][1]):
                        sum_abs_correlations += abs(top_30_most_sim[j][1])
                    if not np.isnan(weighted_top_30[j][1]):
                        sum_weighted_ratings += weighted_top_30[j][1]
                        #print(sum_weighted_ratings)
                
                print('Sum of weighted ratings: ' + str(sum_weighted_ratings))
                print('Sum of absolute correlations: ' + str(sum_abs_correlations))
                
                if sum_abs_correlations == 0 or sum_weighted_ratings == 0:
                    prediction = math.nan
                else:
                    prediction = sum_weighted_ratings / sum_abs_correlations
        print('PREDICTION for user ' + str(user) + ' on item ' + str(item) + ': ' + str(prediction))
        predictions[i] = prediction
        
    predictions = pd.Series(predictions)
        
    results['prediction'] = predictions
    print(results)
    results.to_csv(dest_filename)
    return results
    '''
#adds a prediction to a test set object
    
def main():
    #load MovieLens dataset
    
    #had to change directory, so we can run the called function in recsys/ rather than recsys/item_similarity/
    os.chdir('..')
    #ml_100k = datasets.load_ml_100k()
    ml_u1 = datasets.load_ml_u1_item_pearson()
    print(ml_u1.training.um_df)
    os.chdir('item_similarity')
    prediction = predict(ml_u1, 'filename')
    print(prediction)
    
    #print(ml_u1.test.predictions_df)
    #ml_u1.test.save_test_results('ml_u1_2019_06_24_test_results.csv')
    
    
    
    
if __name__ == '__main__':
    main()