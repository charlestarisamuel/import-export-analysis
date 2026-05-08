#this file's job is to call the api that i got from the websites which i have saved in my env file.#
#then it will load the data it gets into our external_signals table#

import os
from dotenv import load_dotenv
from src.db_connection import get_connection #when writing to the database which we will do in this file, we use get_connection, now when we are using panda is when we use sql alchemy#
import requests #this is what python uses to call the API, it goes to the web address and brings back data#


def fetch_fuel_prices():
    api_key = os.getenv("EIA_API_KEY")
    url = f"https://api.eia.gov/v2/petroleum/pri/spt/data/?api_key={api_key}&frequency=weekly&data[0]=value&facets[series][]=RBRTE&sort[0][column]=period&sort[0][direction]=desc&length=10"

#we changed the url and added some more constraints because we wanted the data to be properly tailored and offer us one type of fuel price that concerns the business and not all of them.#

    response = requests.get(url) #sends the request to the url and gets a response back#
    data = response.json() #converts the reponse into a python dictionary we can work with#


#we made sure we removed the debug print statements for our actual api data because it contains our api key before commiting.#

    prices = data['response']['data'] #since the EIA API gives us the data or wraps the data in nested layers, this line will dig into it and get the actual list of price records.#

    conn = get_connection() #sincce we have gotten the data we want, we open the connection to our database#
    cursor = conn.cursor() #we open the cursor that helps us write into the data base#

    for price in prices:
        date = price['period']
        value = price['value']

        cursor.execute("""
            INSERT INTO external_signals (route_id, recorded_date, fuel_price_usd, weather_risk_score, notes)
            VALUES (1, %s, %s, NULL, 'EIA weekly crude price')
            ON CONFLICT DO NOTHING;                       
""", (date, value))
        
    conn.commit()
    cursor.close()
    conn.close()
    print("Fuel prices loaded successfully.")


if __name__ == "__main__": #indentation matters a lot. This block was not being read because it was inside our fuction based on indentation#
     try:
            fetch_fuel_prices()
     except Exception as e:
            print(f"Error: {e}")