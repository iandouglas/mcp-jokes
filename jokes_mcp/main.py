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

@mcp.resource("resource://joke")
def get_random_joke() -> str:
    """
    Get a random joke from the collection.

    This endpoint fetches a completely random joke from the entire collection,
    regardless of topic or content. Each call will likely return a different joke.

    Returns:
        str: A random joke text

    Example:
        joke = read_resource("resource://joke")
        # "Why did the programmer quit his job? Because he didn't get arrays!"
    """
    response = requests.get(f"http://{API_HOSTNAME}:{API_PORT}/joke")

    if response.status_code == 200:
        joke_data = response.json()
        return joke_data["joke"]
    return "Failed to retrieve joke."

def _search_jokes(query: str, count: int) -> List[str]:
    """Helper function to handle the actual joke search request"""
    logger.info(f"Searching for {count} jokes matching: {query}")

    try:
        response = requests.get(
            f"http://{API_HOSTNAME}:{API_PORT}/joke/search",
            params={"q": query, "count": count},
            timeout=5
        )

        if response.status_code == 200:
            jokes_data = response.json()
            return [joke["joke"] for joke in jokes_data]
        else:
            logger.error(f"Search failed with status {response.status_code}")
            return [f"Failed to retrieve jokes. Status: {response.status_code}"]

    except requests.RequestException as e:
        logger.error(f"Request failed while searching for jokes: {e}")
        return [f"Failed to retrieve jokes due to network error"]

@mcp.resource("resource://jokes/search/{query}")
def search_one_joke(query: str) -> List[str]:
    """
    Search for a single joke containing the query string.

    Parameters:
        query: Search term to find in joke text or topics

    Returns:
        List containing one matching joke text

    Example:
        # Get one joke about animals
        jokes = read_resource("resource://jokes/search/animals")
        # Returns: ["Why don't cats like online shopping? They prefer a cat-alog!"]
    """
    return _search_jokes(query, 1)

@mcp.resource("resource://jokes/search/{query}/{count}")
def search_multiple_jokes(query: str, count: int) -> List[str]:
    """
    Search for multiple jokes containing the query string.

    Parameters:
        query: Search term to find in joke text or topics
        count: Number of jokes to return

    Returns:
        List of matching joke texts

    Example:
        # Get three jokes about animals
        jokes = read_resource("resource://jokes/search/animals/3")
        # Returns: ["joke1", "joke2", "joke3"]
    """
    return _search_jokes(query, count)

if __name__ == "__main__":
    logger.info("Starting MCP Server...")
    try:
        mcp.run()
    except Exception as e:
        logger.error(f"Server error: {e}")
