# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 18:38:50 2019

@author: jonathan
"""

'''
Dataset Class
I created this class because each dataset can be represented as an object.
Each dataset has a source csv file,
and will have a utility matrix, a similarity matrix, and a 
Objects are an easy way to bundle them together.
'''
import numpy as np
import pandas as pd
import math
import timeit
from item_similarity import item_predictor

class Dataset:
    #INSTANCE VARIABLES
    #text description of dataset
    name = None
    
    #Algorithm type: item-based, user-based, WNMF
    algorithm = None
    
    #raw data file/CSV location
    source = None
    
    #pandas dataframe processed directly from source
    df = None
    
    #ITEM-BASED INSTANCE VARIABLES
    #item-based utility matrix source file
    item_utility_source = None
    
    #item-based utility dataframe
    item_utility_df = None
    
    #item-based cosine similarity matrix source file
    item_cos_sim_source = None
    
    #item-based cosine similarity matrix dataframe
    item_cos_sim_df = None
    
    #item-based Pearson correlation similarity matrix source file
    item_pearson_sim_source = None
    
    #item-based Pearson correlation similarity matrix dataframe
    item_pearson_sim_df = None
    
    
    #USER-BASED INSTANCE VARIABLES
    #user-based utility matrix source file
    user_utility_source = None
    
    #user-based utility dataframe
    user_utility_df = None
    
    #user-based cosine similarity matrix source file
    user_cos_sim_source = None
    
    #user-based cosine similarity matrix dataframe
    user_cos_sim_df = None
    
    #user-based Pearson correlation similarity matrix source file
    user_pearson_sim_source = None
    
    #user-based Pearson correlation similarity matrix dataframe
    user_pearson_sim_df = None
    
    
    
    
    #CONSTRUCTOR
    def __init__(self, name):
        self.name = name
        
        
        
        
    #METHODS
    
    #build a dataframe from the source csv file
    def build_df(self):
        #if no source file for the dataset has been specified:
        if self.source is None:
            print('build_df Error: Dataset Needs Source File; set Dataset.source = \'filename\'')
        else:
            df = pd.read_csv(self.source, sep='\t', names=['user', 'movie', 'rating', 'timestamp'])
            #remove timestamp -- not needed
            del df['timestamp']
            self.df = df
    
    #ITEM-BASED METHODS
    
    #builds item-based utility matrix for data file at specified filename
    #results in an item-based utility matrix with columns denoted '1', '2', '3' (strings) and rows 1, 2, 3 (integers)
    def build_item_utility(self, dest_filename):
        if self.item_utility_source is None:
            if self.df is None:
                self.build_df()
            self.item_utility_df = self.df.pivot_table(index='user', columns='movie', values='rating')
            print(self.item_utility_df)
            self.item_utility_df.to_csv(dest_filename)
            self.item_utility_source = dest_filename
        elif self.item_utility_df is None:
            self.build_item_utility_df()
    
    def build_item_utility_df(self):
        if self.item_utility_source is None:
            print('build_item_utility_df Error: build a utility matrix source csv file first')
        else:
            self.item_utility_df = pd.read_csv(self.item_utility_source, index_col = 0)
    
    #build item-based similarity matrix using Pandas Corrwith function (test purposes only)
    def build_item_pearson_sim_corrwith(self, dest_filename):
        #NEED TO IMPLEMENT CODE THAT MAKES IT WORK EVEN IF UTILITY NOT BUILT, etc.
        
        #if utility matrix not built yet
        if self.item_utility_df is None:
            print('build_item_pearson_sim Error: Utility matrix must be built first')
            
        else:            
            #create first column/dataframe
            row = self.item_utility_df.corrwith(self.item_utility_df['1']) #may need to make string
            similarity = pd.DataFrame(row, columns=[1]) #may need to make string
            
            for i in range(2, len(self.item_utility_df.columns)):
                if i % 10 == 0:
                    print('Correlating item ' + str(i) + '...')
                similarity[i] = self.item_utility_df.corrwith(self.item_utility_df[str(i)])
            print(similarity)
            self.item_pearson_sim_df = similarity
            similarity.to_csv(dest_filename)
            self.item_pearson_sim_source = dest_filename
            
    def build_item_pearson_sim(self, dest_filename):
        #NEED TO IMPLEMENT CODE THAT MAKES IT WORK EVEN IF UTILITY NOT BUILT, etc.
        
        #if utility matrix not built yet
        if self.item_utility_df is None:
            print('build_item_pearson_sim Error: Utility matrix must be built first')           
        else:
            utility_np = self.item_utility_df.to_numpy()
            similarity_np = np.zeros((len(utility_np[0]), len(utility_np[0])), dtype=float) 
            #ITERATE OVER DATA
            for i in range(len(similarity_np)):
                print("Item " + str(i))
                for j in range(len(similarity_np[i])):
                    if similarity_np[j][i] != 0:
                        similarity_np[i][j] = similarity_np[j][i]
                    else:
                        similarity_np[i][j] = pearson_corr(utility_np[:, i], utility_np[:, j])
            
            #EXPORT COMPLETED SIMILARITY MATRIX
            similarity = pd.DataFrame(similarity_np, index = self.item_utility_df.columns, columns = self.item_utility_df.columns)
            similarity.to_csv(dest_filename)
            self.item_pearson_sim_source = dest_filename
            self.item_pearson_sim_df = similarity
            
            print("Item-Based Pearson")
            print(similarity)
            
    def build_item_pearson_sim_df(self):
        if self.item_pearson_sim_source is None:
            print('build_item_pearson_sim_df Error: build an item-based Pearson correlation source csv file first with build_item_pearson_sim')
        else:
            self.item_pearson_sim_df = pd.read_csv(self.item_pearson_sim_source, index_col = 0)

    def build_user_pearson_sim(self, dest_filename):     
        #if utility matrix not built yet
        if self.item_utility_df is None:
            print('build_item_pearson_sim Error: Utility matrix must be built first')           
        else:
            self.user_utility_df = self.item_utility_df.transpose()
            utility_np = self.user_utility_df.to_numpy()
            similarity_np = np.zeros((len(utility_np[0]), len(utility_np[0])), dtype=float) 
            #ITERATE OVER DATA
            for i in range(len(similarity_np)):
                print("User " + str(i))
                for j in range(len(similarity_np[i])):
                    if similarity_np[j][i] != 0:
                        similarity_np[i][j] = similarity_np[j][i]
                    else:
                        similarity_np[i][j] = pearson_corr(utility_np[:, i], utility_np[:, j])
            
            #EXPORT COMPLETED SIMILARITY MATRIX
            similarity = pd.DataFrame(similarity_np, index = self.user_utility_df.columns, columns = self.user_utility_df.columns)
            similarity.to_csv(dest_filename)
            self.user_pearson_sim_source = dest_filename
            self.user_pearson_sim_df = similarity
            
            print("User-Based Pearson")
            print(similarity)
            
    def build_user_pearson_sim_df(self):
        if self.user_pearson_sim_source is None:
            print('build_user_pearson_sim_df Error: build a user-based Pearson correlation source csv file first with build_user_pearson_sim')
        else:
            self.user_pearson_sim_df = pd.read_csv(self.user_pearson_sim_source, index_col = 0)

#Class for training/test set pairs
#TestSet subclass inherits from Dataset superclass
class TestSet(Dataset):
    user_item_pairs_df = None
    predictions_df = None
    error_df = None
    
    #CONSTRUCTOR
    def __init__(self, name):
        #Calling superclass constructor
        Dataset.__init__(self, name)
    
    def build_df(self):
        self.df = pd.read_csv(self.source, sep='\t', header=None) #formerly had headers=None
        self.df.columns = ['user', 'item', 'observed', 'timestamp']
        del self.df['timestamp']
        print(self.df)
    
    def build_user_item_pairs_df(self):
        self.user_item_pairs_df = pd.read_csv(self.source, sep='\t', header=None)
        self.user_item_pairs_df.columns = ['user', 'item', 'observed', 'timestamp']
        del self.user_item_pairs_df['observed']
        del self.user_item_pairs_df['timestamp']
        print(self.user_item_pairs_df)
        
    
    #takes a CSV
    def build_predictions_df(self, csv=None, predictions=None):
        if csv is not None:
            self.predictions_df = pd.read_csv(csv, index_col=0)
            self.predictions_df['observed'] = self.df['observed']
        elif predictions is not None:
            self.predictions_df = self.df
            self.predictions_df['prediction'] = predictions
            print(self.predictions_df)
        else:
            print("No source data to build predictions dataframe")
        
    
    def build_error_df(self):
        self.error_df = pd.DataFrame(self.predictions_df)
        self.predictions_df['error'] = (self.predictions_df['observed rating'] - self.predictions_df['prediction']).abs()
    
    def save_test_results(self, dest_filename):
        self.predictions_df.to_csv(dest_filename)
    #def predict(self): exports the user_item_pairs to a predictor which makes a prediction; returns/appends predictions
    
    #def calculate_error(self): adds error column

#this class is to bundle together a training set and a test set
class TrainingAndTest:
    name = None
    algorithm = None
    training = None
    test = None
    
    #CONSTRUCTOR
    def __init__(self, name):
        self.name = name
        self.training = Dataset(self.name + ' training set')
        self.test = TestSet(self.name + ' test set')
    
#CORRELATION/DISTANCE FUNCTIONS
#PEARSON CORRELATION FUNCTION
        
#Pearson correlation (takes two numpy arrays (columns))        
def pearson_corr(col1, col2):
    #Finds corated values by checking each element of each array for non-NaN status and performing AND on the results
    col1_rated = np.logical_not(np.isnan(col1))
    #print(col1_rated[0:25])
    col2_rated = np.logical_not(np.isnan(col2))
    #print(col2_rated[0:25])
    corated = np.logical_and(col1_rated, col2_rated)
    #print(corated[0:25])
    #print(col1_rated[0:25])
    
    #if there are no corated values, return 0 to save time
    if np.sum(corated) == 0: #this is a sum of True values (each True == 1)
        return 0
    
    sum_product_distances_from_mean = 0
    sum_squared_col1_distances_from_mean = 0
    sum_squared_col2_distances_from_mean = 0
    #get mean values of columns before removing non-corated user ratings
    col1_mean = np.nanmean(col1) #mean excluding nans
    col2_mean = np.nanmean(col2)
    
    for i in range(0, len(col1)):

        if corated[i]:
            #numerator of formula
            col1_distance_from_mean = col1[i] - col1_mean
            col2_distance_from_mean = col2[i] - col2_mean
            sum_product_distances_from_mean += col1_distance_from_mean * col2_distance_from_mean
            #denominator of formula
            sum_squared_col1_distances_from_mean += (col1[i] - col1_mean) ** 2
            sum_squared_col2_distances_from_mean += (col2[i] - col2_mean) ** 2
        
    corr = sum_product_distances_from_mean / ((math.sqrt(sum_squared_col1_distances_from_mean) * math.sqrt(sum_squared_col2_distances_from_mean)) + 0.0000001)
    return corr
        
        
   
#DATASET LOADING FUNCTIONS
#format: load_<dataset name>

#load MovieLens datasets
        
    #MovieLens 100k main source file
def load_ml_100k():
    ml_100k = Dataset("MovieLens 100k main file")
    ml_100k.algorithm = 'neighborhood-based collaborative filtering'
    ml_100k.source = 'datasets/ml-100k/u.data'
    ml_100k.build_df() #build dataframe from the source
    ml_100k.item_utility_source = 'datasets/ml-100k/utility-matrix/ml_100k_item_utility.csv'
    #ml_100k.build_item_utility('datasets/ml-100k/utility-matrix/ml_100k_item_utility.csv') #build item-based utility matrix dataframe
    ml_100k.build_item_utility_df()
    ml_100k.item_pearson_sim_source = 'item_similarity/ml_100k_item_pearson_sim.csv'
    #ml_100k.build_item_pearson_sim('item_similarity/ml_100k_item_pearson_sim.csv')
    ml_100k.build_item_pearson_sim_df() #build item-based utility matrix dataframe
    #returns Dataset object to calling function
    return ml_100k


    #MovieLens 100k u1 test/training set
def load_ml_u1():
    ml_u1 = TrainingAndTest("MovieLens u1 training/test sets")
    ml_u1.algorithm = 'item-based neighborhood-based collaborative filtering'
    ml_u1.training.source = 'datasets/ml-100k/u1.base'
    ml_u1.training.build_df()
    ml_u1.training.item_utility_source = 'datasets/ml-100k/utility-matrix/ml_u1_item_utility.csv'
    ml_u1.training.build_item_utility_df()
    ml_u1.training.item_pearson_sim_source = 'item_similarity/ml_u1_item_pearson_sim.csv'
    #ml_u1.training.build_item_pearson_sim('item_similarity/ml_u1_item_pearson_sim.csv')
    ml_u1.training.build_item_pearson_sim_df()
    #print(ml_u1.training.item_utility_df)
    #print(ml_u1.training.item_pearson_sim_df)
    ml_u1.test.source = 'datasets/ml-100k/u1.test'
    ml_u1.test.build_df()
    ml_u1.test.build_user_item_pairs_df()
    ml_u1.test.build_predictions_df(csv='item_similarity/ml_u1_2019_06_24_test_results.csv')
    #print(ml_u1.test.df)
    return ml_u1
    
def load_yelp_stut():
    yelp_stut = Dataset("Yelp Stuttgart, Germany Reviews")
    yelp_stut.item_utility_source = 'datasets/yelp_dataset/utility-matrix/yelp_utility_matrix_stuttgart.csv'
    yelp_stut.build_item_utility_df()
    yelp_stut.item_pearson_sim_source = 'item_similarity/yelp_stut_item_pearson_sim.csv'
    yelp_stut.build_user_pearson_sim('user_similarity/yelp_stut_user_pearson_sim.csv')
    print(yelp_stut.user_pearson_sim_df)
    
def main():
    load_ml_u1()

    
if __name__ == '__main__':
    main()
    
        
        
        



