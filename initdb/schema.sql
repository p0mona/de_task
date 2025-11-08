CREATE TABLE locations(
    location_id INT PRIMARY KEY,
    parent_location_id INT REFERENCES locations(location_id),
    location_name TEXT NOT NULL
);

CREATE TABLE devices(
    device_id INT PRIMARY KEY,
    device_type TEXT NOT NULL,
    device_name TEXT NOT NULL,
    location_id INT REFERENCES locations(location_id)
);

CREATE TABLE events(
    event_id INT PRIMARY KEY,
    device_id INT REFERENCES devices(device_id),
    "timestamp" TIMESTAMP NOT NULL,
    details JSONB NOT NULL
);