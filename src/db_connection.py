#this files reads our .env file and creates the conection to the database#

#these three lines import the libraries we need almost like linking a css file#
import psycopg2
from dotenv import load_dotenv
import os

#this reads the .env file and loads everything into the memory. so after this runs python knows the database credentials#
load_dotenv()


#this defines the function. DEF means you are creating a reusable block of code. Any time another file needs to connect to the database it just calls this function instead of rewriting all the connection logic#
def get_connection():
    conn = psycopg2.connect( #this is the code that actually creates the connection to the database. It uses the psycopg2 library and the credentials from the .env file to connect to the database. The connection object is then returned so that other files can use it to interact with the database.#
        host=os.getenv("DB_HOST"), #reads each value from the .env file by name#
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn #this hands the connection back to whoever calls this function so they can now connect#


if __name__ == "__main__": #every python file has a built in variable called __name__ when you run a file directly, python sets the variable to main. Now when another file imports this file, it gets set to the file's name instead. So this block only runs when you run this file directly — not when other files import it. It's how Python separates "run this" from "just use the functions inside this."#
    conn = get_connection()
    print("Connected to Meridian Freight successfully.")
    conn.close()