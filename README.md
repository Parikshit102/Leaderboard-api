For your leaderboard project, you don't need a very complex system design. Recruiters usually expect a simple but well-thought-out architecture.

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

This design is more than sufficient for a backend assignment and should impress recruiters because it shows both the current implementation and how it can scale in production.

Challenges - First to integerate backend with frontend properly .
Second is I have time limit that's why I can't able to give full focus on this project.
