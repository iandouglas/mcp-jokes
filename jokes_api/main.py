from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union, Optional
import json
import random
import os

app = FastAPI(title="Joke API")

# Data file path
JOKES_FILE = "jokes.json"

# Pydantic models
class JokeBase(BaseModel):
    joke: str
    topics: List[str]

class Joke(JokeBase):
    id: int

class JokeCreate(JokeBase):
    pass

def load_jokes() -> List[Joke]:
    if not os.path.exists(JOKES_FILE):
        return []
    with open(JOKES_FILE, 'r') as f:
        return [Joke(**joke) for joke in json.load(f)]

def save_jokes(jokes: List[Joke]):
    with open(JOKES_FILE, 'w') as f:
        json.dump([joke.model_dump() for joke in jokes], f, indent=2)

def get_next_id() -> int:
    jokes = load_jokes()
    if not jokes:
        return 1
    return max(joke.id for joke in jokes) + 1

@app.get("/status")
async def health_check():
    '''
    send back a status check that the API is running properly
    '''
    jokes = load_jokes()
    return {"status": "running", 'jokes_count': len(jokes)}

@app.get("/joke")
async def get_random_joke() -> Joke:
    '''
    get a random joke
    '''
    jokes = load_jokes()
    if not jokes:
        raise HTTPException(status_code=404, detail="No jokes found")
    return random.choice(jokes)

@app.get("/joke/search", response_model=List[Joke])
async def search_jokes(q: str, count: Optional[int] = 1) -> List[Joke]:
    '''
    Search for jokes containing the query string.
    Returns a list of matching jokes, limited by count if specified.
    '''
    jokes = load_jokes()
    q_lower = q.lower()
    
    matching_jokes = [
        joke for joke in jokes
        if (q_lower in joke.joke.lower() or  
            any(q_lower in topic.lower() for topic in joke.topics))
    ]

    if not matching_jokes:
        raise HTTPException(status_code=404, detail="No matching jokes found")
        
    # If count is larger than available jokes, return all matches
    count = min(count, len(matching_jokes))
    # Randomly select 'count' number of jokes
    return random.sample(matching_jokes, count)

@app.get("/joke/{joke_id}", response_model=Joke) # New endpoint
async def get_joke_by_id(joke_id: int) -> Joke:
    '''
    get a specific joke by its ID
    '''
    jokes = load_jokes()
    for joke in jokes:
        if joke.id == joke_id:
            return joke
    raise HTTPException(status_code=404, detail=f"Joke with ID {joke_id} not found")

@app.post("/joke", status_code=201, response_model=Joke)
async def create_joke(joke: JokeCreate) -> Joke:
    '''
    add a new joke, requires a joke and one or more topics
    '''
    if not joke.joke.strip():
        raise HTTPException(status_code=400, detail="Joke text cannot be empty")
    if not joke.topics:
        raise HTTPException(status_code=400, detail="At least one topic is required")
    
    new_joke = Joke(
        id=get_next_id(),
        joke=joke.joke,
        topics=joke.topics
    )
    
    jokes = load_jokes()
    jokes.append(new_joke)
    save_jokes(jokes)
    return new_joke

@app.delete("/joke/{joke_id}")
async def delete_joke(joke_id: int):
    '''
    remove a joke if you don't like it
    '''
    jokes = load_jokes()
    initial_length = len(jokes)
    jokes = [joke for joke in jokes if joke.id != joke_id]
    
    if len(jokes) == initial_length:
        raise HTTPException(status_code=404, detail=f"Joke with ID {joke_id} not found")
    
    save_jokes(jokes)
    return {"message": f"Joke {joke_id} deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
