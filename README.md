# pytest_docker_tools_demo

This is a demonstration of the `pytest_docker_tools` package to create a local Postgres database for testing with Docker.
* This is one of several Python packages that provide convenient functions for controlling Docker containers within the scope of pytest tests.
* This is useful for when you do not have (or do not want) access to the production database in unit tests.

Advantages
* More realistic tests - you want to test actual DB method calls (e.g., `cursor.execute()`) instead of mocking them
* Development - you can use the test DB to run small snippets and debug in your IDE instead of testing against a live system

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

### Running the tests
`python -m pytest`

### VS Code `.vscode/launch.json` config for IDE debugger
To run the pytest suite in debug mode we have need a little IDE configuration.
* In VS Code, open the command palette with CMD+Shift+P.
* Search `Debug: Add Configuration`.
* Edit the `launch.json` file with the following.
* Set a breakpoint where you need and hit F5 or Run>Start Debugging

```
// .vscode/launch.json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": [
                "tests/test_db.py"
            ],
            "justMyCode": false,
            "console": "integratedTerminal"
        }
    ]
}
```
