
# coding: utf-8

# ## Import Modules

# In[1]:


import csv
from random import randint


# We need CSV to read the menu file that we've made, and we need random to randomly assign meals to days of the week

# ## Define Constants, Classes and Modules

# In[2]:


DAYS = ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')
RECIPE_FILE = 'recipe.csv'


# Here are our initial constants that wont change throughout the program (standard Python practice is to have constants in all uppercase)

# In[3]:


class Day:
    def __init__(self, name):
        self.name = name
        self.meal = None
        self.diners = 0
        
    def add_meal(self, new_meal):
        self.meal = new_meal
        
    def number_of_diners(self):
        self.diners = int(input('How many People are eating on ' + self.name +'? (0,1 or 2)> '))
        
    def ingredients(self):
        return self.meal.recipe


# Okay so now we're making "Classes", the first class we make is a Day class. Each Day has a name (hopefully self explanatory), a meal assigned to that day, and a number of people eating that day. We also make two (very simple) modules for the Day objects, one that assins the meal to the Day, and the other that asks the user how many people are eating on said day.

# In[4]:


class Meal:
    def __init__(self, name, recipe):
        self.name = name
        self.recipe = []
        
    def make_recipe(self, ingredient):
        self.recipe.append(ingredient)
    
    '''def shopping_list(self):
        print(self.name)
        for r in self.recipe:
            print('\t',r.quantity, r.unit, r.name)'''

class Ingredients: 
    def __init__(self, name, quantity, unit):
        self.name = name.title() #make everything the same case to avoid duplicates from bad data entry
        self.quantity = float(quantity) #make everything numbers
        self.unit = unit.lower() #make everything the same case to avoid duplicates from bad data entry        


# Here is where the magic happens in terms of how the program will think about food. We have a class called "Meal" which consists of a name for the meal and a list for its ingredients. 
# 
# We have a second class called Ingredients which has three components, the name of the ingredient, the ammount needed for the recipe it's being used in, and the unit for said ammount (i.e. grams etc). In this program we build the ingredients by parsing a CSV file so the ```__init__``` for the class takes a list, and then populates it from that list.
# 
# Meal has a couple of modules too, firstly ```make_recipe``` which is used to go through the .csv file to add the ingredients to the meal, and ```shopping_list``` which i've been using for debugging, i think i will need to come back to this later and actually move it to days

# In[5]:


class Shopping_List:
    def __init__(self):
        self.ingredients = []
    
    def add_ingredient(self,ingredient_to_add):
        if ingredient_to_add.name not in [i.name for i in self.ingredients]:
            self.ingredients.append(ingredient_to_add)
        else:
            ingredient_to_update = [i.name for i in self.ingredients].index(ingredient_to_add.name)
            self.ingredients[ingredient_to_update].quantity += ingredient_to_add.quantity
            
    def print_shopping_list(self):
        print('This week, you will need:')
        for ingredient in self.ingredients:
            print ("\t",ingredient.quantity, ingredient.unit, "of", ingredient.name)
    


# In[6]:


def make_cookbook(recipes): #goes through the CSV file and makes Meal classes for each meal in there
    meals =[]    
    for r in recipes:
        if r[0] != '': #if the first column it not empty (i.e. contains a name)
            meal = (Meal(r[0].title(),None)) # Make a new meal (with an empty ingredients list with the name that appears in the first column)
            meals.append(meal) #adds it to our list
                
        else:        #steps down to the next row and starts turning everything into ingredients
            ingredient_to_add = Ingredients(r[1],r[2],r[3]) #turn that row into an Ingredient object (starting in the 2nd col)
            meal.make_recipe(ingredient_to_add) #add that ingredient to the list for the above meal
                
    return meals 


# Okay this module is complicated so i've commented it really thoroughly, but basically we go through the CSV file which is laid out like 
# ```
# 'meal1 name',       ''     ,      ''   ,   '', 
#    ''     , 'ingredient1', 'quantity', 'unit',
#    ''     , 'ingredient2', 'quantity', 'unit',
# 'meal2 name',       ''     ,      ''   ,   '', 
#    ''     , 'ingredient1', 'quantity', 'unit',
#    ''     , 'ingredient2', 'quantity', 'unit', ```
#    
#  etc etc and turns that into a python object with a name, and a list of ingredients which themselves are python objects with names, quantities and units.

# ## Start Running The Code

# In[7]:


with open(RECIPE_FILE) as recipe_file:
    recipe_list = list(csv.reader(recipe_file)) #makes a list of all the meals called cookbook
    
cookbook = make_cookbook(recipe_list)


# This opens the .csv file which holds our recipe list and makes a list of all of them called ```cookbook```

# In[8]:


days = [Day(d) for d in DAYS]

for day in days:
    day.number_of_diners()# works out which days people are eating

## Literally no idea why it needs this while loop to work, but this loop makes it work so 👍
while 0 in [d.diners for d in days]:
    for d in days:
        if d.diners == 0:
            days.remove(d)


# This makes a list of Days objects called ```days``` for each of the 7 days of the week. It then asks the user to say how many people are going to be eating on each day of the week. If then removes any days where no one will be eating. 
# 

# In[9]:


print("Your meal plan for this week is:\n")
for day in days:
    chosen_meal = cookbook[randint(0,len(cookbook)-1)]
    day.add_meal(chosen_meal)
    cookbook.remove(chosen_meal)
    
    print("\t",day.name, "=", day.meal.name)


# This goes through the days that people will be eating on and then assigns them a meal randomly from ```cookbook```. It then removes assigned meals from `cookbook` so they can't be assigned more than once a week. Finally it outputs the meal plan for the week.

# In[10]:


for d in days:
    for i in d.ingredients():
        i.quantity = i.quantity * (d.diners/2)


# This code alters the quantity to match the number of diners (assuming the receipes are for 2 people)

# In[11]:


shopping_list = Shopping_List()

for d in days:
    for i in d.ingredients():
        shopping_list.add_ingredient(i)

shopping_list.print_shopping_list()

