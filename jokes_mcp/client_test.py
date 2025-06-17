import asyncio
from fastmcp import Client
from typing import List

async def test_random_joke():
    """Test getting a random joke"""
    print("\n=== Testing random joke ===")
    async with Client("main.py") as client:
        result = await client.read_resource("resource://joke")
        print(f"Random joke: {result[0].text}")

async def test_joke_by_id():
    """Test getting a specific joke by ID"""
    print("\n=== Testing joke by ID ===")
    async with Client("main.py") as client:
        # Try getting joke with ID 1
        result = await client.read_resource("resource://joke/1")
        print(f"Joke #1: {result[0].text}")
        
        # Try getting a non-existent joke
        result = await client.read_resource("resource://joke/999")
        print(f"Non-existent joke: {result[0].text}")

async def test_joke_search():
    """Test searching for jokes"""
    print("\n=== Testing joke search ===")
    async with Client("main.py") as client:
        # Test single joke search
        print("\nSingle joke search:")
        result = await client.read_resource("resource://jokes/search/animal")
        print(f"One animal joke: {result[0].text}")
        
        # Test multiple jokes search
        print("\nMultiple jokes search:")
        result = await client.read_resource("resource://jokes/search/programming/2")
        print(f"Two programming jokes: {result[0].text}")

async def test_joke_management():
    """Test adding and deleting jokes"""
    print("\n=== Testing joke management ===")
    async with Client("main.py") as client:
        # Add a new joke
        print("\nAdding new joke:")
        add_result = await client.call_tool(
            "add_joke",
            {
                "joke_text": "Why did the AI go to therapy? It was having an identity crisis!",
                "topics": ["ai", "technology", "therapy"]
            }
        )
        print(f"Add result: {add_result}")
        
        # Extract the ID from the response
        joke_id = int(add_result[0].text.split()[-1])
        
        # Verify the joke was added by retrieving it
        print("\nVerifying added joke:")
        result = await client.read_resource(f"resource://joke/{joke_id}")
        print(f"Retrieved joke {joke_id}: {result[0].text}")
        
        # Delete the joke
        print("\nDeleting joke:")
        delete_result = await client.call_tool(
            "delete_joke",
            {"joke_id": joke_id}
        )
        print(f"Delete result: {delete_result}")
        
        # Verify deletion
        print("\nVerifying deletion:")
        result = await client.read_resource(f"resource://joke/{joke_id}")
        print(f"Attempt to get deleted joke: {result[0].text}")

async def run_all_tests():
    """Run all test functions"""
    test_functions = [
        test_random_joke,
        test_joke_by_id,
        test_joke_search,
        test_joke_management
    ]
    
    for test in test_functions:
        try:
            await test()
        except Exception as e:
            print(f"Error in {test.__name__}: {e}")

if __name__ == "__main__":
    print("Starting MCP Jokes Extension Tests...")
    asyncio.run(run_all_tests())
    print("\nTests completed!")