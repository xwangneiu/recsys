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
	with open(user_id_dict, 'r') as f:
		user_id_dict = json.load(f)
	with open(business_id_dict, 'r') as f:
		business_id_dict = json.load(f)
	with open(um_dict, 'r') as f:
		um_dict = json.load(f)
	um_dok = sps.dok_matrix((len(user_id_dict),len(business_id_dict)), dtype=np.int8)
	for key_i, value_i in um_dict.items():
		for key_j, value_j in value_i.items():
			um_dok[user_id_dict[key_i], business_id_dict[key_j]] = value_j
	um_csr = um_dok.tocsr()
	del um_dok
	latent_factors = 25 
	um_u = np.random.random(size = (len(user_id_dict), latent_factors))
	um_v = np.random.random(size = (latent_factors, len(business_id_dict)))
	um_csr_u = sps.csr_matrix(um_u)
	um_csr_v = sps.csr_matrix(um_v)
	del um_u
	del um_v
	print(um_csr_u)

def main():
	t1 = time.time()
	build('../datasets/yelp_dataset/utility-matrix/yelp_set1_user_um.json', '../datasets/yelp_dataset/utility-matrix/yelp_uc_user_id.json', '../datasets/yelp_dataset/utility-matrix/yelp_uc_item_id.json')
	print(time.time() - t1)

if __name__ == '__main__':
	main()