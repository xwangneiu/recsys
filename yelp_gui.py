# SCSE RecSys Group
# Minh N.
# 2019.07.22
# This module creates a interactable GUI with the Yelp dataset using WNMF.
# It creates a window where users can input ratings for businesses and receive recommendations.

from tkinter import *
from tkinter.ttk import *
from libraries import tkentrycomplete
import json

class App(Frame):
	def __init__(self, master = None):
		super().__init__(master)
		self.grid(row = 0, column = 0)

def submitForm(string = 'Hello'):
	print(string)

root = Tk()

app = App(root)
b1 = Button(app, text = 'packed', command = submitForm)
b1.pack()
app.grid(row = 0, column = 0)

selection = App(root)
selection.grid(row = 1)
s_entry = tkentrycomplete.AutocompleteCombobox(selection)
s_entry.set_completion_list(['test', 'test2','hello','goodbye','gggg','gg1'])
s_entry.pack()

with open('datasets/yelp_dataset/yelp_business_by_category_uc.json', 'r') as f:
	b_dict = json.load(f)
c_names = [x for x in b_dict.keys()]

c_var = StringVar()
c_var.set(c_names[0])
categories = App(root)
categories.grid(row = 1, column = 1)
c_menu = OptionMenu(categories, c_var, *c_names)
c_menu.pack()
c_var.trace('w', callback = lambda *args : s_entry.set_completion_list(b_dict[c_var.get()]))



# Select from a list of categories
# > Gets selection
# use a pregenerated map which has: keys == categories, values == list of businesses that are in the cateogry
# Update displayed list to businesses in the category from dict

# to do, have an illustration of what the gui will look like


root.mainloop()