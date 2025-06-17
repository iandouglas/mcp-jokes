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

mcp = FastMCP(name="jokes")

@mcp.resource("resource://status")
def get_mcp_status() -> Dict:
    """
    Check if the MCP server is running and can access our API.

    This endpoint verifies the status of the MCP server by making a simple request to a known resource. If the server responds correctly, it is considered "up" and will tell you how many jokes it has available.

    Returns:
        Dict: A dictionary containing the status and number of jokes available.

    Example:
        status = read_resource("resource://status")
        # {"status":"running","jokes_count":35}
    """
    try:
        response = requests.get(f"http://{API_HOSTNAME}:{API_PORT}/status", timeout=5)
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error checking MCP status: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    logger.info("Starting MCP Server...")
    try:
        mcp.run()
    except Exception as e:
        logger.error(f"Server error: {e}")
