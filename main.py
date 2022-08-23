from fastapi import FastAPI
app = FastAPI()
import uvicorn
from pyairtable import Table

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
Accessed Airtable and returns dict of in-stock drinks and specific ingredients.
"""
def fetchRecipes():
    records = recipes_table.all()
    recipes = {}
    for row in records:
        fields = row['fields']
        drink = fields['Drink']
        inStock = fields['STOCKED']
        if inStock == 1:
            ingredientsRaw = fields['Ingredients (from Types)']
            ingredientsProcessed = []
            for ingredientRaw in ingredientsRaw:
                ingredientProcessed = Table.get(inventory_table, ingredientRaw)
                ingredientsProcessed.append(ingredientProcessed['fields']['Product'])
            if 'Specific Ingredients text' in fields:
                specialsRaw = fields['Specific Ingredients text']
                specialsRaw = specialsRaw.split(',')
                for specialRaw in specialsRaw:
                    ingredientsProcessed.append(specialRaw.strip())
            recipes[drink] = ingredientsProcessed
    return recipes


@app.get("/")
def read_root():
    return fetchRecipes()