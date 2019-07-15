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
import json

def build(um_dict, user_id_dict, business_id_dict):
    print('id dicts loading')
    with open(user_id_dict, 'r') as f:
        user_id_dict = json.load(f)
    with open(business_id_dict, 'r') as f:
        business_id_dict = json.load(f)
    print('loading um')
    with open(um_dict, 'r') as f:
        um_dict = json.load(f)
    um_dok = sps.dok_matrix((len(user_id_dict),len(business_id_dict)), dtype=np.int8)
    for key_i, value_i in um_dict.items():
        for key_j, value_j in value_i.items():
            um_dok[user_id_dict[key_i], business_id_dict[key_j]] = value_j
    a = um_dok.tocsr()
    del um_dok
    latent_factors = 25
    u = np.random.random(size = (len(user_id_dict), latent_factors))
    v = np.random.random(size = (latent_factors, len(business_id_dict)))
    u = sps.csr_matrix(u)
    v = sps.csr_matrix(v)
    #print(u)

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
    u_i, u_j = u.nonzero()
    v_i, v_j = v.nonzero()
    while(i < 10 and change > 0.75):
       print('iteration ' + str(i))
       vt = v.transpose()
       u_num = a * vt
       u_denom = w.multiply(u * v) * vt
       for ui, uj in zip(u_i, u_j):
           print("Old u " + str(ui) + ', ' + str(uj) + ': ' + str(u[ui, uj]))
           #u_denom = w[ui, :].multiply(u[ui, :] * v) * vt[:, uj]
           u[ui, uj] = u[ui, uj] * (u_num[ui, uj] / (u_denom[ui, uj] + 0.0000001))
           print("New u " + str(ui) + ', ' + str(uj)  + ': ' + str(u[ui, uj]))
       ut = u.transpose()
       v_num = ut * a
       v_denom = ut * w.multiply(u * v)
       for vi, vj in zip(v_i, v_j):
           print("Old v " + str(vi) + ', ' + str(vj) + ': ' + str(v[vi, vj]))
           #v_denom = ut * w[:, vj].multiply(u * v[:, vj])
           v[vi, vj] = v[vi, vj] * (v_num[vi, vj] / (v_denom[vi, vj] + 0.0000001))
           print("New v" + str(vi) + ', ' + str(vj)  + ': ' + str(v[vi, vj]))
       print('U:')
       print(u)
       print('V:')
       print(v)
       i += 1

       # This takes two matrices, multiplies by weight, subtracts them, and then finds its norm2 

       # uv = u * v
       # uv = w.multiply(uv)

       # norm = a - uv
       # norm = norm.power(2)
       # norm = math.sqrt(norm)

       # This takes two matricies, find each norm2, multiplies by weight, and then subtracts

       uv = u * v
       uv = w.multiply(uv)

       a_norm = a.power(2)
       a_norm = math.sqrt(a_norm)
       uv_norm = uv.power(2)
       uv_norm = math.sqrt(uv_norm)

       norm = a_norm - uv_norm

       prev_norm = curr_norm
       curr_norm = norm
       change = curr_norm - prev_norm
       

def main():
    t1 = time.time()
    build('../datasets/yelp_dataset/utility-matrix/yelp_set1_user_um.json', '../datasets/yelp_dataset/utility-matrix/yelp_uc_user_id.json', '../datasets/yelp_dataset/utility-matrix/yelp_uc_item_id.json')
    print(time.time() - t1)

if __name__ == '__main__':
    main()