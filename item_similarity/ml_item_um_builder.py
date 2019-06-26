# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 16:53:52 2019

@author: jonathan
"""

import numpy as np
import pandas as pd

def build(df, output_file):
    #if passing in an og dataframe
    df = df.pivot_table(index='user', columns='movie', values='rating')
    df.to_csv(output_file)
    return df


    
    