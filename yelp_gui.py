# SCSE RecSys Group
# Minh N.
# 2019.07.22
# This module creates a interactable GUI with the Yelp dataset using WNMF.
# It creates a window where users can input ratings for businesses and receive recommendations.

from tkinter import *
from tkinter.ttk import *
from libraries import tkentrycomplete
import json
import re

class App(Frame):
	def __init__(self, master = None):
		super().__init__(master)
		self.grid(row = 0, column = 0)

with open('yelp_business_uc_id.json', 'r') as f:
	business_id = json.load(f)

with open('datasets/yelp_dataset/yelp_name_by_category_uc.json', 'r') as f:
	b_dict = json.load(f)
c_names = [x for x in b_dict.keys()]
b_names = {x for i in b_dict.values() for x in i}

review_dict = {}

def generate_rec():
	if len(review_dict) < 5:
		# Throw error here
		print('not enough reviews')
	else:
		for x, y in review_dict.items()
			 int(re.sub(r"\D", "", x))
		print('generating reviews now')

def submit_form(business, rating, ur_var):
	if(not business in review_dict.keys() and business in b_names):
		review_dict[business] = rating
		print(review_dict)
		z = ur_var.get()
		z = z + business + ' ' + str(rating) + '\n'
		ur_var.set(z)
		generate_rec()
	else:
		# throw error here
		print('false')

# All app creation below

root = Tk()

# This widget allows users to type up and enter a business

selection = App(root)
selection.grid(row = 0, column = 0)
s_entry = tkentrycomplete.AutocompleteCombobox(selection)
s_entry.pack()

s_entry.set_completion_list(b_dict[c_names[0]])

# This widget is for users to select a categories

categories = App(root)
categories.grid(row = 0, column = 1)
c_var = StringVar(root)
c_var.trace('w', callback = lambda *args : s_entry.set_completion_list(b_dict[c_var.get()]))
c_var.set(c_names[0])
c_menu = OptionMenu(categories, c_var, c_names[0], *c_names)
c_menu.pack()

# This widget is for users to select a rating

r_var = IntVar()
review = App(root)
review.grid(row = 0, column = 2)
r_menu = OptionMenu(review, r_var, 1, *[1, 2, 3, 4, 5])
r_menu.pack()

# This widget displays the user's reviews

ur_var = StringVar()
user_reviews = App(root)
user_reviews.grid(row = 1, column = 0)
ur_text = Label(user_reviews, textvariable=ur_var)
ur_text.pack()

# This widget allows users to enter their rating

e_button = App(root)
e_button.grid(row = 0, column = 3)
e1 = Button(e_button, text = 'click me', command = lambda *args : submit_form(s_entry.get(), r_var.get(), ur_var))
e1.pack()

# TO DO
# Display submitted reviews to new widget
# Once there is enough reviews, allow the user to request recommendations

root.mainloop()