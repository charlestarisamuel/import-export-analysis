#this file is to connect postgreSQL through python so that we can run schema.sql file automatically.
# So instead of going into psql manually every time, you just run Python and it builds everything for you.#
#this file's one job is to read the schema.sql file and execute it against the database throuhg python#

from src.db_connection import get_connection #literally saying from that file, import that function#

def run_schema():
    conn = get_connection()
    cursor = conn.cursor() #this creates a cursor object which is how we execute SQL commands through python. It's like a virtual pen that writes SQL commands to the database. conn opens the line and cursor is what actually sends the commands#
    with open("database/schema.sql", "r") as f: #r means read mode#
        schema = f.read() #now from with we have opened the schema.sql file in read mode, and put the content in the variable "schema". dw with automatically closes the file when it is done#
        
    cursor.execute(schema) #this sends the sql to postgres#
    conn.commit() #this is really important - it saves the changes in postgres#

    with open("database/seed_data.sql", "r") as f:
           seed_data= f.read()

    cursor.execute(seed_data)
    conn.commit() #don't forget to indent these two lines outside the with block#


    cursor.close()
    conn.close() #always close the cursor and connection when done#
    print("Database schema created successfully.")



if __name__ == "__main__":
            run_schema()