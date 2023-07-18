"""test_db.py
This is a demonstration of the pytest_docker_tools package to create a local Postgres database for testing with Docker.

* We create container running a postgres DB on our local machine that is seeded with a table from `postgres-init.sql`
* We test a database insert operation and assert that the inserted values match the defined test cases

"""

import os

import pytest
from psycopg2 import connect
from pytest_docker_tools import container, fetch

# Fetch a PostgreSQL image
postgres_image = fetch(repository="postgres:11")

# Define a container using the image
postgres = container(
    image="{postgres_image.id}",
    environment={"POSTGRES_PASSWORD": "password"},
    ports={"5432/tcp": None},
    volumes={
        os.path.join(os.path.dirname(__file__), "postgres-init.sql"): {
            "bind": "/docker-entrypoint-initdb.d/postgres-init.sql"
        }
    },
)


# Set up a fixture for database connection
@pytest.fixture(scope="function")
def db(postgres):
    """Returns a psycopg2 connection to the test database."""
    docker_port = postgres.ports["5432/tcp"][0]
    conn = connect(
        host="localhost",
        port=docker_port,
        dbname="postgres",
        user="postgres",
        password="password",
    )
    conn.autocommit = True
    yield conn
    conn.close()


# Test case to check simple insert
def test_simple_insert(db):
    cur = db.cursor()
    insert_query_template = "INSERT INTO test (num, data) VALUES (%s, %s)"
    data = [(100, "testdata_foo"), (200, "testdata_bar")]
    cur.executemany(insert_query_template, data)
    cur.execute("SELECT * FROM test;")
    results = cur.fetchall()

    # row 0
    assert results[0][1] == 100
    assert results[0][2] == "testdata_foo"

    # row 1
    assert results[1][1] == 200
    assert results[1][2] == "testdata_bar"
