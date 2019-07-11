# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 14:03:52 2019

@author: jonathan
"""

import numpy as np
import pandas as pd

def get_index_dicts(training_um_df):
    user_indices = training_um_df.index.to_numpy()
    user_indices = [int(x) for x in user_indices]
    print(user_indices)
    item_indices = training_um_df.columns.to_numpy()
    item_indices = [int(x) for x in item_indices]
    print(item_indices)
    #need to make dictionary such that keys are actual IDs, and values are positional.
    uid_to_index = {} #actual user id -> zero-based index in 2d array
    index_to_uid = {} #zero-based index in 2d array -> actual user id
    for i in range(len(user_indices)):
        uid_to_index[user_indices[i]] = i

    iid_to_index = {} #actual item id -> zero-based index in 2d array
    index_to_iid = {} #zero-based index in 2d array -> actual item id
    for i in range(len(item_indices)):
        iid_to_index[item_indices[i]] = i

    return uid_to_index, iid_to_index
#takes: a U factor resulting from WNMF of a training set utility matrix; a V factor resulting from WNMF of a training set utlity 
def predict(training_um_df, training_u_df, training_v_df, users_and_items, results_csv):
    u = training_u_df.to_numpy()
    v = training_v_df.to_numpy()
    #rebuild prediction matrix by multiplying factor matrices
    pm = np.matmul(u, v)
    uid_to_index, iid_to_index = get_index_dicts(training_um_df)
    
    users_and_items = users_and_items.to_numpy()
    predictions = np.zeros(len(users_and_items), dtype=float)
    
    for i in range(len(users_and_items)):
        print('Predicting user/item pair ' + str(i + 1))
        
        user = users_and_items[i][0]
        item = users_and_items[i][1]
        prediction = pm[uid_to_index[user]][iid_to_index[item]]
        print("User: " + str(user) + " Item: " + str(item) + "Prediction: " + str(prediction))
        predictions[i] = prediction
    
    
    
    
    