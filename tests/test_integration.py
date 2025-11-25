from testcontainers.postgres import PostgresContainer
import pytest
import os
from helpers import *

postgres = PostgresContainer("postgres:16")
sql_path = os.path.join(os.path.dirname(__file__), "../initdb/schema.sql")
with open(sql_path, "r") as f:
    sql = f.read()

@pytest.fixture(scope="module", autouse=True)
def setup(request):
    postgres.start()

    def remove_container():
        postgres.stop()

    request.addfinalizer(remove_container)
    os.environ["DB_CONN"] = postgres.get_connection_url()
    os.environ["DB_HOST"] = postgres.get_container_host_ip()
    os.environ["DB_PORT"] = postgres.get_exposed_port(5432)
    os.environ["DB_USERNAME"] = postgres.username
    os.environ["DB_PASSWORD"] = postgres.password
    os.environ["DB_NAME"] = postgres.dbname
    sql.create_table()


@pytest.fixture(scope="function", autouse=True)
def setup_data():
    sql.delete_all_customers()

def integration_test():
    db = DBManager()

    db.load_data('data/locations.json', LocationsParse, 'locations')
    db.load_data('data/devices.json', DevicesParse, 'devices')
    db.load_data('data/events.json', EventsParse, 'events')

    query_locations = "SELECT COUNT(*) FROM locations" #6220
    query_devices = "SELECT COUNT(*) FROM devices" #48815
    query_events = "SELECT COUNT(*) FROM events" #27468

    result_locations = db.execute_query(query_locations)
    result_devices = db.execute_query(query_devices)
    result_events = db.execute_query(query_events)

    assert result_locations == 6220
    assert result_devices == 48815
    assert result_events == 27469