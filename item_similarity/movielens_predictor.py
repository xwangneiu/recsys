# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 13:01:30 2019

@author: jonathan
"""
import numpy as np
import pandas as pd
#input: pandas dataframe

def predictor(similarity_matrix_csv, utility_matrix_csv, user, item, k):
    
    #MAYBE WE WILL NEED TO FIX INDEX and COLUMN LABELS
    similarity = pd.read_csv(similarity_matrix_csv, sep=',')
    
    utility = pd.read_csv(utility_matrix_csv, sep=',')
    
    #CREATE LIST OF K MOST SIMILAR ITEMS
        
        #make a list of the k most similar items in an item's column of the similarity matrix
        item_similarity = pd.DataFrame(similarity[item])
        
        #remove all item 
        #sort in descending order
        #remove the item itself (top item)
        #remove all but the top k items remaining
        
    #CREATE LIST OF USER RATINGS ON K MOST SIMILAR ITEMS
    
    #CREATE LIST CONTAINING USER RATINGS * CORRELATION
    
    
        
        
        