# main.py — Entry point of the FastAPI app

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import leaderboard

# Create all tables in the database on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Competitive Leaderboard API")

# ── CORS — allows frontend to talk to this backend ──────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # In production, replace * with your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register routers ─────────────────────────────────────────────────────
app.include_router(leaderboard.router)


@app.get("/")
def root():
    return {"message": "Leaderboard API is running!"}
