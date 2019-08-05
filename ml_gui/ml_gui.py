# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 13:57:53 2019

@author: jonathan
"""
import sys
sys.path.insert(0, '../datasets/ml-100k/')
sys.path.insert(0, '../')
import datasets
import tkinter as tk
from libraries import tkentrycomplete
import movie_titles
import pandas as pd
import numpy as np
import time
from shutil import copyfile
import os
import math

def load_film_data():
    print('nothing here yet')
    
    #pre-produce json containing film names: ids as dictionary
    #load said file
    #convert film names to a list
    #return list of film names
    
#new_user_ratings should be pandas dataframe with user id, item id, observed value, and UNIX epoch seconds only timestamp  
def top_k_recommendation(file_with_user_ratings, test_og_df, k):
    name = 'ml_gui'
    data_utility_dir = '../datasets/ml-100k/utility-matrix/'
    results_folder = '../wnmf/'
    ds = datasets.TrainingAndTest('ml_gui')
    ds.training = datasets.Dataset(
        'ml_gui',                            #name
        file_with_user_ratings,                                      #original source
        data_utility_dir + name + '_um.csv',            #utility matrix
        results_folder + name + '_',            #similarity matrix
        'ml',                                             #data source
        'wnmf',                                             #algorithm
        'wnmf',
        2, #latent factors
        26) #iterations
    #get 
    ds.test = datasets.TestSet(
        str(name) + ' test set',                                          #name
        'gui_user_test.csv', 'ml')
    ds.build_ml_wnmf_predictions_df(results_folder + str(name) + '_wnmf_predictions.csv', cap=False)
    predictions = ds.test.predictions_df.copy()
    recommendations = predictions.sort_values('prediction', ascending=False).head(k)   
    recommendations = list(recommendations['item'])
    movie_dict, titles = movie_titles.get_movie_info()
    recommendations = [movie_dict[i] for i in recommendations]

    #delete source files to ensure not reused
    os.remove('../wnmf/ml_gui__u.csv')
    os.remove('../wnmf/ml_gui__v.csv')
    os.remove('../wnmf/ml_gui_wnmf_predictions.csv')
    os.remove('../datasets/ml-100k/utility-matrix/ml_gui_um.csv')
    #returns list of top 5    
    return recommendations
    
def get_rec(user_ratings, file_with_user_ratings, k):
    #TO DO: any new ratings for the active user that the active user has already rated should be dropped
    df = None
    try:
        df = pd.read_csv(file_with_user_ratings, sep='\t', names=['user', 'movie', 'rating', 'timestamp'])
    except FileNotFoundError:
        copyfile('../datasets/ml-100k/u.data', file_with_user_ratings)
        df = pd.read_csv(file_with_user_ratings, sep='\t', names=['user', 'movie', 'rating', 'timestamp'])
    df = pd.read_csv(file_with_user_ratings, sep='\t', names=['user', 'movie', 'rating', 'timestamp'])
    
    ratings_to_write = pd.DataFrame(user_ratings, columns=['user', 'movie', 'rating'])
    ratings_to_write['timestamp'] = float(int(time.time()))
    df = df.append(ratings_to_write)
    df.index = [i for i in range(len(df.index))]
    df.to_csv(file_with_user_ratings, sep='\t', index=False, header=None)
    

    top_movies = df.copy()
    by_ratings = top_movies.groupby('movie')['rating'].count()
    
    movie_ratings = pd.DataFrame(by_ratings).sort_values('rating', ascending=False)
    movie_ratings = movie_ratings[movie_ratings['rating'] > 50]
    movies_to_predict = movie_ratings.index.to_numpy()
    
    user_item_pairs = pd.DataFrame([2000 for i in range(len(movies_to_predict))], columns=['user'])
    user_item_pairs['movie'] = pd.Series(movies_to_predict)

    test_og_df = user_item_pairs.copy()
    test_og_df['rating'] = math.nan
    test_og_df['timestamp'] = 999999999
    test_og_df.to_csv('gui_user_test.csv', sep='\t', index=False, header=None)
    return top_k_recommendation(file_with_user_ratings, test_og_df, k)

def run_gui_app():
    
    #get ID->title / title->ID dictionary and movie titles list
    movie_dict, titles = movie_titles.get_movie_info()
    root = tk.Tk()
    root.title('MOVIE RECOMMENDER')
    root.geometry("720x720+0+0")
    #color and font scheme
    background = 'gray6'
    main_font = 'calibri'
    main_font_size = 12
    main_font_weight = ''
    main_font_color = 'gray45'
    button_color = background
    
    root['bg'] = background
    heading = tk.Label(root, text="MOVIE RECOMMENDER", font=("fixedsys", 30), fg=main_font_color, bg=background).pack()
    headers = tk.Frame(root, height=200, width=720, bg=background)
    headers_subframe_1 = tk.Frame(root, height=200, width=360, bg=background)
    headers_subframe_2 = tk.Frame(root, height=200, width=360, bg=background)
    movies_title = tk.Label(text="Select Movies", font=(main_font, 16, "italic"), fg=main_font_color, bg=background, anchor="w" 
                            ).pack(in_=headers_subframe_1, side='left')
    ratings_title = tk.Label(text="Rate Movies (5 is highest)", font=(main_font, 16, "italic"), fg=main_font_color, bg=background, justify="left").pack(in_=headers_subframe_2, side='left')
    headers_subframe_1.pack(in_=headers, side='left')
    headers_subframe_2.pack(in_=headers, side='left')
    headers.pack()
    #get user ratings
    file_with_user_ratings = '../datasets/ml-100k/gui_og.csv'
    user_ratings = [
            [2000, 2000, 0],
            [2000, 2000, 0],
            [2000, 2000, 0],
            [2000, 2000, 0],
            [2000, 2000, 0]]
    
    star_ratings = [1, 2, 3, 4, 5]
    frames = []
    dropdown_values = []
    dropdowns = []
    rating_values = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
       
    radios = []
    curr_movie_id = 0
    x_loc = 200
    y_loc = 200
    for i in range(len(star_ratings)):
        frames.append(tk.Frame(root, height=50, width=640, bg=background))
        frames[i].pack()
        #combo box
        dropdown_values.append(tk.StringVar())
        dropdowns.append(tkentrycomplete.AutocompleteCombobox(textvariable=dropdown_values[i], font=(main_font, main_font_size, main_font_weight), width=40))
        dropdowns[i].set_completion_list(titles)
        dropdowns[i].pack(in_=frames[i], side='left')
        
        #radios
        for j in range(len(star_ratings)):
            radios.append(tk.Radiobutton(root, 
                       text=str(star_ratings[j]) + ' ★',
                       font=(main_font, 16, "bold"),
                       fg=main_font_color, 
                       bg=background,
                       indicatoron=False,
                       padx=10,
                       variable=rating_values[i],
                       #command=lambda: set_radio(i),
                       value=star_ratings[j]).pack(in_=frames[i], side='left'))
        
    duplicate_entry = "You may only rate the same movie once"
    missing_movie = "Please select 5 movies to rate"
    missing_rating = "Please rate all 5 movies"
    invalid_user_input = tk.Label(text="", height=0, fg=main_font_color, font=(main_font, main_font_size, main_font_weight), bg=background)
    movies_rated = {}
    top_k_recommendations = []
    def rec_list_to_string(top_k_recommendations):
        result = ''
        for i in range(len(top_k_recommendations)):
            result += str(i + 1) + '.  ' + top_k_recommendations[i] + '\n'
        return result
    
    def record_recommend():
        movies_this_round = {}
        invalid_user_input.config(text="", height=0)
        validated = False
        for i in range(len(rating_values)):
            try:
                movie_id = movie_dict[dropdown_values[i].get()]
                #if there is a duplicate
                if movie_id in movies_rated:
                    invalid_user_input.config(text=duplicate_entry, height=3)
                    break
                elif movie_id in movies_this_round:
                    invalid_user_input.config(text=duplicate_entry, height=3)
                    break
                else:
                    user_ratings[i][1] = movie_id
                    movies_this_round[movie_id] = True
                    user_ratings[i][2] = rating_values[i].get()
                    #if user forgot to rate one of the movies
                    if user_ratings[i][2] == 0:
                        invalid_user_input.config(text=missing_rating, height=3)
                        break
                    if i == len(rating_values) - 1:
                        validated = True
            #if user did not select 5 movies
            except KeyError:
                invalid_user_input.config(text=missing_movie, height=3)
        if validated:
            print("Form submitted is valid; proceeding with recommendation");
            #make function that adds a row to the csv from an element in rating_values
            invalid_user_input.config(text="", height=0)
            top_k_recommendations = get_rec(user_ratings, file_with_user_ratings, 5)
            for j in range(len(user_ratings)):
                movies_rated[user_ratings[j][1]] = True
            recommendation_list.config(text=rec_list_to_string(top_k_recommendations), height=6)
        else:
            print("Form submitted is invalid; user must correct before recommendation")

                
    invalid_user_input.pack()
    recommendation_list = tk.Label(text="", height=0, bg=background, justify='left', fg=main_font_color, font=(main_font, "16", main_font_weight))
    record_and_recommend = tk.Button(root, text="Recommend Movies", width=30, height=3, fg=main_font_color, bg=button_color, command=record_recommend, font=(main_font, main_font_size, main_font_weight)).pack()
    recommendation_list.pack()
     
    def clean_up():
        invalid_user_input.config(text="", height=0)
        print("movies rated: " + str(movies_rated))
        try:
            os.remove(file_with_user_ratings)
        except FileNotFoundError:
            print('no file to remove')
        movies_rated_keys = list(movies_rated.keys())
        for key in movies_rated_keys:
            del movies_rated[key]
        recommendation_list.config(text="", height=0)
            
    def end_program():
        clean_up()
        root.destroy()
    new_session_button = tk.Button(root, text="Start New Session", width=30, height=3, fg=main_font_color, bg=button_color, command=clean_up, font=(main_font, main_font_size, main_font_weight)).pack()
    quit_button = tk.Button(root, text="Quit", width=30, height=3, fg=main_font_color, bg=button_color, command=end_program, font=(main_font, main_font_size, main_font_weight)).pack()
    
    #validate results
    #if validated:
    
    root.mainloop()
    
def main():
    run_gui_app()
if __name__ == '__main__':
    main()