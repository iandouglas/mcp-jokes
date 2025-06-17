# Welcome to the Toronto Machine Learning Summit workshop!

This workshop is designed as a code-along session where you will learn how to set up and run an MCP server that interacts with a RESTful API, and how to integrate it with the MCP server for use with [Codename Goose](https://block.github.io/goose).

## Workshop Agenda

The workshop will begin with some background on MCP and some of the mechanisms used to connect with other compute systems like APIs and a demo of the MCP server in action.

Next, we'll get everyone to download and install the Goose Desktop application, and register with a QR code for some LLM credits through OpenRouter. These credits should be more than enough to get us through our workshop, and will expire shortly after the workshop ends.

We'll wrap up this part by getting everyone running the joke API server.
From there, we'll break everything into about 15-minute segments where we review the work so far, talk about what's next, and then code the work together. We'll instruct Goose to restart the MCP server periodically as we work through the code.

1. Run our Joke API server, and get a simple MCP server running, and activate it in Goose and have Goose verify that the MCP server is working
2. Add MCP control to get a joke from our API server
3. Add MCP controls to search for jokes by keyword or topic, with and without a count
4. Add MCP controls to add and delete jokes

## I value your feedback!

Please provide feedback on the workshop during breaks or at the end of the workshop. If you've enjoyed it, please consider leaving a note on social media, and tag me and our team at Block:
- https://x.com/iandouglas736, https://x.com/blockopensource
- https://bsky.app/profile/iandouglas736.com, https://bsky.app/profile/opensource.block.xyz
- https://youtube.com/@iandouglas, https://youtube.com/@blockopensource

You can also find all of our collective open source work on GitHub:
- https://github.com/iandouglas, https://github.com/block

## Acknowledging that Humour is Subjective

I've always been around corny jokes and riddles, and my kids love "dad jokes". I do acknowledge, though, that humour is subjective, and the "wordplay" with the English language may not translate well to other languages or cultures. Please do provide feedback if any jokes provided in this workshop feel inappropriate and I will do my best to find alternatives that are more inclusive and appropriate for everyone.

## Would you like a Goose keychain?

I have a limited quantity of some fun 3D-printed keychains to give away to participants in this workshop. If you'd like one, please come see me at the end of the workshop, and I'll be happy to give you one while supplies last.

The design is by [ilya91](https://patreon.com/FlexyToys) and can be found here if you'd like to make your own: https://makerworld.com/en/models/749098-flexi-funny-goose#profileId-682552

![goose keychain](https://makerworld.bblmw.com/makerworld/model/US82a4db4e6cdc29/design/2024-11-01_1608f34ba589c.jpeg?x-oss-process=image/resize,w_1000/format,webp)

Note that these are not "official" Block merchandise, I'm just a nerd for 3D printed things and wanted to share these with everyone :)

---

# The Workshop Steps

While the workshop is meant to be a work-together format, you're welcome to work at your own pace. This git repo also has several branches for each step of our build process. If you ever feel stuck or lost, you can save your work in a different git branch, check out the next sections' branch, and you'll be back up and running!

As we work, we'll probably be prompting Goose to "try an enable the extension again" quite a lot.

> IMPORTANT TIP:
>
> Everyone's learning style is different, but the muscle memory of writing the code by hand will help your understanding of what we're building. You can certainly copy-and-paste the code if you like, but you'll be finished the workshop in about 10 minutes :)
>
> As such, I highly encourage you to write the CODE along with me as I explain what's happening so you can go build your own MCP servers with a deeper understanding of why things work the way they do.
>
> I do provide "docblocks" in the work below, and you're welcome to copy/paste that to save time. The dockblocks provide vital information to MCP clients like Goose, but you don't need to type that out yourself. :)

## Nobody is Left Behind!

If you get stuck on a step, don't worry! This is a workshop, and we're all here to learn together. If you find yourself stuck on a step, you can ask for help, or you can save your work in a separate git branch and then check out the next branch to get you caught up to the next step!

To save your work:
```bash
$ git co -b my-new-branch
$ git add .
$ git commit -m"this is where i got stuck"
```

Later, you can always check your branch versus the next checkpoint to see where things went wrong:

```bash
$ git co branch-01-getting-started
$ git diff my-new-branch
```

This will produce a "diff" format of the expected code and the code you were writing so you can see what happened.

## Step 1: Getting Started

The associated git branch if you get stuck here is called `branch-01-getting-started`.

In this section we're going to get a basic MCP server up and running and make sure that Goose can activate the extension. 

1. Run the Jokes API

    First, we need to make sure the jokes API server is running. If you haven't already, open a separate terminal window (and leave it open during the workshop) and run the jokes API server inside the `jokes_api` directory:

    ```bash
    cd jokes_api
    uv run main.py
    ```

    (the first time you run this command, it will take a few moments to download and install the required packages)

    You can confirm the joke API is running by opening a terminal and running the following command:

    ```bash
    curl http://localhost:8000/status
    ```

2. Let's tweak our `manifest.json` file
   The manifest file will help instruct our AI Agents how to run our MCP server, so we need to make sure the manifest is pointing to the correct path for your MCP server. This is the file that Goose will run to start your MCP server.

    Change the line of your manifest.json file that looks like this:

    ```json
        "cwd": "/TODO/path/to/jokes_mcp"
    ```

    to point to the correct disk path on your system.

> All other work in the workshop session will be done only in the `main.py` file after this.

3. Configure the MCP server to call the API's status check
    In `main.py`, we have some starter code with a status check on our API's `/status` endpoint that Goose can use to verify that our MCP server is running and that the MCP server can connect to the jokes API.

    Verify that `main.py` is going to connect to the jokes API by setting the hostname or IP address, and the port number
    ```python
    API_HOSTNAME = "localhost"
    API_PORT = 8000
    ```

4. Create an MCP 'resource' to call our status check endpoint:
   ```python
    @mcp.resource("resource://status")
    def get_mcp_status() -> Dict:
        try:
            response = requests.get(f"http://{API_HOSTNAME}:{API_PORT}/status", timeout=5)
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error checking MCP status: {e}")
            return {"error": str(e)}
   ```

5. Add a "docblock" to our resource
   FastMCP will transmit any information in the function comments, known as a "documentaiton block" or "docblock" to an MCP client to give it the full context of what the resource or tool is for, how to use it, etc.. The more information we can provide here, the better the AI Agents will be able to use our MCP server.

   ```python
    @mcp.resource("resource://status")
    def get_mcp_status() -> Dict:
        """
        Check if the MCP server is running and can access 
        our API.

            This endpoint verifies the status of the MCP
            server by making a simple request to a known 
            resource. If the server responds correctly, it 
            is considered "up" and will tell you how many 
            jokes it has available.

        Returns:
            Dict: A dictionary containing the status and 
            number of jokes available.

        Example:
            status = read_resource("resource://status")
            # {"status":"running","jokes_count":35}
        """
        try:
            ...
        except ...
   ```

5. Let's run the MCP server!
   Now that we have our MCP server set up, we can run it. In the terminal where you have the jokes API running, open a new terminal window and run the following command:

   ```bash
   uv run main.py
   ```
   (the first time you run this command, it will take a few moments to download and install the required packages)

   To stop the MCP process, you can try `Ctrl-C` in the terminal window where you started it, or you try `Ctrl+\`.

6. Add the Goose extension
   In Goose, click on the 'gear' icon or use the menu to go into the settings. Click on 'Advanced Settings' and scroll down until you see a button that says "Add custom extension". Click on that button and fill in the following information:
    - **Name**: Jokes
    - **Type**: STDIO
    - **Description**: Access jokes from a RESTful API
    - **Command**: `uv run /path/to/jokes_mcp/main.py`
      - note: if `uv` is not in your PATH, you may need to use the full path to the `uv` command, such as `/usr/local/bin/uv` or wherever it is installed on your system, like `/path/to/uv run /path/to/jokes_mcp/main.py`
    Click "Save Changes", scroll to the very top of the window and click the "back" link.

7. Ask Goose to enable the extension
   In the main Goose window, ask Goose to "enable the jokes extension and tell me what the status check responds with".
   We should see a response like this:
   ```text
    Based on the status check, the jokes extension is:
    Status: running
    Number of jokes in the collection: 36
    ```

## Step 2: Getting a Joke

The associated git branch if you get stuck here is called `branch-02-get-a-joke`.

Alright, now we're getting into the good stuff! In this section, we're going to add a resource to our MCP server that will allow us to get a random joke from the jokes API.

All work in this section will be done in the MCP server's `main.py` file.

1. Add the following code to main.py:
   ```python
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
    ```
2. Restart the extension and test it
   In Goose, ask it to "restart the jokes extension and tell me a random joke". You should see a response like this:
   ```text
    Here's your random joke:

    I just broke up with my mathematician girlfriend. She was obsessed with an X.
    ```
    If you don't see a joke, tell Goose to "make sure I can see the joke output in your response".

## Step 3: Searching for Jokes by keyword or topic

The associated git branch if you get stuck here is called `branch-03-search-jokes`.

All work in this section will be done in the MCP server's `main.py` file.

Now we'll add some resources to fetch jokes based on a search term. The search query will look at words in the jokes as well as the 'topics' of the jokes. The second resource we are going to add will take a 'count' parameter to limit the number of jokes returned.

We could do this as a single resource and take an optional parameter, but it's more direct to have two separate resources for this so the AI agent doesn't have to guess so much about what to do.

1. Add thie code to `main.py`:
   ```python
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
        return _search_jokes(query, 1)

    @mcp.resource("resource://jokes/search/{query}/{count}")
    def search_multiple_jokes(query: str, count: int) -> List[str]:
        return _search_jokes(query, count)
   ```

   Here are the dockblocks for the two resources:
   ```python
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
        ...

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
        ...
   ```

2. Test the new resources:
    In Goose, ask it to restart the extension and then "search for a joke about animals" and then "search for 3 jokes about animals". You should see responses like this:
    
    ```text
    Here's an animal-related joke for you:

    How do cows stay up to date? They read the Moo-spaper.
    ```

    Then, ask Goose for 3 jokes about animals. You should see a response like this:

    ```text
    Here are 3 animal-related jokes:

    1. How do cows stay up to date? They read the Moo-spaper.
    2. What do you call a beehive without an exit? Unbelievable.
    3. If I ever find the doctor who screwed up my limb replacement surgery, 
       I'll kill him with my bear hands.
    ```

## Step 4: Add a joke, Get by ID, Delete by ID

The associated git branch if you get stuck here is called `branch-04-final-steps`.

All work in this section will be done in the MCP server's `main.py` file.

This next section will implement MCP "tools" to add a joke (which will return an ID value), get a joke by ID, and delete a joke by ID.

1. Add this code to `main.py`:
    ```python
    @mcp.resource("resource://joke/{joke_id}")
    def get_joke_by_id(joke_id: int) -> str:
        response = requests.get(f"http://{API_HOSTNAME}:{API_PORT}/joke/{joke_id}")

        if response.status_code == 200:
            joke_data = response.json()
            return joke_data["joke"]
        else:
            return f"Failed to retrieve joke {joke_id}"

    @mcp.tool("add_joke")
    def add_joke(joke_text: str, topics: list[str]) -> str:
        response = requests.post(
            f"http://{API_HOSTNAME}:{API_PORT}/joke",
            json={"joke": joke_text, "topics": topics}
        )
        
        if response.status_code == 201:
            joke_data = response.json()
            return f"Added joke with ID {joke_data['id']}"
        else:
            return f"Failed to add joke. Status: {response.status_code}"

    @mcp.tool("delete_joke")
    def delete_joke(joke_id: int) -> str:
        try:
            response = requests.delete(f"http://{API_HOSTNAME}:{API_PORT}/joke/{joke_id}")

            if response.status_code == 200:
                return f"Successfully deleted joke {joke_id}"
            elif response.status_code == 404:
                return f"Joke {joke_id} not found"
            else:
                return f"Failed to delete joke {joke_id}. Error: {response.text}"
                
        except requests.RequestException as e:
            logger.error(f"Network error while deleting joke {joke_id}: {e}")
            return f"Network error while trying to delete joke {joke_id}"
            return f"Failed to delete joke {joke_id}. Status: {response.status_code}"

   ```

   Here are the docblocks:

    ```python
    def get_joke_by_id(joke_id: int) -> str:
        """
        Get a specific joke by its ID.
        
        Retrieves a joke with a specific ID. This is useful when you want to
        reference a particular joke or verify a joke was added successfully.
        
        Args:
            joke_id (int): The ID of the joke to retrieve
        
        Returns:
            str: The joke text if found, otherwise an error message
        
        Example:
            # Get joke with ID 42
            joke = read_resource("resource://joke/42")
        """
        ...

    def add_joke(joke_text: str, topics: list[str]) -> str:
        """
        Add a new joke to the collection.
        
        Creates a new joke in the collection with the provided text and topics.
        The joke will be assigned a unique ID which is returned in the response.
        
        Args:
            joke_text (str): The text of the joke
            topics (list[str]): List of topics/categories for the joke
        
        Returns:
            str: A confirmation message with the joke ID or error message
        
        Example:
            result = add_joke(
                joke_text="Why did the function go to therapy? It had too many complex issues.",
                topics=["programming", "therapy", "puns"]
            )
            # Returns: "Added joke with ID 43"
        """
        ...
    
    def delete_joke(joke_id: int) -> str:
        """
        Delete a joke from the collection by its ID.
        
        Permanently removes a joke from the collection. This action cannot be undone.
        
        Args:
            joke_id (int): The ID of the joke to delete
        
        Returns:
            str: A confirmation message or error message
        
        Example:
            result = delete_joke(42)
            # Returns: "Successfully deleted joke 42"
        """
    ```

2. Test the work
   Ask Goose to reset the extension one more time and to test the integration. Example prompts would include:
   ```
   Add a new joke about the day of the week, and choose some topics to assign to the joke.
   ```
   ```
   Fetch joke number 14
   ```
   ```
   Delete joke number 22
   ```

## Full, complete code

The full, final project can be found in the branch called `branch-05-complete`.

This branch will have the final completed code for the MCP server, including all of the resources and tools we built together in this workshop.

