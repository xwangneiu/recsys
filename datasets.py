# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 18:38:50 2019

@author: jonathan
"""

'''
Dataset Class
I created this class because each dataset can be represented as an object.
Each dataset has a source csv file,
and will have a utility matrix and a similarity matrix.
Objects are an easy way to bundle them together.
'''
import numpy as np
import pandas as pd
import math

class Dataset:
    #INSTANCE VARIABLES
    #text description of dataset
    name = None
    
    #item-based, user-based, WNMF
    algorithm = None
    
    #raw data file/CSV
    source = None
    
    #pandas dataframe from source, if it exists
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
    def build_item_utility(self, dest_filename):
        if self.item_utility_source is None:
            if self.df is None:
                self.build_df()
            self.item_utility_df = self.df.pivot_table(index='user', columns='movie', values='rating')
            print(self.item_utility_df)
            self.item_utility_df = self.item_utility_df.set_index(self.item_utility_df.user)
            self.item_utility_df.to_csv(dest_filename)
            self.item_utility_source = dest_filename
        elif self.item_utility_df is None:
            self.item_utility_df = pd.read_csv(self.item_utility_source)
    
    #build item-based similarity matrix using Pearson correlation
    def build_item_pearson_sim(self, dest_filename):
        #NEED TO IMPLEMENT CODE THAT MAKES IT WORK EVEN IF UTILITY NOT BUILT, etc.
        output_series = []
        if self.item_utility_df is None:
            print('build_item_pearson_sim Error: Utility matrix must be built first')
        else:
            input_df = self.item_utility_df
            for column_i in input_df:
                print('Correlating column ' + str(column_i))
                pearson_corr_list = []
                for column_j in input_df:
                    corated_i = (input_df[column_j] / input_df[column_j]) * input_df[column_i]
                    corated_j = (input_df[column_i] / input_df[column_i]) * input_df[column_j]
        
                    mean_i = corated_i.mean()
                    mean_j = corated_j.mean()
        
                    calculated_i = corated_i - mean_i
                    calculated_j = corated_j - mean_j
        
                    numerator = (calculated_i*calculated_j).sum()
                    denumerator = math.sqrt((calculated_i * calculated_i).sum()) * math.sqrt((calculated_j * calculated_j).sum())
        
                    pearson_corr = numerator / denumerator
        
                    pearson_corr_list.append(pearson_corr)
                output_series.append(pd.Series(pearson_corr_list))
            output_df = pd.concat(output_series, axis = 1)
            output_df.index = input_df.columns
            output_df.columns = input_df.columns
            self.item_pearson_sim_df = output_df
            output_df.to_csv(dest_filename)
    

#Class for MovieLens test/training set pairs
class TrainingAndTest(Dataset):
    name = None
    algorithm = None
    training = None
    test = None
    
    def __init__(self, name):
        self.name = name
        self.set_training()
        self.set_test()
        
    def set_training(self):
        self.training = Dataset(self.name + ' training set')
    
    def set_test(self):
        self.test = Dataset(self.name + ' test set')
    
    
#load MovieLens datasets
def load_ml_datasets():
    #MovieLens 100k main source file
    ml_100k = Dataset("MovieLens 100k main file")
    ml_100k.algorithm = 'neighborhood-based collaborative filtering'
    ml_100k.source = 'datasets/ml-100k/u.data'
    ml_100k.build_df() #build dataframe from the source
    #ml_100k.item_utility_source = 'datasets/ml-100k/utility-matrix/ml_100k_item_utility.csv'
    ml_100k.build_item_utility('datasets/ml-100k/utility-matrix/ml_100k_item_utility.csv') #import item-based utility matrix csv
    #ml_100k.build_item_pearson_sim('item_similarity/ml_100k_item_pearson_sim.csv')


    #ml_100k.build_item_similarity
    
    #MovieLens 100k u1 test/training set
    ml_u1 = TrainingAndTest("MovieLens u1 training/test sets")
    ml_u1.algorithm = 'item-based neighborhood-based collaborative filtering'
    ml_u1.training.source = 'datasets/ml-100k/u1.base'
    ml_u1.training.build_df()
    #ml_u1.training.item_utility_source = 'datasets/ml-100k/utility-matrix/ml_u1_item_utility.csv'
    ml_u1.training.build_item_utility('datasets/ml-100k/utility-matrix/ml_u1_item_utility.csv')
    #ml_u1.training.build_item_pearson_sim('item_similarity/ml_100k_item_pearson_sim.csv')
    
def main():
    load_ml_datasets()
    
if __name__ == '__main__':
    main()
    
        
        
        



