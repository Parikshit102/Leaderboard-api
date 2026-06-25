# main.py — Entry point of the FastAPI app
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from rate_limit import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import leaderboard

# Create all tables in the database on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Competitive Leaderboard API")

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

# ── CORS — allows frontend to talk to this backend ──────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000"],        # In production, replace * with your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register routers ─────────────────────────────────────────────────────
app.include_router(leaderboard.router)
app.add_middleware(SlowAPIMiddleware)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = []

    for error in exc.errors():
        errors.append(error["msg"])

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "msg": "add in range 1 - 1000"
        }
    )
@app.get("/")
def root():
    return {"message": "Leaderboard API is running!"}
