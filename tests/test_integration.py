from testcontainers.postgres import PostgresContainer
import pytest
from helpers import *
import psycopg2
import os

@pytest.fixture(scope="module")
def postgres_container():
    os.environ["DOCKER_HOST"] = f"unix://{os.path.expanduser('~/.docker/run/docker.sock')}" 
    
    postgres = PostgresContainer("postgres:16")
    postgres.start()
            
    yield postgres
    postgres.stop()

@pytest.fixture(scope="module")
def db_connection(postgres_container):
    conn = psycopg2.connect(
        host=postgres_container.get_container_host_ip(),
        port=postgres_container.get_exposed_port(5432),
        user='test',
        password='test',
        database='test',
    )

    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS locations(
                location_id INT PRIMARY KEY,
                parent_location_id INT REFERENCES locations(location_id),
                location_name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS devices(
                device_id INT PRIMARY KEY,
                device_type TEXT NOT NULL,
                device_name TEXT NOT NULL,
                location_id INT REFERENCES locations(location_id)
            );

            CREATE TABLE IF NOT EXISTS events(
                event_id INT PRIMARY KEY,
                device_id INT REFERENCES devices(device_id),
                "timestamp" TIMESTAMP NOT NULL,
                details JSONB NOT NULL
            );
        """)
        conn.commit()
    
    yield conn
    conn.close()

@pytest.fixture
def clean_db(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("DELETE FROM events;")
        cursor.execute("DELETE FROM devices;")
        cursor.execute("DELETE FROM locations;")
        db_connection.commit()

def test_intagration(db_connection):
    db = DBManager(conn = db_connection)

    db.load_data('data/locations.json', LocationsParse, 'locations')
    db.load_data('data/devices.json', DevicesParse, 'devices')
    db.load_data('data/events.json', EventsParse, 'events')

    query_locations = "SELECT COUNT(*) as count FROM locations" #6220
    query_devices = "SELECT COUNT(*) as count FROM devices" #48815
    query_events = "SELECT COUNT(*) as count FROM events" #27468

    result_locations = db.execute_query(query_locations)
    result_devices = db.execute_query(query_devices)
    result_events = db.execute_query(query_events)

    assert result_locations[0]['count'] == 6220
    assert result_devices[0]['count'] == 48815
    assert result_events[0]['count'] == 27469