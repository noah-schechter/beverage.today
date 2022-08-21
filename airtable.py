from pyairtable import Table
from pyairtable.formulas import match


#Set Up Airtable stuff
base_key = 'appTHjcO6A2sfezsV'
table_name = 'Table 1'
api_key = 'keyZdLTuA4efKanuo' #Set API Key. This isn't secure
table = Table(api_key, base_key, table_name)

def fetchFromAirtable():
    records = table.all()
    menu = {}
    for row in records:
        fields = row['fields']
       # implement this at some point to protect against empty fields if fields.isntEmpty():
        name = fields['Name']
        print(name)
        menu[name] = []
    return menu


def sendToLive(menu):
    return menu



if __name__ == "__main__":
    menu = fetchFromAirtable()
    sendToLive(menu)
    print(menu)
