# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 11:45:52 2019

@author: jonathan
"""
import pandas as pd
import numpy as np
import json

#loads u.item file with movie IDs and titles; returns dict movie_id and 1D list movie_list with titles only
def get_movie_info():
    movie_data = pd.read_csv('../datasets/ml-100k/u.item', sep='\|', header=None)
    movie_data = movie_data.drop(movie_data.iloc[:, 2:24], axis=1)
    movie_data = movie_data.to_numpy()
    movie_list = movie_data[:, 1]
    print(movie_list)
    movie_id = {}
    for i in range(len(movie_data)):
        movie_id[movie_data[i][0]] = movie_data[i][1]
        movie_id[movie_data[i][1]] = movie_data[i][0]
    return movie_id, movie_list
    
def main():
    get_movie_info()

if __name__ == '__main__':
    main()