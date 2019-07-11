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

def build():
	with open('../datasets/yelp_dataset/utility-matrix/yelp_set1_user_um.json', 'r') as f:
		um_dict = json.load(f)

	um_dok = sps.dok_matrix((len(um_dict),1573), dtype=np.int8)
	


def main():
	build()

if __name__ == '__main__':
	main()