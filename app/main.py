from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio
import time

from . import models, schemas, utils
from .database import get_async_db, engine

app = FastAPI(title="FastAPI Async Demo", version="1.0.0")

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

# Example 1: Simple async endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI Async Demo"}

# Example 2: Async endpoint with simulated I/O
@app.get("/async-delay/{seconds}")
async def async_delay(seconds: float = 1.0):
    result = await utils.simulate_slow_io_operation(seconds)
    return {"message": result}

# Example 3: Synchronous endpoint (blocks the event loop!)
@app.get("/sync-delay/{seconds}")
def sync_delay(seconds: float = 1.0):
    # WARNING: This will block the entire event loop!
    time.sleep(seconds)  # Blocking sleep - BAD!
    return {"message": f"Waited {seconds} seconds synchronously"}

# Example 4: Async database operations
@app.get("/users/{user_email}", response_model=schemas.User)
async def get_user(user_email: str, db: AsyncSession = Depends(get_async_db)):
    user = await utils.get_user_by_email(db, user_email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_async_db)):
    # Check if user already exists
    existing_user = await utils.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    db_user = await utils.create_user(db, user.model_dump())
    return db_user

# Example 5: Calling external APIs asynchronously
@app.get("/fetch-external-data")
async def fetch_external_data():
    # Fetch from multiple APIs concurrently
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/comments/1",
        "https://jsonplaceholder.typicode.com/albums/1"
    ]
    
    # All requests happen concurrently!
    tasks = [utils.fetch_external_api(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    return {
        "results": results,
        "message": "Fetched from multiple APIs concurrently"
    }

# Example 6: Handling CPU-bound tasks with BackgroundTasks
@app.post("/process-data/{message}")
async def process_data(message: str, background_tasks: BackgroundTasks):
    # Offload CPU-intensive work to background thread
    background_tasks.add_task(utils.simulate_cpu_intensive_task)
    return {
        "message": "Processing started in background",
        "input": message
    }

# Example 7: Mixed async operations
@app.get("/user-with-external-data/{user_email}")
async def get_user_with_external_data(
    user_email: str, 
    db: AsyncSession = Depends(get_async_db)
):
    # Get user from database (async)
    user = await utils.get_user_by_email(db, user_email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Fetch external data (async)
    external_data = await utils.fetch_external_api(
        "https://jsonplaceholder.typicode.com/posts/1"
    )
    
    return {
        "user": user,
        "external_data": external_data
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "FastAPI Async server is running"}

# Performance comparison endpoints
@app.get("/performance/async")
async def performance_async():
    # Simulate 3 async I/O operations that run concurrently
    start_time = time.time()
    
    # These run concurrently, not sequentially!
    results = await asyncio.gather(
        utils.simulate_slow_io_operation(1.0),
        utils.simulate_slow_io_operation(1.0),
        utils.simulate_slow_io_operation(1.0)
    )
    
    total_time = time.time() - start_time
    return {
        "results": results,
        "total_time": f"{total_time:.2f} seconds",
        "message": "Async operations ran concurrently"
    }

@app.get("/performance/sync")
async def performance_sync():
    # Simulate 3 sync I/O operations that run sequentially
    start_time = time.time()
    
    # These run sequentially, one after another
    result1 = await utils.simulate_slow_io_operation(1.0)
    result2 = await utils.simulate_slow_io_operation(1.0)
    result3 = await utils.simulate_slow_io_operation(1.0)
    
    total_time = time.time() - start_time
    return {
        "results": [result1, result2, result3],
        "total_time": f"{total_time:.2f} seconds",
        "message": "Operations ran sequentially"
    }