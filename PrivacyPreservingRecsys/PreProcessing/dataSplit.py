import os
import sys
import csv

import pandas as pd
from collections import defaultdict


################################################################################################
def creatFilePath(root , quantity):
    trainFiles   = root + 'u%d.base'
    testFiles    = root + 'u%d.test'
    TOI = tuple(range(1, quantity + 1))
    folds_files = [(trainFiles % i, testFiles % i) for i in TOI]
    
    return folds_files, trainFiles, testFiles


################################################################################################
def createFilePath_allTrain(root, quantity):
    trainFiles  = root + 't%d.fullTrain'
    TOI = tuple(range(1, quantity + 1))
    timed_files = [(trainFiles % i) for i in TOI]
    #print(timed_files)
    return timed_files, trainFiles

################################################################################################
def data_analysis(ratingsPath):
    with open(ratingsPath, newline='', encoding='ISO-8859-1') as csvfile:
        ratingReader = csv.reader(csvfile)
        next(ratingReader)  #Skip header line
        n = 0
        for row in ratingReader:
            userID.append(row[0])
            movieID.append(row[1])
            userRating.append(float(row[2]))
            timeStamp.append(int(row[3]))
            n = n+1
            if n%1000000 == 0:
                print(f"Already read {n} lines ...")
        print(f"Read {n} lines in total")
    Tmax   = max(timeStamp)
    Tmin   = min(timeStamp)
    Length = len(timeStamp)
    
    print( f"the max time is {Tmax}, and the min time is {Tmin} ...")
    return Tmax, Tmin, Length#, index
#so the max time is 1427784002, the min time is 789652004.
#I will split the rows into 20 folds, time span is 31906600.
################################################################################################

def writeTrTeFiles(NOFI,timeSpan, dataSpan, ratingMatrix, trainFiles, testFiles,byTime = True):
    matrixList = Boxit(ratingMatrix,timeSpan, dataSpan, byTime)
    
    for i in range(1, NOFI + 1):
        print(f"Start processing file: {trainFiles % i}, {testFiles % i} ...")
        with open(trainFiles % i ,'w',newline='',encoding='ISO-8859-1') as train_out,\
             open( testFiles % i ,'w',newline='',encoding='ISO-8859-1') as  test_out : 
                 
            print("Output file opened...")
            writer_Tr = csv.writer(train_out, sys.stdout, lineterminator='\n')
            writer_Te = csv.writer( test_out, sys.stdout, lineterminator='\n')
            
            print("Starting to write...")
  
            #for ii in range(i, i+7+1):
            for ii in range(i,i+9+1):    
                for row in matrixList[ii]:
                    writer_Tr.writerow(row)
                        
            #for ii in range(i+8,i+9+1):
            for ii in range(i,i+9+1):    
                for row in matrixList[ii]:
                    writer_Te.writerow(row)
            print(f"Finished writing {i} training files and {i} testing files")
            print("============================================================================")
################################################################################################
def writeTrFiles(NOFI,timeSpan,dataSpan,ratingMatrix,trainFiles, byTime = True):
    matrixList = Boxit(ratingMatrix,timeSpan, dataSpan, byTime)
    
    for i in range(1, NOFI + 1):
        print(f"Start processing file: {trainFiles%i} ... ")
        with open(trainFiles % i, 'w', newline = '', encoding = 'ISO-8859-1') as train_out:
        
            print("Output file opened ...")
            writer = csv.writer(train_out,sys.stdout, lineterminator = '\n')
        
            print("Starting to write ... ")
        
            for ii in range(i,i+9+1):
                for row in matrixList[ii]:
                    writer.writerow(row)
            print(f"Finished writing {i} training files ...")
            print("===========================================================================")
###############################################################################################
def Boxit(ratingMatrix, timeSpan, dataSpan, byTime):
    matrixList = defaultdict()
    print("Start to categorize ...")
    if byTime == True:
        n = 0
        for row in ratingMatrix.itertuples():

            i = int((int(row[4]) - oldest_time)/timeSpan) + 1
            #print(f"i : {i} --- row[4] : {row[4]} --- timeSpan : {timeSpan} --- oldest time : {oldest_time} ...")
            if((i in matrixList) == False):
                matrixList[i] = []
            matrixList[i].append([row[1],row[2],row[3],row[4]])
            n = n + 1
            if n%1000000 == 0:
                print(f"Already processed {n} rows ...")
        #print(f"The length of the matrixList is ")
    else:
        n = 0
        print("before the for loop")
        for row in ratingMatrix.itertuples():
            
            i = int(int(row[0]+1)/dataSpan ) + 1
            if((i in matrixList) == False):
                matrixList[i] = []
            matrixList[i].append([row[1],row[2],row[3],row[4]])
            n = n + 1
            if n%1000000 == 0:
                print(f"Already processed {n} lines ...")
                
    return matrixList       
################################################################################################
"""
ratingsPath = '../ml-latest-small/ml-20m/ratings.csv'
outputFile  = '../ml-latest-small/ml-20m/100folds_allTrain/'

NOFI = 91 #number of files
NOFO = 100 #number of folds

os.chdir(os.path.dirname(sys.argv[0]))
folds_files, trainFiles, testFiles = creatFilePath(outputFile, NOFI)
#folds_files, trainFiles = createFilePath_allTrain(outputFile, NOFI)
print(folds_files)                     

userID = []
movieID = []
userRating = []
timeStamp = []

newest_time, oldest_time, number_of_data = data_analysis(ratingsPath)
timeSpan = int((newest_time - oldest_time)/NOFO)
dataSpan = int(number_of_data/NOFO)

print("Start to concatenent to a dictionary ...")
ratings_dict = {'userID':userID,
                'movieID':movieID,
                'userRating':userRating,
                'timeStamp' : timeStamp        }

print("Start to convert to pandas data frame ...")
ratingMatrix = pd.DataFrame(ratings_dict)

print("Start to sort ...")
#print(ratingMatrix)
ratingMatrix = ratingMatrix.sort_values(by = ['timeStamp'])
ratingMatrix = ratingMatrix.reset_index(drop = True)

print("Start to write to the files")
#writeTrFiles(NOFI,timeSpan,dataSpan,ratingMatrix,trainFiles, False)
writeTrTeFiles(NOFI,timeSpan, dataSpan, ratingMatrix, trainFiles, testFiles,byTime = False)
 """





