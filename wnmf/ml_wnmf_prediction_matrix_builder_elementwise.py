# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 16:04:35 2019

@author: jonathan
"""

import numpy as np
import pandas as pd
import math 
import time


def build(um_df, output_filename, latent_factors, iterations):

    um = um_df.to_numpy()
    

    #original utility matrix 
    a = np.nan_to_num(um)
    
    #create matrix w of weights: 1 for observed values, else 0
    w = np.zeros((len(a), len(a[0])), dtype=int)
    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] != 0:
                w[i][j] = 1
    
              
    
    #factor matrix initialization
    u = np.random.rand(len(a), latent_factors)
    v = np.random.rand(latent_factors, len(a[0]))
    
    iteration = 0
    prev_norm = 0
    curr_norm = 0
    change = 999999
    print('starting wnmf loop')
    while(iteration < iterations and change > 0.0000001):
      u_it = np.nditer(u, flags=['multi_index'])
      v_it = np.nditer(v, flags=['multi_index'])
      while (not u_it.finished or not v_it.finished):
        if not u_it.finished:
          i, j = u_it.multi_index
          num = np.matmul((w[i,:] * a[i,:]), v.T[:,j])
          denom = np.matmul(w[i,:] * np.matmul(u[i,:], v), v.T[:,j])
          u[i][j] = u_it[0] * (num / denom)
          u_it.iternext()
        if not v_it.finished:
          i, j = v_it.multi_index
          num = np.matmul(u.T[i,:], (w[:,j] * a[:,j]))
          denom = np.matmul(u.T[i,:], (w[:,j] * np.matmul(u, v[:,j])))
          v[i][j] = v_it[0] * (num / denom)
          v_it.iternext()
                
      prev_norm = curr_norm
      curr_norm = np.linalg.norm((np.multiply(w, (a - np.matmul(u, v)))), ord='fro')
      change = abs(curr_norm - prev_norm)
      #print('Previous Norm: ' + str(prev_norm) + ' Current Norm: ' + str(curr_norm) + ' Change: ' + str(change))
      iteration += 1
    
    print('Final WNMF-produced prediction matrix:')
    uv = np.matmul(u, v)
    print(uv)
    u_df = pd.DataFrame(u)
    v_df = pd.DataFrame(v)
    u_df.to_csv(output_filename + '_u.csv')
    v_df.to_csv(output_filename + '_v.csv')
    #actual number of iterations and final change between norm of each iteration
    log_data = str(iteration) + ',' + str(change)
    return u_df, v_df, log_data
    
def main():
    um_df = pd.read_csv('../datasets/yelp_dataset/yelp_review_uc_training_um_1.csv', index_col = 0)
    build(um_df, "elwisetest.csv", 2, 2)
    #print(log)
    
if __name__ == '__main__':
    main()