# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 17:35:41 2019

@author: jonathan
"""
import numpy as np
import math
import json
import correlation
import sys
sys.path.insert(0, 'datasets/yelp_dataset/utility-matrix/')

def build(um_dict, output_file):
    #um_df is a dict here
    #Cosine similarity (takes two numpy arrays (columns))        
    similarity = {}
    i_ratings = None
    j_ratings = None
    #ITERATE OVER DATA
    user_num = 0
    for key_i, value_i in um_dict.items():
        print('Calculating user ' + str(user_num))
        user_num += 1
        for key_j, value_j in um_dict.items():
            # for key i in um_data:
            # for key 
            i_items_set = set(value_i.keys())
            j_items_set = set(value_j.keys())
            union = list(i_items_set | j_items_set)
            i_ratings = np.zeros(len(union), dtype=float)
            j_ratings = np.zeros(len(union), dtype=float)
            for k in range(len(union)):
                if union[k] in value_i:
                    i_ratings[k] = value_i[union[k]]
                else:
                    i_ratings[k] = math.nan
                if union[k] in value_j:
                    j_ratings[k] = value_j[union[k]]
                else:
                    j_ratings[k] = math.nan
            duplicate = False
            temp = None
            if key_j in similarity:
                if key_i in similarity[key_j]:    
                    temp = similarity[key_j][key_i]
                    duplicate = True
            if key_i in similarity:
                if duplicate:
                    similarity[key_i][key_j] = temp
                else:
                    similarity[key_i][key_j] = correlation.cosine(i_ratings, j_ratings)
            else:
                if duplicate:
                    similarity[key_i] = {}
                    similarity[key_i][key_j] = temp
                else:
                    similarity[key_i] = {}
                    similarity[key_i][key_j] = correlation.cosine(i_ratings, j_ratings)
    with open(output_file, 'w') as f:
        json_dump = json.dumps(similarity)
        f.write(json_dump)
        f.close()
    return similarity

def main():
    utility = None
    with open('datasets/yelp_dataset/utility-matrix/yelp_utility_matrix_uc_user.json', 'r') as f:
        utility = json.load(f)
    build(utility, 'yelp_user_cosine_sm.json')
    #testd(dict)
    
if __name__ == '__main__':
    main()
    