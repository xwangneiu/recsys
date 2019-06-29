#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:50:27 2019

@author: jonathan
"""

f = open('datasets/ml-100k/u2.base', 'r')
user = []
item = []
lines = f.readlines()
for line in range(len(lines)):
    print('line' + str(line))
    lines[line] = lines[line].rstrip('\n').split('\t')
    user = user + [int(lines[line][0])]
    item = item + [int(lines[line][1])]

user = list(set(user))
user.sort()

item = list(set(item))
item.sort()

user_skips = 0
for i in range(1, len(user)):
        if user[i - 1] < user[i] - 1:
            user_skips += 1
item_skips = 0
for i in range(1, len(item)):
        if item[i - 1] < item[i] - 1:
            item_skips += 1
            
print('user skips: ' + str(user_skips) + ' item skips: ' + str(item_skips))



    