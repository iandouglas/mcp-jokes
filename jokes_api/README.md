# Joke API

This is a simple RESTful API for serving jokes. It allows users to retrieve jokes based on categories, search for jokes, and get random jokes.

## Features
- Retrieve a random joke
- Get a joke by its ID
- Search for jokes by keyword
- Search by keyword with a count of maximum results


## Setup & Running the API

You will need [uv](https://docs.astral.sh/uv/getting-started/installation/) installed and working.

The API is set up to bind to IP address "0.0.0.0" on port 8000, which means it will be accessible from any IP address on your local network on port 8000. To change this, modify main.py on line 123 from this:

```python
uvicorn.run(app, host="0.0.0.0", port=8000)
```

to this:

```python
# to bind to localhost only
uvicorn.run(app, host="127.0.0.1", port=...)

# or, to bind to a different port, like port 9000:
uvicorn.run(app, host="...", port=9000)

# or specify a different IP address and port. The port must be an integer between 1024 and 65535.
uvicorn.run(app, host="1.2.3.4", port=19000)
```

Note that changing the IP address or port will require you to modify the MCP server configuration to match the new settings. Otherwise, the MCP server will not be able to connect to the API.

### Running the API

To run the API, follow these steps:

```bash
uv run main.py
```

The first time you use the `uv run ...` command, it will download and install the required packages, which may take a few minutes. After the initial setup, subsequent runs will be much faster.

You should see output similar to:

```text
$ uv run main.py
Using CPython 3.13.2 interpreter at: /opt/homebrew/opt/python@3.13/bin/python3.13
Creating virtual environment at: .venv
Installed 13 packages in 8ms
INFO:     Started server process [21623]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)    
```

## Documentation and OpenAPI spec

When your API is running, you can access the following URLs to see more information about the API and test it locally. Adjust the hostname/IP address and port number as needed if you changed them in the setup step above.

### Built-in Documentation

* http://localhost:8000/docs

### OpenAPI Specification

* http://localhost:8000/openapi.json
