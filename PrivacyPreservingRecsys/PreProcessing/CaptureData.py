#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 13:34:55 2019

Whennever you can generate predictoins, you can use this class. Instead of generating the predicitons on the testSet,
you can generate the predictions based on the entire dataset. Then, these predictions are written into a csv file.


@author: longyin
"""
import os
import csv
import sys
import re
from surprise import Prediction
from EvaluationData import EvaluationData
from MovieLens import MovieLens


class CaptureData:
    
    #copiedRatingPath = '../ml-latest-small/ratings.csv'
    #resultFilePath = '../ml-latest-small/SVD_preprocessed.csv'
    ml = MovieLens()
    userIDs, movieIDs = ml.loadAllIDs()
    predictions = []
    pu = []
    
    def __init__(self,algorithm, dataset, resultFilePath):
        #self.predictions = predictions
        self.algorithm = algorithm
        
        self.trainSet = dataset
        self.resultFilePath = resultFilePath
        #print(f"There are {len(self.userIDs)} users")
        #print(f"There are {len(self.movieIDs)} movies")        
        #print(self.userIDs)
        #print(self.movieIDs)
    
    def showUserLatentFactors(self):
        n = 0
        for eachUser in self.pu: 
            print(eachUser)
            if n == 5:
                break

    def getUserLatentFactors(self):
        self.algorithm.fit(self.trainSet)
        self.pu = self.algorithm.getUserLatentFactors()
        return self
            
    def showPredictions(self):
        
        for x in self.predictions:
            for y in x:
                print("###############################################################################################################")
                print(f"uid: {x[0]}")
                print(f"iid: {x[1]}")
                print(f"r_ui: {x[2]}")
                print(f"est: {x[3]}")
                print(f"details(dict): {x[4]}")
            
    def getPredictions(self):
        
        self.algorithm.fit(self.trainSet)
        n = 0
        m = 0
        for uid in self.userIDs:
            #print(uid)
            predictions_per_user = []
            for iid in self.movieIDs:
                prediction = self.algorithm.predict(str(uid),str(iid),verbose = False)
                #print(f"global mean is : {self.trainSet.global_mean} ...")
                predictions_per_user.append(prediction)
                n = n + 1
                if (n%1000000 == 0) :
                    print( f"Finished predicting {n} movies")
            self.predictions.append(predictions_per_user)
            m = m + 1
            if (m%100 == 0) :
                print( f"Finished predicting {m} users")
        print("Prediction Complete...")
        #print(predictions[0])
        return self
        
    def extract_without_real_ratings(self):
        #predictions = self.getPredictions()
        os.chdir(os.path.dirname(sys.argv[0]))
        with open(self.resultFilePath,'w',newline='',encoding='ISO-8859-1') as f_out:
            print("Output file opened...")
            n = 0
            writer = csv.writer(f_out, sys.stdout, lineterminator='\n')

            print("Starting to extract...")
            writer.writerow(["uid,iid,ratings"])
            for x in self.predictions:
                for y in x:
                    writer.writerow([y[0],y[1],y[3]])
                    n = n + 1
                    if (n%1000000 == 0) :
                        print( f"Finished extracting {n} lines")

    def extract_with_real_ratings(self):
        #predictions = self.getPredictions()
        os.chdir(os.path.dirname(sys.argv[0]))
        with open(self.copiedRatingPath, newline='', encoding='ISO-8859-1') as f_in, open(self.resultFilePath,'w',newline='',encoding='ISO-8859-1') as f_out:
            print("Output file opened...")
            
            reader = csv.reader(f_in)
            writer = csv.writer(f_out, sys.stdout, lineterminator='\n') 
            next(reader)
            has_rating= defaultdict(dict)
            
            for x in self.userIDs:
                for y in self.movieIDs:
                    has_rating[x][y] = 0
                    
            for row in reader:
                has_rating[int(row[0])][int(row[1])] = float(row[2])
                    
            n = 0
            writer.writerow(['uid','iid','ratings'])
            for x in self.predictions:
                for y in x:
                    if has_rating[int(y[0])][int(y[1])] != 0:
                        writer.writerow([y[0],y[1],has_rating[int(y[0])][int(y[1])]])
                    else:
                        writer.writerow([y[0],y[1],y[3]])
                    n = n + 1
                    if (n%1000000 == 0) :
                        print( f"Finished extracting {n} lines")
                        
    def extract_user_latent_factors(self,factors):
        os.chdir(os.path.dirname(sys.argv[0]))
        with open(self.resultFilePath,'w',newline='',encoding='ISO-8859-1') as f_out:
            print("Output file opened...")
            n = 0
            writer = csv.writer(f_out, sys.stdout, lineterminator='\n')
            print("Starting to extract...")           
            for eachUser in self.pu:     
                row = []
                known_user = self.trainSet.knows_user(n)
                if known_user == False:
                    raise Exception(f"There is no such user ID{n}!!")
                row.append(self.trainSet.to_raw_uid(n))
                for factorIndex in range(0, factors):
                    row.append(eachUser[factorIndex])
                       
                writer.writerow(row)
                n = n + 1
                if (n%113 == 0) :
                    print( f"Finished extracting {n} users ...")
                
                
