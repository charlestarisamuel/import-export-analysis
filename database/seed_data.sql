-- suppliers
INSERT INTO suppliers (supplier_id, supplier_name, country, contact_email, reliability_score) VALUES
(1, 'FastShip Ltd', 'Nigeria', 'ops@fastship.com', 7.5),
(2, 'TransGlobe Freight', 'Germany', 'contact@transglobe.de', 8.2),
(3, 'Nile Cargo Co', 'Egypt', 'info@nilecargo.eg', 6.8),
(4, 'Meridian Partners', 'United Kingdom', 'partners@meridian.co.uk', 9.0),
(5, 'Gulf Express', 'UAE', 'ops@gulfexpress.ae', 7.1);

-- ports
INSERT INTO ports (port_id, port_name, country, port_type, avg_delays_days) VALUES
(1, 'Apapa Port', 'Nigeria', 'sea', 3.2),
(2, 'Port of Hamburg', 'Germany', 'sea', 1.1),
(3, 'Port of Felixstowe', 'United Kingdom', 'sea', 0.8),
(4, 'Alexandria Port', 'Egypt', 'sea', 2.5),
(5, 'Jebel Ali Port', 'UAE', 'sea', 0.5),
(6, 'Heathrow Airport', 'United Kingdom', 'air', 1.2),
(7, 'Frankfurt Airport', 'Germany', 'air', 0.9);

-- routes
INSERT INTO routes (route_id, origin_port_id, destination_port_id, distance_km, typical_duration_days, base_cost_usd) VALUES
(1, 1, 3, 8400, 21, 9500.00),
(2, 1, 2, 7200, 18, 8200.00),
(3, 4, 3, 5100, 14, 7100.00),
(4, 5, 2, 6300, 16, 7800.00),
(5, 4, 6, 4500, 7, 12000.00);

-- shipments
INSERT INTO shipments (shipment_id, supplier_id, route_id, origin_port_id, destination_port_id, departure_date, expected_arrival, actual_arrival, cargo_type, weight_kg, status) VALUES
(1001, 1, 1, 1, 3, '2024-01-10', '2024-01-31', '2024-02-03', 'Agricultural', 12000.00, 'delivered'),
(1002, 2, 2, 1, 2, '2024-01-15', '2024-02-02', '2024-02-02', 'Electronics', 8500.00, 'delivered'),
(1003, 3, 3, 4, 3, '2024-01-20', '2024-02-03', '2024-02-07', 'Textiles', 15000.00, 'delivered'),
(1004, 4, 4, 5, 2, '2024-02-01', '2024-02-17', '2024-02-17', 'Machinery', 22000.00, 'delivered'),
(1005, 5, 5, 4, 6, '2024-02-10', '2024-02-17', NULL, 'Pharmaceuticals', 3200.00, 'delayed'),
(1006, 1, 1, 1, 3, '2024-02-15', '2024-03-07', '2024-03-10', 'Agricultural', 11000.00, 'delivered'),
(1007, 3, 3, 4, 3, '2024-02-20', '2024-03-05', NULL, 'Textiles', 9000.00, 'in transit'),
(1008, 2, 2, 1, 2, '2024-03-01', '2024-03-19', '2024-03-18', 'Electronics', 7800.00, 'delivered'),
(1009, 4, 4, 5, 2, '2024-03-10', '2024-03-26', '2024-03-28', 'Machinery', 19000.00, 'delivered'),
(1010, 5, 5, 4, 6, '2024-03-15', '2024-03-22', NULL, 'Pharmaceuticals', 2800.00, 'delayed');

-- costs
INSERT INTO costs (cost_id, shipment_id, fuel_cost, port_fees, supplier_fee, customs_cost, miscellaneous) VALUES
(1, 1001, 3200.00, 850.00, 4500.00, 1200.00, 300.00),
(2, 1002, 2800.00, 720.00, 3900.00, 980.00, NULL),
(3, 1003, 2100.00, 650.00, 3200.00, 850.00, 200.00),
(4, 1004, 2600.00, 780.00, 4100.00, 1100.00, NULL),
(5, 1005, 4200.00, 920.00, 5800.00, 1400.00, 500.00),
(6, 1006, 3100.00, 830.00, 4400.00, 1150.00, NULL),
(7, 1007, 2000.00, 640.00, 3100.00, 820.00, 180.00),
(8, 1008, 2750.00, 710.00, 3850.00, 960.00, NULL),
(9, 1009, 2550.00, 770.00, 4050.00, 1080.00, NULL),
(10, 1010, 4100.00, 900.00, 5700.00, 1380.00, 450.00);

-- external_signals
INSERT INTO external_signals (signal_id, route_id, recorded_date, fuel_price_usd, weather_risk_score, notes) VALUES
(1, 1, '2024-01-10', 88.50, 6.0, 'Mild storm warning near Lagos'),
(2, 2, '2024-01-15', 87.20, 2.0, 'Clear conditions'),
(3, 3, '2024-01-20', 86.80, 3.5, 'Light winds near Alexandria'),
(4, 4, '2024-02-01', 89.10, 1.5, 'Clear conditions'),
(5, 5, '2024-02-10', 91.50, 7.5, 'Storm system over Mediterranean'),
(6, 1, '2024-02-15', 90.20, 4.0, 'Moderate swell reported'),
(7, 3, '2024-02-20', 88.90, 2.5, 'Clear conditions'),
(8, 2, '2024-03-01', 87.60, 1.0, 'Clear conditions'),
(9, 4, '2024-03-10', 89.80, 3.0, 'Light turbulence reported'),
(10, 5, '2024-03-15', 92.10, 8.0, 'Severe storm warning issued');