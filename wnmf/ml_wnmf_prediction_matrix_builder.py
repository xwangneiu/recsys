# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 16:04:35 2019

@author: jonathan
"""

import numpy as np
import pandas as pd
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
    while(iteration < iterations and change > 0.75):
        print('iteration ' + str(iteration))
        #update u
        vt = v.T #1650 x 25
        u_num = np.matmul(a, vt) #948 x 1650 * 1650 x 25 = 948 x 25
        u_denom = np.matmul(np.multiply(w, np.matmul(u, v)), vt) #(948 x 1650) * (1650 x 25) = 948 x 25
        for i in range(len(u)):
            for j in range(len(u[i])):
                u[i][j] = u[i][j] * (u_num[i][j] / (u_denom[i][j] + 0.0000001))
        
        #update v
        ut = u.T
        v_num = np.matmul(ut, a)
        v_denom = np.matmul(ut, np.multiply(w, np.matmul(u, v)))
        for i in range(len(v)):
            for j in range(len(v[i])):
                v[i][j] = v[i][j] * (v_num[i][j] / (v_denom[i][j] + 0.0000001))
        print('U:')
        print(u)
        print('V:')
        print(v)
        prev_norm = curr_norm
        curr_norm = np.linalg.norm((np.multiply(w, (a - np.matmul(u, v)))), ord='fro')
        change = abs(curr_norm - prev_norm)
        print('Previous Norm: ' + str(prev_norm) + ' Current Norm: ' + str(curr_norm) + ' Change: ' + str(change))
        iteration += 1
    
    print('Final WNMF-produced prediction matrix:')
    uv = np.matmul(u, v)
    print(uv)
    u_df = pd.DataFrame(u)
    v_df = pd.DataFrame(v)
    u_df.to_csv(output_filename + '_u.csv')
    v_df.to_csv(output_filename + '_v.csv')
    return u_df, v_df

def main():
    um_df = pd.read_csv('../datasets/ml-100k/utility-matrix/ml_u1_item_um.csv', index_col = 0)
    u_df, v_df = build(um_df, 'wnmf_test_', 3, 25)

if __name__ == '__main__':
    main()