# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 17:35:41 2019

@author: jonathan
"""
import numpy as np
import pandas as pd
import correlation
import timeit

def build(um_df, output_file):
    #Pearson correlation (takes two numpy arrays (columns))        
#NEED TO IMPLEMENT CODE THAT MAKES IT WORK EVEN IF UTILITY NOT BUILT, etc.:
    utility_np = um_df.to_numpy()
    similarity_np = np.zeros((len(utility_np[0]), len(utility_np[0])), dtype=float) 
    #ITERATE OVER DATA
    for i in range(len(similarity_np)):
        print("Calculating column " + str(i) + "...")
        similarity_np[i][i] = 1
        for j in range(i + 1, len(similarity_np[i])):
            corr = correlation.cosine(utility_np[:, i], utility_np[:, j])
            similarity_np[i][j] = corr
            similarity_np[j][i] = corr
    
    #EXPORT COMPLETED SIMILARITY MATRIX
    similarity = pd.DataFrame(similarity_np, index = um_df.columns, columns = um_df.columns)
    similarity.to_csv(output_file)
    return similarity

def main():
    t = timeit.Timer(stmt='''
i = j = 500
print("Calculating column " + str(i) + "...")
similarity_np[i][i] = 1
for j in range(i + 1, len(similarity_np[i])):
    corr = correlation.pearson(utility_np[:, i], utility_np[:, j])
    similarity_np[i][j] = corr
    similarity_np[j][i] = corr
    

''', setup='''import numpy as np
import pandas as pd
import correlation
import sys
sys.path.insert(0, '../')
import os
import datasets
os.chdir('...')
ml_u1 = datasets.load_ml_u1()
os.chdir('item_similarity')
um_df = ml_u1.training.um_df
utility_np = um_df.to_numpy()
similarity_np = np.zeros((len(utility_np[0]), len(utility_np[0])), dtype=float) 
    ''')
    tests = 50
    print(str(t.timeit(number=tests) * (1000/tests)) + ' ms per operation')
    
if __name__ == '__main__':
    main()