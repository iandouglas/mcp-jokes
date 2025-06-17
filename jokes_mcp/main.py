"""
Jokes MCP Extension
------------------
A humor extension that provides access to a collection of jokes.

This MCP server connects to a local jokes API to provide various joke-related
functionality including random jokes, searching, and joke management.

Resources:
- resource://status - is the MCP server running properly?
- resource://joke - Get a random joke
- resource://joke/{joke_id} - Get a specific joke by ID
- resource://jokes/search/{query} - Search for a single random matching joke
- resource://jokes/search/{query}/{count} - Get multiple matching jokes

Tools:
- add_joke - Add a new joke with text and topics
- delete_joke - Remove a joke by ID

The server expects the jokes API to be running on localhost:8000
"""

from fastmcp import FastMCP
from typing import List, Dict
import requests
import logging
from typing import List, Optional

API_HOSTNAME = "localhost"
API_PORT = 8000

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP(name="")


if __name__ == "__main__":
    logger.info("Starting MCP Server...")
    try:
        mcp.run()
    except Exception as e:
        logger.error(f"Server error: {e}")
