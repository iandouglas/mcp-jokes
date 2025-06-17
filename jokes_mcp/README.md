# MCP Jokes Extension

A humor/joke extension for [Codename Goose](https://block.github.io/goose) that provides access to a collection of jokes through the Model Context Protocol (MCP).

## Features

- Get random jokes
- Search for one or more jokes by topic or keyword
- Retrieve a specific jokes by ID
- Add new jokes with topics
- Delete jokes

## Setup

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver
- A local jokes API running on port 8000 (provided separately); manually change the hostname/port in `main.py` if needed.

### Installation & Running

By running `uv run main.py`, the virtual environment will be created automatically, and all dependencies will be installed.

## Testing the MCP Server

Run the "client" script to verify everything is working:

```bash
$ uv run client_test.py
Starting MCP Jokes Extension Tests...

(output here)

Tests completed!
```

If no errors are shown, the MCP server is functioning correctly and ready to use.

This will test all available resources and tools:
- Random joke retrieval
- Joke lookup by ID
- Joke searching (single and multiple)
- Adding and deleting jokes

## Adding the MCP Server to Codename Goose

1. [Download Goose Desktop](https://block.github.io/goose/docs/getting-started/installation)
1. Open Goose Desktop
1. Go to Settings (top right menu)
1. Navigate to Extensions
1. Click "Add Extension"
1. Give it a name, select 'STDIO' as the type, add a description, and enter the command to run the MCP server:
   ```
   uv run /path/to/jokes_mcp/main.py
   ```
   Replace `/path/to/jokes_mcp/main.py` with the actual path to the `main.py` file in your MCP server directory.
   If `uv` is not in your PATH, you may need to provide the full path to the `uv` executable, such as:
   ```
   /path/to/uv run /path/to/jokes_mcp/main.py
   ```
1. Click "Save changes"

You should be ready to ask Goose for some laughs! Goose will enable the MCP server on an as-needed basis. The first time you ask for a joke, Goose will start the MCP server, check its capabilities, and then respond to your request. The MCP server will remain running in the background until you close your Goose session.

## Sample Prompts for Goose

Here are some example prompts to use with Goose once the extension is enabled:

1. Get a random joke:
```
Tell me a joke
```

2. Get jokes about a specific topic:
```
Tell me a joke about animals
Tell me 3 jokes about programming
```
(Goose may return fewer results than requested if not enough jokes match the topic.)


3. Add a new joke:
```
Add this joke: "Why don't programmers like nature? It has too many bugs!" with topics: programming, nature, bugs
```

4. Manage jokes:
```
Get joke number 15
Delete joke number 42
```

## Troubleshooting

1. **API Connection Issues**
   - Ensure the jokes API is running; modify the MCP server's `main.py` to match the API's hostname and port if different than localhost:8000.
   - Check the API health endpoint: `curl http://localhost:8000/health` (adjust the host/ip and port as needed). You should see a response like this:
   ```json
   {
      "status": "running",
      "jokes_count":35
   }
   ```

2. **Extension Not Working in Goose or can't be Enabled**
   - Verify the manifest.json file is properly formatted and has the correct file system path to the MCP server's `main.py`.
   - Check the extension path in Goose settings for the `uv run /path/to/main.py` command.


If the MCP server isn't behaving as expected, check the terminal output where the API is running for any error messages or output that might indicate what went wrong. You can also check the logs in the Goose Desktop application for any errors related to the MCP server. You can find those logs in the "Logs" section of the Goose Desktop application.
