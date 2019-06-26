# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 17:35:41 2019

@author: jonathan
"""
import numpy as np
import pandas as pd
import json
import correlation

def build(um_dict, output_file):
    #um_df is a dict here
    #Cosine similarity (takes two numpy arrays (columns))        
    similarity = {}
    i_ratings = None
    j_ratings = None
    #ITERATE OVER DATA
    for key_i, value_i in um_dict.items():
        #inner_dict = um_dict[key_i]
        for key_j, value_j in um_dict.items():
            # for key i in um_data:
            # for key 
            '''
            print('key i : ' + str(key_i))
            print('value i : ' + str(value_i))
            print('key j : ' + str(key_j))
            print('value j : ' + str(value_j))
            '''
            i_items_set = set(value_i.keys())
            j_items_set = set(value_j.keys())
            intersection = list(i_items_set & j_items_set)
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
            print('i_ratings: ' + str(i_ratings))
            print('j_ratings: ' + str(j_ratings))
            
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
    
    return similarity

            
                

                
    '''
    for i in range(len(similarity_np)):
        print("Calculating column " + str(i) + "...")
        for j in range(len(similarity_np[i])):
            if similarity_np[j][i] != 0:
                similarity_np[i][j] = similarity_np[j][i]
            else:
                similarity_np[i][j] = correlation.cosine(utility_np[:, i], utility_np[:, j])
    
    #EXPORT COMPLETED SIMILARITY MATRIX
    similarity = pd.DataFrame(similarity_np, index = um_df.columns, columns = um_df.columns)
    similarity.to_csv(output_file)
    '''
def testd(um_dict):
    for key, value in um_dict.items():
        #inner_dict = um_dict[key_i]
        for key_j, value_j in um_dict.items():
            # for key i in um_data:
            # for key 
            print('key i : ' + str(key))
            print('value i : ' + str(value.keys()))
            print('key j : ' + str(key_j))
            print('value j : ' + str(value_j.keys()))

def main():
    dict = {'user1': {'item1': 4.24, 'item2': 4.39, 'item4': 3.38, 'item9': 3.81},
            'user2': {'item1': 5.00, 'item2': 3.31, 'item3': 3.19, 'item9': 3.18}}
    print(build(dict, 'file.json'))
    #testd(dict)
    
if __name__ == '__main__':
    main()
    