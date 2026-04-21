/*this file is made to create the tables*/

/*We first drop all the tables in reverse order so that whenever another script runs this file it first deletes the tables before creating them agian because postgres wouldn't let us create tables if they already exist*/
/*We drop the tables in reverse order of their dependencies if not postgres would send us an error*/
DROP TABLE IF EXISTS external_signals;
DROP TABLE IF EXISTS costs;
DROP TABLE IF EXISTS shipments;
DROP TABLE IF EXISTS routes;
DROP TABLE IF EXISTS ports;
DROP TABLE IF EXISTS suppliers;

CREATE TABLE suppliers (
    supplier_id INT PRIMARY KEY NOT NULL,
    supplier_name VARCHAR(225) NOT NULL,
    country VARCHAR(50) NOT NULL,
    contact_email VARCHAR(50),
    reliability_score DECIMAL(3, 1) /*this is saying there can be 3 total digits one before the point and 2 thereafter*/
);

CREATE TABLE ports (
    port_id INT PRIMARY KEY NOT NULL,
    port_name VARCHAR(225) NOT NULL,
    country VARCHAR(50) NOT NULL,
    port_type VARCHAR(10) CHECK (port_type IN ('sea', 'air', 'land')), /*this is how we write it when we want the inputs only be this tree values*/
    avg_delays_days DECIMAL(3,1)
);

CREATE TABLE routes (
    route_id INT PRIMARY KEY NOT NULL,
    origin_port_id INT NOT NULL,
    destination_port_id INT NOT NULL,
    distance_km DECIMAL(10, 2),
    typical_duration_days INT,
    base_cost_usd DECIMAL(10, 2),
    FOREIGN KEY (origin_port_id) REFERENCES ports(port_id),
    FOREIGN KEY (destination_port_id) REFERENCES ports(port_id)
);

CREATE TABLE shipments (
    shipment_id INT PRIMARY KEY NOT NULL,
    supplier_id INT NOT NULL,
    route_id INT NOT NULL,
    origin_port_id INT NOT NULL,
    destination_port_id INT NOT NULL,
    departure_date DATE NOT NULL,
    expected_arrival DATE NOT NULL,
    actual_arrival DATE,
    cargo_type VARCHAR(50),
    weight_kg DECIMAL(10, 2),
    status VARCHAR(20) CHECK (status IN ('delivered', 'in transit', 'delayed', 'arrived', 'cancelled')),  
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
    FOREIGN KEY (route_id) REFERENCES routes(route_id),
    FOREIGN KEY (origin_port_id) REFERENCES ports(port_id),
    FOREIGN KEY (destination_port_id) REFERENCES ports(port_id) 
);

CREATE TABLE costs(
    cost_id INT PRIMARY KEY NOT NULL,
    shipment_id INT NOT NULL,
    fuel_cost DECIMAL(10, 2) NOT NULL,
    port_fees DECIMAL(10, 2) NOT NULL,
    supplier_fee DECIMAL(10, 2) NOT NULL,
    customs_cost DECIMAL(10, 2) NOT NULL,
    miscellaneous DECIMAL(10, 2),
    FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id)
);

CREATE TABLE external_signals (
    signal_id INT PRIMARY KEY NOT NULL,
    route_id INT NOT NULL,
    recorded_date DATE NOT NULL,
    fuel_price_usd DECIMAL(10, 2) NOT NULL,
    weather_risk_score DECIMAL(3, 1),
    notes TEXT,
    FOREIGN KEY (route_id) REFERENCES routes(route_id)
);

/*notice routes references ports, and shipments references both routes and suppliers. The order your tables are written matters — PostgreSQL can't create a table that references another table that doesn't exist yet.*/
/*to run it we need to connect to our database psql -U postgres -d meridian_freight*/
/*inside the meridian_freight database we ran \i database/schema.sql to execute the script*/