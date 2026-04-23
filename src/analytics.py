from unittest import result

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



#which shipments cost more than the average in their route#

#this pulls every shipment with it's total cost into our dataframe#
def get_cost_outliers():
    conn = get_engine()
    query = """
         SELECT s.shipment_id, s.cargo_type, s.route_id,
               c.fuel_cost + c.port_fees + c.supplier_fee + 
               c.customs_cost + COALESCE(c.miscellaneous, 0) AS total_cost
        FROM shipments s
        JOIN costs c ON s.shipment_id = c.shipment_id
"""

    df = pd.read_sql(query, conn)

    route_avg = df.groupby('route_id')['total_cost'].mean() #groupby groups the data by route. Then .mean() calculates the average cost for each route#
    route_std = df.groupby('route_id')['total_cost'].std() #this calculates the standard deviation for each route, which is a measure of how spread out the costs are#

    df['route_avg'] = df['route_id'].map(route_avg) #this creates a new column in the dataframe called route_avg, which maps each shipment's route_id to the average cost for that route#
    df['route_std'] = df['route_id'].map(route_std) #this creates a new column in the dataframe called route_std, which maps each shipment's route_id to the standard deviation of costs for that route#

    #now the outlier logic#
    df['is_outlier'] = df['total_cost'] > df['route_avg'] + df['route_std'] #this creates a new column called is_outlier, which is True if the shipment's total cost is greater than the average cost for its route plus one standard deviation#
    outliers = df[df['is_outlier'] == True]
    return outliers
    #the outlier logic is saying if the shipment's cost is greater than the route averaege plus the standard diviation, flag it as an outlier#
    #the last line then filters the data frmae and returns only the outliers#



def get_delay_rate_per_route():
    conn = get_engine()
    query = """
        SELECT r.route_id,
               p1.port_name AS origin_port,
               p2.port_name AS destination_port,
               COUNT(*) AS total_shipments,
               SUM(CASE WHEN s.status = 'delayed' THEN 1 ELSE 0 END) AS delayed_shipments
        FROM shipments s
        JOIN routes r ON s.route_id = r.route_id
        JOIN ports p1 ON r.origin_port_id = p1.port_id
        JOIN ports p2 ON r.destination_port_id = p2.port_id
        GROUP BY r.route_id, p1.port_name, p2.port_name
        ORDER BY r.route_id;
"""
    df = pd.read_sql(query, conn)
    df['delay_rate_%'] = (df['delayed_shipments'] / df['total_shipments'] * 100).round(1)
    return df


def get_transit_time_comparison():
    conn = get_engine()
    query = """
        SELECT sup.supplier_name, s.supplier_id, s.shipment_id, s.expected_arrival, s.actual_arrival
        FROM shipments s
        JOIN suppliers sup ON s.supplier_id = sup.supplier_id
        WHERE s.actual_arrival IS NOT NULL
"""
    df = pd.read_sql(query, conn)
    df['actual_arrival'] = pd.to_datetime(df['actual_arrival'])
    df['expected_arrival'] = pd.to_datetime(df['expected_arrival']) #this is to convert these columns to datetime#


    
    df['delayed_days'] = (df['actual_arrival'] - df['expected_arrival']).dt.days #since actual time and expected are already columns we can just do this calculation here. .dt.days converts the result from time diffrence to a plain number of days#

    result = df.groupby('supplier_name')['delayed_days'].mean().reset_index() #reset index pushes it back to a regular column so the result looks like a clean table#
    result.columns = ['supplier_name', 'avg_delay_days'] #this renames the columns#
    return result

#notes#
#putting it in result is how you display what you want from your dataframe not everything in the dataframe#



if __name__ == "__main__":
    df = get_transit_time_comparison() 
    print(df)


