# routers/leaderboard.py — All leaderboard API routes
from fastapi import APIRouter, Request
from rate_limit import limiter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.player import Player
from schemas.player import PlayerInput, PlayerResponse

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


# ── POST /leaderboard/add ────────────────────────────────────────────────
# Frontend sends: { "username": "Alice", "score": 9500 }
# Saves to DB and returns the saved player
@router.post("/add", response_model=PlayerResponse)
@limiter.limit("5/hour")
def add_player(request: Request, data: PlayerInput, db: Session = Depends(get_db)):

    player = db.query(Player).filter(
        Player.username == data.username
    ).with_for_update().first()

    if player:
        # Add new score to existing score
        player.score += data.score

        db.commit()
        db.refresh(player)

        return player

    # Create a new player if username does not exist
    new_player = Player(
        username=data.username,
        score=data.score
    )

    db.add(new_player)      # add to session
    db.commit()             # save to database
    db.refresh(new_player)  # get updated data (like auto id)

    return new_player
# ── GET /leaderboard/ ────────────────────────────────────────────────────
# Returns all players sorted by score (highest first)
# Frontend uses this to display the leaderboard
from sqlalchemy import desc

@router.get("/", response_model=list[PlayerResponse])

def get_leaderboard(db: Session = Depends(get_db)):
    players = db.query(Player).order_by(Player.score.desc()).all()
    return players


# ── DELETE /leaderboard/{player_id} ─────────────────────────────────────
# Removes a player from the leaderboard by their ID
@router.delete("/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        return {"error": "Player not found"}
    db.delete(player)
    db.commit()
    return {"message": f"Player {player.username} deleted successfully"}
