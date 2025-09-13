import asyncio
import time
import httpx
from sqlalchemy import select
from . import models

async def simulate_slow_io_operation(seconds: float = 1.0):
    """Simulate a slow I/O operation (e.g., database query, API call)"""
    print(f"Operation started. Will take {seconds} seconds...")
    await asyncio.sleep(seconds)  # Non-blocking sleep
    print("Operation finished!")
    return f"Result after {seconds} seconds"

def simulate_cpu_intensive_task(iterations: int = 10000000):
    """Simulate a CPU-intensive task (blocking!)"""
    print(f"CPU task started. Will process {iterations} iterations...")
    result = 0
    for i in range(iterations):
        result += i * i  # Some computation
    print("CPU task finished!")
    return f"Computed result: {result}"

async def fetch_external_api(url: str, timeout: float = 5.0):
    """Fetch data from an external API asynchronously"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=timeout)
            return response.json()
    except Exception as e:
        return {"error": str(e)}

async def get_user_by_email(db, email: str):
    """Async database query example"""
    result = await db.execute(
        select(models.User).where(models.User.email == email)
    )
    return result.scalar_one_or_none()

async def create_user(db, user_data: dict):
    """Async database insert example"""
    db_user = models.User(**user_data)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user