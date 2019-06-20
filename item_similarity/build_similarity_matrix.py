# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 11:44:39 2019

@author: jonathan
"""

#builds similarity matrix using Pearson correlation
def build_similarity_matrix(utility_matrix_csv, similarity_matrix_csv_output):
    import numpy as np
    import pandas as pd
    
    utility = pd.read_csv(utility_matrix_csv)

    #create first column/dataframe
    row = utility.corrwith(utility['1'])
    row = pd.DataFrame(row, columns=['1'])
    similarity = row.drop('user')
                       
    def get_item_corrs(item):
        item = str(item)
        row = utility.corrwith(utility[item])
        row = row.drop('user')
        return row
    
    for i in range(2, len(utility.columns)):
        if i % 10 == 0:
            print('Correlating item ' + str(i) + '...')
        similarity[str(i)] = get_item_corrs(i)
        
    print(similarity)
    similarity.to_csv(similarity_matrix_csv_output)