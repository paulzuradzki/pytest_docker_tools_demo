# pytest_docker_tools_demo

This is a demonstration of the `pytest_docker_tools` package to create a local Postgres database for testing with Docker.
* Several Python packages exist that provide convenient functions for controlling Docker containers within the scope of pytest tests.
* This is useful for when you do not have (or do not want) access to the production database in unit tests.

### Repo contents

```
.
├── README.md
├── requirements.txt
├── src
└── tests
    ├── postgres-init.sql
    └── test_db.py

2 directories, 4 files
```

### Database initialization script
* Create a SQL DB table initializer script (`postgres-init.sql`), which runs automatically when the container starts.
* Alternatively, you run the CREATE TABLE statements directly in your tests.

```sql
/* ./tests/postgres-init.sql */
CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, num integer, data varchar);
```

### Test code - `tests/test_db.py`
* The code is designed to test database operations in isolation by running each test with a clean, temporary PostgreSQL database in a Docker container.
* This approach is useful when you need to test database operations but don't want the tests to affect a persistent database.
