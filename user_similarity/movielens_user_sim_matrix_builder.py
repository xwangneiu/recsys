# SCSE RecSys Group
# Minh N. and Chen T.
# 19.06.18
import pandas as pd
import numpy as np


# Read the utility matrix file (derived from u.data) and 
# transpose so the users are columns and items are rows.
df = pd.read_csv('../datasets/ml-100k/utility-matrix/')
df = df.transpose()