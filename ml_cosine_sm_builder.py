# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 17:35:41 2019

@author: jonathan
"""
import numpy as np
import pandas as pd
import correlation

def build(um_df, output_file):
    #Cosine similarity (takes two numpy arrays (columns))        
    utility_np = um_df.to_numpy()
    similarity_np = np.zeros((len(utility_np[0]), len(utility_np[0])), dtype=float) 
    #ITERATE OVER DATA
    for i in range(len(similarity_np)):
        print("Calculating column " + str(i) + "...")
        for j in range(len(similarity_np[i])):
            if similarity_np[j][i] != 0:
                similarity_np[i][j] = similarity_np[j][i]
            else:
                similarity_np[i][j] = correlation.cosine(utility_np[:, i], utility_np[:, j])
                print(similarity_np[i][j])
    
    #EXPORT COMPLETED SIMILARITY MATRIX
    similarity = pd.DataFrame(similarity_np, index = um_df.columns, columns = um_df.columns)
    similarity.to_csv(output_file)
    return similarity