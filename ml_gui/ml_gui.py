# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 13:57:53 2019

@author: jonathan
"""
import tkinter as tk
def load_film_data():
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
    root = tk.Tk()
    root.title("New Application")
    root.geometry("640x640+0+0")
    
    heading = tk.Label(root, text="Recommender System", font=("arial", 40, "bold"), fg="steelblue").pack()
    
    label1 = tk.Label(root, text="Enter your name: ", font=("arial", 20, "bold"), fg="black").place(x=10, y=200)
    
    name = tk.StringVar()
    entry_box = tk.Entry(root, textvariable=name, width=25, bg="lightgreen").place(x=280, y=210)
    
    def do_it():
        print("Hello "+ name.get())
    
    work = tk.Button(root, text="Enter", width=30, height=5, bg="lightblue", command=do_it).place(x=250, y=300)
    
    #5 dropdown menus with films to rate (autocomplete), then 
    #Autocomplete: https://stackoverflow.com/questions/55649709/is-autocomplete-search-feature-available-in-tkinter-combo-box
    #Radio buttons: https://www.python-course.eu/tkinter_radiobuttons.php
    root.mainloop()
    
def main():
    run_gui_app()
if __name__ == '__main__':
    main()