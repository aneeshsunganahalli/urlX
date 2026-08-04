# urlX

urlX is a simple URL shortener built with FastAPI. It lets you create short links, redirect them to their original destinations, and collect basic analytics for clicks.

---

![Architecture](/images/Architecture.png)

## Features

- Create short URLs from long URLs
- Redirect short links to the original target
- Basic click analytics using user-agent data
- Health checks for the database and Redis
- Cache-based redirect lookup for faster responses

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Pydantic settings

## Getting Started

1. Install dependencies:

   ```bash
   pip install -r app/requirements.txt
   ```

2. Create a `.env` file in the project root with the required settings:

   ```env
   worker_id=1
   custom_epoch=1704067200
   database_url=postgresql+asyncpg://user:password@localhost:5432/urlx
   client_url=http://localhost:3000
   redis_host=localhost
   redis_port=6379
   redis_db=0
   redis_password=
   ```

3. Start the app:

   ```bash
   cd app
   uvicorn main:app --reload
   ```

## API Endpoints

- `POST /generate` – shorten a URL
- `GET /{short_url}` – redirect to the original URL
- `GET /db/health` – check database health
- `GET /redis/health` – check Redis health
