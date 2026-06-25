

🏆 Competitive Leaderboard API

A simple leaderboard application built using FastAPI, PostgreSQL, and SQLAlchemy. Users can submit scores and view rankings through a lightweight web interface.

✨ Features
Add new players with scores
View leaderboard rankings
Automatic ranking based on score
Simple and responsive UI
🛠️ Tech Stack
Component	Technology
Backend	FastAPI
Database	PostgreSQL
ORM	SQLAlchemy
Frontend	HTML, CSS, JavaScript
Frontend Server	Flask
📂 Project Structure
project/
│
├── main.py                 # FastAPI entry point
├── database.py             # Database configuration
├── routers/
│   └── leaderboard.py      # API routes
│
├── models/
│   └── player.py           # Database model
│
├── templates/
│   └── index.html          # Frontend page
│
├── static/
│   ├── app.js              # Frontend logic
│   └── style.css           # Styling
│
├── app.py                  # Flask server
└── README.md
 Getting Started
1. Clone the Repository
git clone <your-repository-url>
cd leaderboard-project
2. Create a Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
Linux/Mac
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary flask
4. Configure PostgreSQL

Create a PostgreSQL database:

CREATE DATABASE leaderboard_db;

Update database.py:

DATABASE_URL = "postgresql://username:password@localhost:5432/leaderboard_db"

Example:

DATABASE_URL = "postgresql://postgres:password@localhost:5432/leaderboard_db"
5. Start the FastAPI Server
uvicorn main:app --reload

You should see:

INFO: Uvicorn running on http://127.0.0.1:8000
API Documentation

Open in browser:

http://127.0.0.1:8000/docs
6. Start the Frontend

Open a new terminal and run:

python app.py

Frontend will be available at:

http://127.0.0.1:5000


# Competitive Leaderboard System Design

```text
                         +----------------------+
                         |      User Browser    |
                         | (HTML/CSS/JS UI)     |
                         +----------+-----------+
                                    |
                                    | HTTP Requests
                                    v
                         +----------------------+
                         |      Flask Server    |
                         |  Serves Frontend UI  |
                         +----------+-----------+
                                    |
                                    | REST API Calls
                                    v
                         +----------------------+
                         |    FastAPI Backend   |
                         |                      |
                         |  POST /add          |
                         |  GET  /leaderboard  |
                         +----------+-----------+
                                    |
                                    | SQLAlchemy ORM
                                    v
                         +----------------------+
                         |    SQLite Database   |
                         |                      |
                         |      players         |
                         +----------------------+
```

---

# Request Flow

## Adding a Player

```text
User
  |
  | Enter username + score
  v
Frontend (JavaScript)
  |
  | POST /leaderboard/add
  v
FastAPI
  |
  | Validate request
  | Check duplicate username
  | Create Player object
  v
SQLAlchemy
  |
  | INSERT INTO players
  v
SQLite Database
  |
  | Return saved record
  v
Frontend updates leaderboard
```

---

## Fetching Leaderboard

```text
User opens webpage
          |
          v
JavaScript loadPlayers()
          |
          | GET /leaderboard/
          v
FastAPI
          |
          | Query database
          | ORDER BY score DESC
          v
SQLite
          |
          | Return sorted players
          v
Frontend renders leaderboard
```

---

# High-Level Components

### 1. Frontend Layer

Responsibilities:

* Capture user input.
* Call backend APIs.
* Display rankings.
* Show statistics.

Technology:

* HTML
* CSS
* JavaScript

---

### 2. API Layer

Responsibilities:

* Expose REST endpoints.
* Validate incoming requests.
* Handle business logic.
* Return JSON responses.

Technology:

* FastAPI

Endpoints:

```text
POST /leaderboard/add
GET  /leaderboard/
```

---

### 3. Business Logic Layer

Responsibilities:

* Prevent duplicate usernames.
* Apply ranking logic.
* Manage database transactions.

Example:

```python
players = db.query(Player)\
            .order_by(Player.score.desc())\
            .all()
```

---

### 4. Data Access Layer

Responsibilities:

* Convert Python objects to SQL.
* Interact with database.

Technology:

* SQLAlchemy ORM

---

### 5. Persistence Layer

Responsibilities:

* Store player data permanently.

Technology:

* Potgre sql

Schema:

```text
players
--------
id
username (UNIQUE)
score
created_at
```

---

# Concurrency Design

Current implementation:

```text
Request 1 ---> Session 1 ---> DB
Request 2 ---> Session 2 ---> DB
Request 3 ---> Session 3 ---> DB
```

Every request receives its own SQLAlchemy session.

This prevents multiple requests from sharing the same database session.

---

# Ranking Algorithm

```text
Sort all players by score in descending order.

Highest score -> Rank 1
Second highest -> Rank 2
Third highest -> Rank 3
```

Complexity:

```text
Time Complexity: O(N log N)
```

---

# Scalability Improvements (Production)

If traffic grows:

```text
Browser
   |
Load Balancer
   |
+-----------+-----------+
|                       |
FastAPI Instance 1   FastAPI Instance 2
|                       |
+-----------+-----------+
            |
         PostgreSQL
            |
            |
         Redis Cache
```

Possible improvements:

* Replace SQLite with PostgreSQL.
* Add Redis caching for leaderboard reads.
* Add authentication.
* Add rate limiting.
* Containerize using Docker.
* Deploy behind Nginx.

Challenges - First to integerate backend with frontend properly .
Second is I have time limit that's why I can't able to give full focus on this project.
