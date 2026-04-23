from src.db_connection import get_connection
import pandas as pd

def get_total_cost_per_shipment(): #notice that naming your functions properly are important too, the should be self explanatory non of that coded bs that is unnecessary#
    conn = get_connection() #establish you database connection then write your query below#
    query = """
        SELECT s.shipment_id, s.cargo_type, s.status,
               c.fuel_cost + c.port_fees + c.supplier_fee + c.customs_cost + COALESCE(c.miscellaneous, 0) AS total_cost
        FROM shipments s
        JOIN costs c ON s.shipment_id = c.shipment_id
        ORDER BY total_cost DESC;
    """
    df = pd.read_sql(query, conn) #runs the query and loads result into the panda dataframe. It takes the query and the database connection as arguments#
    conn.close() #always close the connection when done#
    return df

if __name__ == "__main__":
    df = get_total_cost_per_shipment()
    print(df)


