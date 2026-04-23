from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv() #loads the environment variables from the .env file into the system environment variables, making them accessible via os.getenv()#


def get_engine():
    engine = create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )
    return engine

def get_total_cost_per_shipment(): #notice that naming your functions properly are important too, the should be self explanatory non of that coded bs that is unnecessary#
    conn = get_engine()
    query = """
        SELECT s.shipment_id, s.cargo_type, s.status,
               c.fuel_cost + c.port_fees + c.supplier_fee + c.customs_cost + COALESCE(c.miscellaneous, 0) AS total_cost
        FROM shipments s
        JOIN costs c ON s.shipment_id = c.shipment_id
        ORDER BY total_cost DESC;
    """
    df = pd.read_sql(query, conn) #runs the query and loads result into the panda dataframe. It takes the query and the database connection as arguments#
    #we dont need to close the connection because sqlalchemy handles it automatically#
    return df

def get_avg_cost_per_route():
    conn = get_engine()
    query = """
        SELECT r.route_id,
                p1.port_name AS origin_port,
                p2.port_name AS destination_port,
                ROUND(AVG(c.fuel_cost + c.port_fees + c.supplier_fee + c.customs_cost + COALESCE(c.miscellaneous, 0)), 2) AS avg_total_cost
        FROM routes r
        JOIN shipments s ON r.route_id = s.route_id
        JOIN costs c ON s.shipment_id = c.shipment_id
        JOIN ports p1 ON r.origin_port_id = p1.port_id
        JOIN ports p2 ON r.destination_port_id = p2.port_id
        GROUP BY r.route_id, p1.port_name, p2.port_name
        ORDER BY avg_total_cost DESC;
    """
    df = pd.read_sql(query, conn)
    return df 

def get_delayed_shipments_by_supplier():
    conn = get_engine()
    query = """
        SELECT sup.supplier_id, sup.supplier_name, COUNT(*) AS Delayed_Shipments
        FROM shipments s
        JOIN suppliers sup ON sup.supplier_id = s.supplier_id
        WHERE s.status = 'delayed'
        GROUP BY sup.supplier_id, sup.supplier_name
        ORDER BY Delayed_Shipments DESC;         
"""
    df = pd.read_sql(query, conn)
    return df


if __name__ == "__main__":
    df = get_delayed_shipments_by_supplier()
    print(df)


