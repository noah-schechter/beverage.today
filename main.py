from fastapi import FastAPI
app = FastAPI()

from pyairtable import Table
from pyairtable.formulas import match

import os 
from dotenv import load_dotenv

#Set Up Airtable stuff
base_key = 'appTHjcO6A2sfezsV'
load_dotenv()
api_key = os.environ.get('API_KEY')
table_1_name = 'tbl85euKMNpg1Fn0O'
inventory_table = Table(api_key, base_key, table_1_name)
table_2_name = 'tblcgPnwDpkj6x36D'
recipes_table = Table(api_key, base_key, table_2_name)

"""
Accesses Airtable and returns list of available drinks
"""
def fetchInventory():
    records = inventory_table.all()
    inventory = {}
    for row in records:
        fields = row['fields']
        typeDrink = fields['Type of Alcohol']
        ingredient = fields['Product']
        if typeDrink not in inventory:
            inventory[typeDrink] = []
        inventory[typeDrink].append(ingredient)
    return inventory

def fetchRecipes():
    records = recipes_table.all()
    recipes = {}
    for row in records:
        fields = row['fields']
        drink = fields['Drink']
        ingredients = fields['Ingredients']
        if drink not in recipes:
            recipes[drink] = []
        recipes[drink] = ingredients
    return recipes

"""
Takes in recipe of form [ingredient list] and inventory of form {type of drink: [products], type of drink: [products]. Returns boolean indicating whether a drink can be made, and, if true, a list of products in barcart that comprise that recipe.
"""
def constructMenuItem(ingredients, inventory):
    menuItem = []
    for ingredient in ingredients:
        if ingredient not in inventory:
            return False, []
        menuItem.append(inventory[ingredient][0]) #this is where we could break ties in a different way
    return True, menuItem

"""
Loops through recipes and constructs a menu of drinks that can be assembled, and which products they will require.
"""
def constructMenu(recipes, inventory):
    menu = {}
    for drink in recipes.keys():
        possible, ingredients = constructMenuItem(recipes[drink], inventory)
        if possible and drink not in menu:
            menu[drink] = ingredients
    return menu


@app.get("/")
def read_root():
    inventory = fetchInventory()
    recipes = fetchRecipes()
    return constructMenu(recipes, inventory)
    print(menu)