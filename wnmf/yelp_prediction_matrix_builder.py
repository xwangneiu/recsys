# SCSE RecSys Group
# Minh N.
# 2019.07.10
# This module will take a utility matrix in json format and build a prediction matrix

import scipy as sp
from scipy import sparse as sps
import numpy as np
import sys
import math
import time
import timeit
import json
import pandas as pd

def read_dict(um_dict):
    with open(um_dict, 'r') as f:
        um_dict = json.load(f)
    return um_dict

def find_missing(set_u, set_b, dict_with_missing):
    missing_u = set_u.difference(set(dict_with_missing.keys()))
    missing_b = set_b.difference(set([i for x in dict_with_missing.values() for i in x.keys()]))
    return missing_u, missing_b

def build(um_dict, output_filename, latent_factors, wnmf_iterations, user_id_dict, business_id_dict):
    print('id dicts loading')
    with open(user_id_dict, 'r') as f:
        user_id_dict = json.load(f)
    with open(business_id_dict, 'r') as f:
        business_id_dict = json.load(f)
    print('loading um')
    um_dok = sps.dok_matrix((len(user_id_dict),len(business_id_dict)), dtype=np.int8)
    for key_i, value_i in um_dict.items():
        for key_j, value_j in value_i.items():
            um_dok[user_id_dict[key_i], business_id_dict[key_j]] = value_j
    a = um_dok.tocsr()
    missing_u, missing_b = find_missing(set(user_id_dict.keys()), set(business_id_dict.keys()), um_dict)
    del um_dict
    u = np.random.random(size = (len(user_id_dict), latent_factors))
    v = np.random.random(size = (latent_factors, len(business_id_dict)))
    for i in missing_u:
      u[user_id_dict[i],:] = 0
    for i in missing_b:
      v[:,business_id_dict[i]] = 0
    np.set_printoptions(threshold=np.inf)
    print(u)

    #get nonzero rows, columns
    x, y = a.nonzero()

    #copy um_csr into new sparse matrix
    w = a.copy()
    for i, j in zip(x, y):
        w[i, j] = 1

    i = 0
    prev_norm = 0
    curr_norm = 0
    change = 999999
    print('starting wnmf loop')
    while(i < wnmf_iterations and change > 2):
       print('iteration ' + str(i))
       vt = v.transpose()
       u_num = a * vt
       u_denom = w.multiply(np.matmul(u, v)) * vt
       for ui in range(np.size(u, 0)):
          for uj in range(np.size(u, 1)):
           # print("Old u " + str(ui) + ', ' + str(uj) + ': ' + str(u[ui, uj]))
           #u_denom = w[ui, :].multiply(u[ui, :] * v) * vt[:, uj]
           u[ui, uj] = u[ui, uj] * (u_num[ui, uj] / (u_denom[ui, uj] + 0.0000001))
           # print("New u " + str(ui) + ', ' + str(uj)  + ': ' + str(u[ui, uj]))
       ut = u.transpose()
       v_num = ut * a
       v_denom = ut * w.multiply(np.matmul(u, v))
       for vi in range(np.size(v, 0)):
          for vj in range(np.size(v, 1)):
           # print("Old v " + str(vi) + ', ' + str(vj) + ': ' + str(v[vi, vj]))
           #v_denom = ut * w[:, vj].multiply(u * v[:, vj])
           v[vi, vj] = v[vi, vj] * (v_num[vi, vj] / (v_denom[vi, vj] + 0.0000001))
           # print("New v" + str(vi) + ', ' + str(vj)  + ': ' + str(v[vi, vj]))
       # print('U:')
       # print(u)
       # print('V:')
       # print(v)
       i += 1

       # This takes two matrices, multiplies by weight, subtracts them, and then finds its norm2 

       uv = np.matmul(u, v)
       uv = w.multiply(uv)

       norm = a - uv
       norm = norm.power(2)
       norm = norm.sum()
       norm = math.sqrt(norm)

       prev_norm = curr_norm
       curr_norm = norm
       change = math.fabs(curr_norm - prev_norm)
       print(change)
    u = pd.DataFrame(u)
    v = pd.DataFrame(v)
    u.to_csv((output_filename + 'u.csv'))
    v.to_csv((output_filename + 'v.csv'))
    log_data = str(i) + ',' + str(change)
    return u, v, log_data
       

# um, output file, latent factors, iterations
    
def operation_time():
    t = timeit.Timer(stmt='''

                     ''', setup='''from scipy import sparse as sps
import numpy as np
import sys
import math
import time
import timeit
import json
import pandas as pd
def read_dict(um_dict):
    with open(um_dict, 'r') as f:
        um_dict = json.load(f)
    return um_dict
#initializing variables as needed
um_dict = read_dict('../datasets/yelp_dataset/utility-matrix/yelp_set1_user_um.json')
output_filename = 'wmnf_matrix'
latent_factors = 1
wnmf_iterations = 1
user_id_dict = '../datasets/yelp_dataset/utility-matrix/yelp_uc_user_id.json'
business_id_dict ='../datasets/yelp_dataset/utility-matrix/yelp_uc_item_id.json'
with open(user_id_dict, 'r') as f:
    user_id_dict = json.load(f)
with open(business_id_dict, 'r') as f:
    business_id_dict = json.load(f)
um_dok = sps.dok_matrix((len(user_id_dict),len(business_id_dict)), dtype=np.int8) #0.04319421600030182 ms per operation
for key_i, value_i in um_dict.items():
    for key_j, value_j in value_i.items():
        um_dok[user_id_dict[key_i], business_id_dict[key_j]] = value_j #979.1366858800029 ms per operation
a = um_dok.tocsr() #25.99948301400036 ms per operation
''')
    tests = 500
    print(str(t.timeit(number=tests) * (1000/tests)) + ' ms per operation')
    #only for testing formulas

def main():
    # operation_time()
    
    t1 = time.time()
    um = read_dict('../datasets/yelp_dataset/utility-matrix/yelp_set1_user_um.json')
    build(um, 'wmnf_matrix', 10, 50,'../datasets/yelp_dataset/utility-matrix/yelp_uc_user_id.json', '../datasets/yelp_dataset/utility-matrix/yelp_uc_item_id.json')
    print(time.time() - t1)
    

if __name__ == '__main__':
    main()