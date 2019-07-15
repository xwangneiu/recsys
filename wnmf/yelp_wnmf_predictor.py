# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 14:03:52 2019

@author: jonathan
"""

import numpy as np
import pandas as pd
import math
import json
import sys
sys.path.insert(0, '../')
import os
import datasets

#takes: a U factor resulting from WNMF of a training set utility matrix; a V factor resulting from WNMF of a training set utlity 
def predict(u_df, v_df, test_set, output_file_path, user_id_dict, business_id_dict):
    
    with open(user_id_dict, 'r') as f:
        user_id_dict = json.load(f)
    with open(business_id_dict, 'r') as f:
        business_id_dict = json.load(f)
    print('loading um')
    
    
    u = u_df.to_numpy()
    v = v_df.to_numpy()
    print(u)
    print(v)
    #rebuild prediction matrix by multiplying factor matrices
    pm = np.matmul(u, v)
    
    
    test_set['prediction'] = math.nan
    
    for num, (user, business) in enumerate(zip(test_set['user_id'], test_set['business_id']), start = 0):
        prediction = 1
        try:
            prediction = max(1, pm[user_id_dict[user]][business_id_dict[business]])
            if prediction > 5:
                prediction = 5
        except KeyError:
            prediction = math.nan

        print("User: " + str(user) + " Item: " + str(item) + " Prediction: " + str(prediction))
        test_set.at[num, 'prediction'] = prediction
        
    print(test_set)
    return test_set
    
    
def main():
    print('nothing here yet')
    

if __name__ == '__main__':
    main()
    
    