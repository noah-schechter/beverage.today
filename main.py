#Use the following to run locally: uvicorn main:app --host 0.0.0.0 --port 80


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
api_key = os.environ.get('API_TOKEN')
table_1_name = os.environ.get('table_1_name')
inventory_table = Table(api_key, base_key, table_1_name)
table_2_name = os.environ.get('table_2_name')
recipes_table = Table(api_key, base_key, table_2_name)


#Initialize Time
from datetime import time, timedelta
import datetime
import pytz


def getTime():
    #dateTime = str(datetime.date.today())
    place = pytz.timezone('America/Los_Angeles')
    dateTime = datetime.datetime.now(place)
    dateTime = str(dateTime)[0:10]
    print(dateTime)
    return str(dateTime[5:7] + u'\u2022' + dateTime[8:10] + u'\u2022' + dateTime[0:4])


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
        if inStock == 1 and 'IngredientsText' in fields:         #Only continue if all of the drink's ingredients are in stock
            ingredientsRaw = fields['IngredientsText'].strip()   #Fetch a string containing comma-separated ingredient names
            if 'GarnishesText' in fields:                        #Check if there are any garnishes
                garnishes = fields['GarnishesText']   
                garnish = garnishes[0]
                #for garnish in garnishes:                            #Change this logic to just select one garnish or display multiple
                ingredientsRaw = ingredientsRaw + ", " + garnish  
            recipes[drink] = (ingredientsRaw).lower()            #Add a lowercased version of the ingredient list as the value to the drink key in the recipes dict
    return recipes


@app.get("/")
def read_root(request:Request):
    menu = fetchRecipes()
    dateTime = getTime()
    return templates.TemplateResponse("home.html", {"request": menu, "menu":menu, "time":dateTime})


@app.get("/api")
def gen_api(request:Request):
    return fetchRecipes()
