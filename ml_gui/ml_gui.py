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


def load_film_data():
    print('nothing here yet')
    #pre-produce json containing film names: ids as dictionary
    #load said file
    #convert film names to a list
    #return list of film names
    
#new_user_ratings should be pandas dataframe with user id, item id, observed value, and UNIX epoch seconds only timestamp
def get_rec(new_user_ratings):
    print('nothing here yet')
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
        
    def record_recommend():
        for i in range(len(rating_values)):
            user_ratings[i][1] = movie_dict[dropdown_values[i].get()]
            user_ratings[i][2] = rating_values[i].get()
        print(user_ratings)
            
    
    record_and_recommend = tk.Button(root, text="Recommend Movies", width=30, height=5, bg="brown", command=record_recommend).pack()
        
    '''
    def get_dropdown_0():
        user_ratings[0][1] = movie_dict[dropdown_0_value.get()]
    dropdown_0 = tkentrycomplete.AutocompleteCombobox(textvariable=dropdown_0_value)
    dropdown_0.set_completion_list(titles)
    dropdown_0.place(x=200, y=400)
    rating_0 = tk.IntVar()
    rating_0.set(3)
    def get_rating_0():
        user_ratings[0][2] = rating_0.get()
    for i in range(len(star_ratings)):
        tk.Radiobutton(root, 
                       text=star_ratings[i],
                       padx=20,
                       variable=rating_0,
                       command=get_rating_0,
                       value=star_ratings[i]).pack(anchor=tk.W)
    def record_ratings():
        user_ratings[0][1] = movie_dict[dropdown_0_value.get()]
        
        print(user_ratings)
    record_button = tk.Button(text='Record Ratings', command=record_ratings)
    record_button.place(x=200, y=450)
    #5 dropdown menus with films to rate (autocomplete), then 
    #Autocomplete: https://stackoverflow.com/questions/55649709/is-autocomplete-search-feature-available-in-tkinter-combo-box
    #Radio buttons: https://www.python-course.eu/tkinter_radiobuttons.php
    #Keep adding ratings until 
    '''
    root.mainloop()
    
def main():
    run_gui_app()
if __name__ == '__main__':
    main()