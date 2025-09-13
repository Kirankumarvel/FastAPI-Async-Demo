# FastAPI Async Programming: Handling Thousands of Requests Efficiently

A complete FastAPI project demonstrating async/await, async database operations, concurrent external API calls, background tasks, and performance comparisons between async and sync approaches.

---

## 📁 Project Structure

```
fastapi-async-demo/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── utils.py
├── requirements.txt
└── README.md
```

---

## 🚀 Features

- 🚦 Async/await endpoints for non-blocking I/O
- 🗄️ Async database operations (PostgreSQL or SQLite with SQLAlchemy 1.4+)
- 🌐 Concurrent external API calls using httpx
- ⚡ Performance comparison: async vs sync
- 🔄 Background tasks for CPU-intensive work
- 🧪 Health check and practical demos

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.7+
- pip

---

### 1. Create and Set Up Project

```bash
mkdir fastapi-async-demo
cd fastapi-async-demo
python -m venv venv
```

Activate your environment:
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> **requirements.txt**
> ```
> fastapi==0.104.1
> uvicorn[standard]==0.24.0
> sqlalchemy==2.0.23
> asyncpg==0.29.0
> httpx==0.25.2
> aiosqlite==0.19.0
> python-multipart==0.0.6
> pydantic==2.5.0
> ```

---

### 3. Project Files

- Place Python files as described in the **Project Structure** above.
- You can copy the code from this README or the full file blocks.

---

### 4. Run the Application

```bash
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

### 5. Open the API Docs

- [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)
- [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🎯 Practical Exercises

### 1. Test Async vs Sync Delay

- Open two browser tabs.
- Tab 1: `http://localhost:8000/async-delay/3`
- Tab 2: `http://localhost:8000/async-delay/2`
  - Both will complete around the same time (async concurrency!).
- Try the same with `/sync-delay/3` and `/sync-delay/2` (tab 2 will wait for tab 1 to finish).

### 2. Performance Comparison

- `GET /performance/async` → Should take ~1s (concurrent)
- `GET /performance/sync` → Should take ~3s (sequential)

### 3. Database Operations

- Create a user: `POST /users/` (e.g., `{"email": "test@example.com", "full_name": "Test User"}`)
- Get user by email: `GET /users/test@example.com`

### 4. External API Calls

- `GET /fetch-external-data` → Fetch from multiple APIs concurrently
- `GET /user-with-external-data/{user_email}` → Combines database + external API in one async endpoint

### 5. Background Tasks

- `POST /process-data/any_message` → Simulates CPU work in the background

---

## 🔗 API Endpoints

| Method | Endpoint                                 | Description                               |
|--------|------------------------------------------|-------------------------------------------|
| GET    | `/`                                      | Welcome message                           |
| GET    | `/async-delay/{seconds}`                 | Async non-blocking delay                  |
| GET    | `/sync-delay/{seconds}`                  | Sync (blocking!) delay                    |
| POST   | `/users/`                                | Async user creation                       |
| GET    | `/users/{user_email}`                    | Async user lookup by email                |
| GET    | `/fetch-external-data`                   | Concurrent external API calls             |
| GET    | `/user-with-external-data/{user_email}`  | DB + external API (full async chain)      |
| POST   | `/process-data/{message}`                | Background CPU task                       |
| GET    | `/performance/async`                     | Concurrent async performance test         |
| GET    | `/performance/sync`                      | Sequential async performance test         |
| GET    | `/health`                                | Health check                              |

---

## ⚡ How Async Works in FastAPI

- `async def` endpoints run non-blocking code (e.g., `await asyncio.sleep`, async DB, async HTTP).
- I/O-bound tasks (DB, network) get **concurrency** for free with async/await.
- CPU-bound tasks should use `BackgroundTasks` or a process/thread pool.

---

## 🧪 Load Testing (Optional)

**Example: Simulate concurrent requests**

```python
# test_async.py
import asyncio, httpx, time

async def make_request(client, url):
    start = time.time()
    resp = await client.get(url)
    return {"url": url, "status": resp.status_code, "time": time.time() - start}

async def main():
    urls = ["http://localhost:8000/async-delay/2"] * 3
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(*(make_request(client, u) for u in urls))
        for r in results:
            print(r)

if __name__ == "__main__":
    asyncio.run(main())
```

Run: `python test_async.py`  
See how all requests finish in ~2 seconds!

---

## 🛡️ Production Considerations

- Use **PostgreSQL** with `asyncpg` for best performance.
- Set up **connection pooling** for async DB.
- Monitor event loop with tools like `uvicorn --loop uvloop`.
- Use a reverse proxy (nginx, Caddy) for SSL, timeouts, etc.
- Never use sync I/O (e.g., `time.sleep`) in async endpoints!

---

## 🐞 Common Pitfalls

- Blocking the event loop with sync code (e.g., `time.sleep`, heavy computation)
- Not using `await` with async functions
- Not closing async DB sessions
- Forgetting to activate the virtual environment
- Wrong working directory (must be project root!)

---

## 📚 Further Reading

- [FastAPI Async Docs](https://fastapi.tiangolo.com/async/)
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html)

---

## ✅ Quickstart

1. Install dependencies: `pip install -r requirements.txt`
2. Run: `uvicorn app.main:app --reload`
3. Visit: [http://localhost:8000/docs](http://localhost:8000/docs)
4. Try `/async-delay/2` and `/performance/async` for async magic!

---

**This demo shows how FastAPI's async capabilities enable massive concurrency and efficient resource usage—even for thousands of simultaneous requests.** 🚀
