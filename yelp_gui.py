# SCSE RecSys Group
# Minh N.
# 2019.07.22
# This module creates a interactable GUI with the Yelp dataset using WNMF.
# It creates a window where users can input ratings for businesses and receive recommendations.
# The widgets follow the scheme according to the yelp_gui_scheme.png

from tkinter import *
from tkinter.ttk import *
from libraries import tkentrycomplete
import json
import scipy
import numpy as np
from staticmap import StaticMap, CircleMarker
from PIL import Image, ImageTk 

class App(Frame):
	def __init__(self, master = None, **options):
		super().__init__(master, **options)
		self.grid(row = 0, column = 0)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)
		self.grid_rowconfigure(1, weight=1)


# These are the files necessary for  the program

# This is the Urbana-Champaign utility matrix, in dictionary format to limit sparsity
with open('datasets/yelp_dataset/yelp_utility_dictionary_uc.json', 'r') as f:
	ud = json.load(f)
# These two are dictionaries of (numeric id) : (yelp id) and (yelp id) : (numeric id)
with open('datasets/yelp_dataset/yelp_user_uc_id.json', 'r') as f:
	user_id = json.load(f)
with open('datasets/yelp_dataset/yelp_business_uc_id.json', 'r') as f:
	business_id = json.load(f)

# This is a dictionary of 'business_id' : 'name (numeric id)'
with open('datasets/yelp_dataset/yelp_businessid_to_name.json', 'r') as f:
	bid_to_name = json.load(f)

# A dictionary of (categories) : (A list of business names that are within the category)
with open('datasets/yelp_dataset/yelp_name_by_category_uc.json', 'r') as f:
	b_dict = json.load(f)

# This is used in the category widget
c_names = [x for x in b_dict.keys()]
# This is used to validate entries
b_names = {x for i in b_dict.values() for x in i}


# This is the recommender
def sort_helper(item):
	return item[1]

def wnmf(lf, it):
	try: 
		a
		# add updating a[11900]
	except NameError:
		a = np.zeros((len(user_id) // 2 + 1, len(business_id) // 2), dtype = int)
		for k, v in ud.items():
			for kk, vv in v.items():
				a[int(k), int(kk)] = int(vv)
	w = a.copy()
	wi, wj = w.nonzero()
	for i, j in zip(wi, wj):
		w[i, j] = 1
	u = np.random.random(size = (len(user_id) // 2 + 1, lf))
	v = np.random.random(size = (lf, len(business_id) // 2))
	ux, uy = u.shape
	vx, vy = v.shape
	for i in range(it):
		# for 

		vt = v.T
		u_num = np.matmul(a, vt)
		u_denom = np.matmul(np.multiply(w, np.matmul(u, v)), vt) 
		for i in range(ux):
			for j in range(uy):
				u[i][j] = u[i][j] * (u_num[i][j] / (u_denom[i][j] + 0.0000001))

		#update v
		ut = u.T
		v_num = np.matmul(ut, a)
		v_denom = np.matmul(ut, np.multiply(w, np.matmul(u, v)))
		for i in range(vx):
			for j in range(vy):
				v[i][j] = v[i][j] * (v_num[i][j] / (v_denom[i][j] + 0.0000001))
	m = np.matmul(u, v)
	# get last row
	prediction = m[-1]
	prediction = [(bid, prediction[bid]) for bid in range(prediction.size) if prediction[bid] <= 40]
	prediction.sort(reverse = True, key = sort_helper)
	return prediction[0:5]

# This method generates the recommendations when called if there are enough reviews

def generate_rec():
	if len(review_dict) < 5: # && len(review_dict) % 5 != 0
		# Throw error here
		print('not enough reviews')
	else:
		for x, y in review_dict.items():
			curr_id = x[str.find(x, '(') + 1 : str.find(x, ')')]
			if 11900 in ud:
				print('exists')
				ud[11900][curr_id] = y
			else:
				print('does not exist')
				ud[11900] = {curr_id: y}
		print(ud[11900])
		top_five_recs = wnmf(lf = 2, it = 25)
		print(top_five_recs)
		z = ''
		for i in top_five_recs:
			z = z + bid_to_name[business_id[str(i[0])]] + '\n'
		recommendation_var.set(z)

# After the user presses enter, validate entry and, if correct, add it to the list of reviews and call generate_rec()	
def submit_form(business, rating, ur_var, rating_var):
	if (not business in review_dict.keys() and business in b_names):
		review_dict[business] = rating
		print(review_dict)
		z = ur_var.get()
		z = z + business + '\n'
		user_var.set(z)
		z = rating_var.get()
		z = z + str(rating) + '\n'
		rating_var.set(z)
		generate_rec()
	else:
		# throw error here
		print(False)

def reset_reviews():
	review_dict = {}
	user_var.set('')
	recommendation_var.set('')
	rating_var.set('')


# All app creation below

root = Tk()
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

review_dict = {}

# This container and widget starts off as a blank map, and updates after WNMF
# TB

width, height, tile_size = (512, 512, 256)
m = StaticMap(width, height, tile_size = tile_size)
marker = CircleMarker((-88.2234, 40.1064), '#0036FF', 1)
m.add_marker(marker)
image = m.render(15)
photo = ImageTk.PhotoImage(image)

displaymap_image = Label(image=photo)
displaymap_image.grid(row = 0, column = 0, rowspan = 3)

# This is a widget for containing the all interactable widgets

input_container = App(root)
input_container.grid(row = 1, column = 1, columnspan = 4, sticky = 'n')

# This is a widget for containing recommendation output portion.

display_container = App(root, height = 200, borderwidth = 3, relief = 'solid')
display_container.grid(row = 0, column = 1, rowspan = 2, columnspan = 4, sticky = 'n')

# This widget resets the users score

reset = App(input_container)
reset.grid(row = 0, column = 3)
reset_button = Button(reset, text = 'Reset', command = reset_reviews)
reset_button.pack()

# This is a widget container for the labels and input boxes

input_container_sub = App(input_container)
input_container_sub.grid(row = 1, column = 0, columnspan = 4, pady = (0, 75))

# This widget, its label, and container is for users to select a categories

categories = App(input_container_sub)
categories.grid(row = 0, column = 0)
categories_label = Label(categories, text = 'Select a business category here:', justify = 'left', padding = (10, 0, 5, 0), font = ('Helvetica', 13))
categories_label.grid(row = 0, column = 0)
categories_var = StringVar(categories)
categories_var.trace('w', callback = lambda *args : selection_entry.set_completion_list(b_dict[categories_var.get()]))
categories_var.set(c_names[0])
categories_menu = OptionMenu(categories, categories_var, c_names[-2], *c_names)
categories_menu.grid(row = 1, column = 0)

# This widget, its label, and container allows users to type up and enter a business

selection = App(input_container_sub)
selection.grid(row = 0, column = 1)
selection_label = Label(selection, text = 'Search and select a business here:', justify = 'left', padding = (5, 0, 5, 0),font = ('Helvetica', 13))
selection_label.grid(row = 0, column = 0)
selection_entry = tkentrycomplete.AutocompleteCombobox(selection)
selection_entry.grid(row = 1, column = 0)
selection_entry.set_completion_list(b_dict[c_names[-2]])

# This widget is for users to select a rating

review = App(input_container_sub)
review.grid(row = 0, column = 2)
review_label = Label(review, text = 'Select a rating:', justify = 'left', padding = (5, 0, 10, 0), font = ('Helvetica', 13))
review_label.grid(row = 0, column = 0)
review_var = IntVar()
review_menu = OptionMenu(review, review_var, 1, *[1, 2, 3, 4, 5])
review_menu.grid(row = 1, column = 0)

# This widget allows users to enter their rating

enter = App(input_container_sub)
enter.grid(row = 0, column = 3)
enter_button = Button(enter, text = 'Enter Rating', command = lambda *args : submit_form(selection_entry.get(), review_var.get(), user_var, rating_var))
enter_button.grid(row = 1, column = 0)

# This widget container is for displaying the user's reviews as well as a separator

user_reviews = App(display_container)
user_reviews.grid(row = 0, column = 0, columnspan = 2, rowspan = 2, sticky = 'n')

display_separator = Separator(user_reviews, orient = VERTICAL)
display_separator.grid(row = 0, column = 2, rowspan = 2, sticky="ns")

# This widget displays the user's reviews and 

user_header = Label(user_reviews, text = 'Your reviews:', justify = 'center', padding = (50, 20, 25, 10), font = ('Helvetica', 13))
user_header.grid(row = 0, column = 0, columnspan = 2)
user_var = StringVar()
user_label = Label(user_reviews, textvariable = user_var, justify = 'left', padding = (0,0,15,0))
user_label.grid(row = 1, column = 0)
rating_var = StringVar()
rating_label= Label(user_reviews, textvariable = rating_var, justify = 'right', padding = (5, 0 , 5, 0))
rating_label.grid(row = 1, column = 1)

# This widget container is for displaying the user's recommendations after at least 5 reviews are added

user_recommendations = App(display_container)
user_recommendations.grid(row = 0, column = 3, rowspan = 2, sticky = 'n')

# This widget displays recommendations after at least 5 reviews are added

recommendation_header = Label(user_recommendations, text = 'Your recommendations:', justify = 'center', padding = (25, 20, 50, 10), font = ('Helvetica', 13))
recommendation_header.grid(row = 0, column = 0)
recommendation_var = StringVar()
recommendation_label = Label(user_recommendations, textvariable = recommendation_var, justify = 'center')
recommendation_label.grid(row = 1, column = 0)

# TO DO
# CURRENT ISSUE:
# Implement map fully after poster is finished
# Improve on recommendation system to limit noise
# Make map bigger, make i/o area more compact
# Separate review and recommendations with borders or boxes
# Place 

# Database style??? - to implement after symposium 
# business id, numeric id/um position, name, category, coordinates or whatever is best for Overpass
# ao23RekjzT-09, 438, McDonald's, Restaurant, -50.20956 or whatever is best for Overpass

# user id, um position
# -=23adyYNvmda, 304

if __name__ == '__main__':
	#test = [('Ambar India (400)', 5), ('Amaravati  Indian Royal Cuisine (61)', 5), ('Aroma Curry House (592)', 5), ('Basmati Indian Cuisine (1450)', 3), ('Bombay Indian Grill (346)', 4)]
	#for i in test:
	#	submit_form(i[0], i[1],user_var, rating_var)
	root.mainloop()