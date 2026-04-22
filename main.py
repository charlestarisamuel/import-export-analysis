#this is the main file. The one we run to kickstart the application and everything else#
from src.db_connection import get_connection
from src.setup_database import run_schema

def main():
    print("Starting Meridian Frieght System...")
    run_schema() #this runs the shema file#
    conn = get_connection() #this connects to the database#
    print("System ready.")
    conn.close() #always close the connection when done#

if __name__ == "__main__":
    main()