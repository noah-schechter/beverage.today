#Initialize FASTAPI
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pathlib import Path
app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",)
import uvicorn


#Set Up API Key Security
import os 
from dotenv import load_dotenv

#Set up Templates
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
templates = Jinja2Templates(directory="templates")


#Set Up Airtable stuff
from pyairtable import Table
base_key = 'appTHjcO6A2sfezsV'
load_dotenv()
api_key = os.environ.get('API_KEY')
table_1_name = 'tbl85euKMNpg1Fn0O'
inventory_table = Table(api_key, base_key, table_1_name)
table_2_name = 'tblcgPnwDpkj6x36D'
recipes_table = Table(api_key, base_key, table_2_name)

#Initialize Time
from datetime import time, timedelta
import datetime

def getTime():
    dateTime = str(datetime.datetime.utcnow())
    hour = int(dateTime[11:13])
    if hour < 7:
        return str(datetime.date.today() - timedelta(days=1))
    dateTime = str(datetime.date.today())
    new = dateTime[5:7] +u"\u2022" + dateTime[8:10] + 	u"\u2022" + dateTime[0:4]
    return new


"""
Accesses Airtable and returns dict of in-stock drinks and specific ingredients.
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
            ingredientsProcessed = ""
            for ingredientRaw in ingredientsRaw:
                ingredientProcessed = Table.get(inventory_table, ingredientRaw)
                ingredientsProcessed = ingredientsProcessed + (ingredientProcessed['fields']['Product']) + ", "
            if 'Specific Ingredients text' in fields:
                specialsRaw = fields['Specific Ingredients text']
                specialsRaw = specialsRaw.split(',')
                for specialRaw in specialsRaw:
                    ingredientsProcessed = ingredientsProcessed + (specialRaw.strip()) + ", "
            length = len(ingredientsProcessed)
            recipes[drink] = ingredientsProcessed[:length - 2].lower()
    return recipes


@app.get("/")
def read_root(request:Request):
    menu = fetchRecipes()
    dateTime = getTime()
    return templates.TemplateResponse("home.html", {"request": menu, "menu":menu, "time":dateTime})