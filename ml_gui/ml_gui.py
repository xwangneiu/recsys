# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 13:57:53 2019

@author: jonathan
"""
import sys
sys.path.insert(0, '../datasets/ml-100k/')
sys.path.insert(0, '../')
import tkinter as tk
from libraries import tkentrycomplete
import movie_titles
import pandas as pd
import numpy as np
from shutil import copyfile
import os

def load_film_data():
    print('nothing here yet')
    
    #pre-produce json containing film names: ids as dictionary
    #load said file
    #convert film names to a list
    #return list of film names
    
#new_user_ratings should be pandas dataframe with user id, item id, observed value, and UNIX epoch seconds only timestamp
def get_rec(user_ratings):
    file_with_user_ratings = '../datasets/ml-100k/gui_og.csv'
    copyfile('../datasets/ml-100k/u1.base', file_with_user_ratings)
    f = open(file_with_user_ratings, 'a')
    ratings_to_write = str(user_ratings).replace('],', '\n').replace('[', '').replace()
    
    print(ratings_to_write)
    #append user ratings to u.base
    #load as new dataset with new user ratings
    #get user prediction for ALL films (predict on pairs that consist of the active user and all items)
    #sort by predicted rating (there will be many 5s), and then by popularity or maybe do not cap ratings at 5 anymore in predictor
    #return top rated 5 as a list
    
def run_gui_app():
    
    #get ID->title / title->ID dictionary and movie titles list
    movie_dict, titles = movie_titles.get_movie_info()
    root = tk.Tk()
    root.title('FILM RECOMMENDER')
    root.geometry("640x640+0+0")
    
    heading = tk.Label(root, text="FILM RECOMMENDER", font=("copperplate gothic", 30, "bold"), fg="steelblue").pack()
    headers_frame = tk.Frame(root, height=100, width=640).pack()
    movies_title = tk.Label(text="-- Pick movies (start typing to see what's available) ", font=("arial", 16, "bold"), fg="black", justify='left').pack()
    ratings_title = tk.Label(text="-- Rate them 1-5 stars", font=("arial", 16, "bold"), fg="black", wraplength=320, justify='left').pack()
    '''
    name = tk.StringVar()
    entry_box = tk.Entry(root, textvariable=name, width=25, bg="lightgreen").place(x=280, y=210)
    
    def do_it():
        print("Hello "+ name.get())
    
    work = tk.Button(root, text="Enter", width=30, height=5, bg="lightblue", command=do_it).place(x=250, y=300)
    '''
    #get user ratings
    
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
    '''
    def set_radio(i):
        user_ratings[i][2] = rating_values[i].get()
    '''
        
    radios = []
    curr_movie_id = 0
    x_loc = 200
    y_loc = 200
    for i in range(len(star_ratings)):
        frames.append(tk.Frame(root, height=50, width=640))
        frames[i].pack()
        #combo box
        dropdown_values.append(tk.StringVar())
        dropdowns.append(tkentrycomplete.AutocompleteCombobox(textvariable=dropdown_values[i], width=40))
        dropdowns[i].set_completion_list(titles)
        dropdowns[i].pack(in_=frames[i], side='left')
        
        #radios
        for j in range(len(star_ratings)):
            radios.append(tk.Radiobutton(root, 
                       text=star_ratings[j],
                       padx=20,
                       variable=rating_values[i],
                       #command=lambda: set_radio(i),
                       value=star_ratings[j]).pack(in_=frames[i], side='left'))
        
    duplicate_entry = tk.Label(root, text="You may only rate the same movie once")
    missing_movie = tk.Label(root, text="You forgot to select 5 movies to rate")
    missing_rating = tk.Label(root, text="Please rate all 5 movies")
    
    def record_recommend():
        movies_rated = {}
        duplicate_entry.pack_forget()
        missing_movie.pack_forget()
        missing_rating.pack_forget()
        validated = False
        for i in range(len(rating_values)):
            try:
                movie_id = movie_dict[dropdown_values[i].get()]
                #if there is a duplicate
                if movie_id in movies_rated:
                    duplicate_entry.pack()
                    break
                else:
                    user_ratings[i][1] = movie_id
                    movies_rated[movie_id] = True
                    user_ratings[i][2] = rating_values[i].get()
                    #if user forgot to rate one of the movies
                    if user_ratings[i][2] == 0:
                        missing_rating.pack()
                        break
                    if i == len(rating_values) - 1:
                        validated = True
            #if user did not select 5 movies
            except KeyError:
                missing_movie.pack()
        print(validated)
        if validated:
            #make function that adds a row to the csv from an element in rating_values
            get_rec(user_ratings)
            
                
            
            
    
    record_and_recommend = tk.Button(root, text="Recommend Movies", width=30, height=5, bg="brown", command=record_recommend).pack()
    
    #validate results
    #if validated:
    
    root.mainloop()
    
def main():
    run_gui_app()
if __name__ == '__main__':
    main()