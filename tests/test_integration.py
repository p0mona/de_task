import time

import docker
import psycopg2
import pytest
from testcontainers.postgres import PostgresContainer

from helpers import DBManager, LocationsParse


@pytest.fixture(scope="module")
def postgres_container():

    client = docker.from_env()
    for i in range(10):
        try:
            client.ping()
            break
        except Exception as e:
            print(f"Error {e}")
            time.sleep(2)
    else:
        raise ConnectionError("Error connection to Docker Daemon.")

    postgres = PostgresContainer("postgres:16")
    postgres.start()

    yield postgres
    postgres.stop()


@pytest.fixture(scope="module")
def db_connection(postgres_container):
    time.sleep(1)

    conn = psycopg2.connect(
        host=postgres_container.get_container_host_ip(),
        port=postgres_container.get_exposed_port(5432),
        user="test",
        password="test",
        database="test",
    )

    with conn.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS locations(
                location_id INT PRIMARY KEY,
                parent_location_id INT REFERENCES locations(location_id),
                location_name TEXT NOT NULL
            );
        """
        )
        conn.commit()

    yield conn
    conn.close()


@pytest.fixture
def clean_db(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("DELETE FROM locations;")
        db_connection.commit()


def test_integration(db_connection):
    db = DBManager(conn=db_connection)

    test_data = [
        {
            "location_id": 1,
            "parent_location_id": None,
            "location_name": "Office Building 1",
        },
        {
            "location_id": 2,
            "parent_location_id": 1,
            "location_name": "Floor 1",
        },
    ]
    parsed_data = LocationsParse().parse(test_data)
    db.insert_data("locations", parsed_data)

    query_locations = "SELECT COUNT(*) as count FROM locations"

    result_locations = db.execute_query(query_locations)

    assert result_locations[0]["count"] == 2
