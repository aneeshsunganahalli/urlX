# _urlX_

  _**urlX**_ is a production-inspired URL shortening service focused on scalability, performance, and reliability. It features Redis-backed redirects, PostgreSQL persistence, NGINX load balancing, Dockerized FastAPI services, and asynchronous click analytics to simulate a real-world backend system.

---
![Preview](/docs/images/Preview.png)



---

![Architecture](/docs/images/Architecture.png)

## Features

- **URL Shortening:** Generate compact, collision-resistant short links from long URLs.
- **Fast Redirection:** High-speed redirect engine powered by in-memory caching.
- **Click Analytics:** Lightweight tracking utilizing User-Agent data upon access.
- **Health Monitoring:** Dedicated diagnostic endpoints for PostgreSQL and Redis readiness.
- **Cache-First Lookup:** Minimizes database load by utilizing Redis as an primary read cache.





## Tradeoffs

For my [[URL Shortener]] design, I did not implement a CDN to absorb traffic which is required for an ideal setup, but too much overhead for a small project like this.

#### Why PostgreSQL over a NoSQL Database?
Figured since the principal is to keep the number of times the database is read or written to, should be kept as small as possible and it’s mainly read-heavy, so more than the database itself the architecture surrounding it should be absorbing the more frequent reads. So since I’m using Redis to handle most reads and speed, I went with  PostgreSQL, since I’m more familiar with it, so there’s less overhead.

#### Shortening Implementation
Went with a custom Twitter Snowflake ID inspired method instead of hashing, or purely counting. Counting has security risks and Hashing is just plain bad since collision frequencies even though a friend of mine likes to believe *The simplest method is usually the best one*, but his hashing method just doesn’t cut it for scaling this architecture.

#### Custom Snowflake ID
`24 bit Timestamp | 10 bit Worker ID | 12 bit Sequence Number`

Randomness is increased through this but since I’m using seconds for 24 bit Timestamp, it revolved around every 194 days, since 2^24 seconds = 194 days but that was enough for the sake of this project. After that collision can occur if machine with same ID and same sequence number in that second could be combined with timestamp field 194 days later.


## 🚀 Getting Started

### Prerequisites
Ensure Node.js, Python 3.9+, PostgreSQL, and Redis instances are installed and running locally.

### Backend Setup

1. **Install dependencies:**

   ```bash
   pip install -r app/requirements.txt
   ```

2. **Configure Environment Variables:**

   Create a `.env` file in the project root with the following configuration:

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

3. **Run the Application:**

   ```bash
   cd app
   uvicorn main:app --reload
   ```

### Frontend Setup (Vite)

1. **Install dependencies:**

   ```bash
   cd client
   npm install
   ```

2. **Run the development server:**

   ```bash
   npm run dev
   ```

---
