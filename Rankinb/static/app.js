// static/app.js — All FastAPI calls are made from here

const BASE_URL = "http://127.0.0.1:8000";  // FastAPI backend URL

let players = [];

// ── ON PAGE LOAD: fetch all players from FastAPI ─────────────────────────
// API CALL → GET /leaderboard/
// FastAPI returns all players sorted by score from database
async function loadPlayers() {
  try {
    const res = await fetch(`${BASE_URL}/leaderboard/`);
    if (!res.ok) throw new Error(`Error ${res.status}`);
    players = await res.json();   // store players from DB
    renderLeaderboard();
  } catch (e) {
    console.error("Failed to load players:", e.message);
  }
}

// ── ADD PLAYER: send new player to FastAPI ───────────────────────────────
// API CALL → POST /leaderboard/add
// FastAPI saves player + score to database and returns saved record

async function addPlayer() {
  const name  = document.getElementById("player-name").value.trim();
  const score = parseInt(document.getElementById("player-score").value);
  const status = document.getElementById("add-status");

  if (!name || isNaN(score)) {
    status.textContent = "Please enter a name and valid score.";
    status.className = "status error";
    return;
  }

  try {
    status.textContent = "Saving...";
    status.className = "status";

    // API CALL → POST /leaderboard/add
    const res = await fetch(`${BASE_URL}/leaderboard/add`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: name, score })
    });
     const result = await res.json();

    if (!res.ok) {
        status.textContent = result.msg;
        status.className = "status error";
        return;
    }

   
    await loadPlayers();

    document.getElementById("player-name").value  = "";
    document.getElementById("player-score").value = "";
    status.className = "status success";
    setTimeout(() => status.textContent = "", 3000);

  } catch (e) {
    status.textContent = e.message || "Failed to add player.";
    status.className = "status error";
  }
}

// ── RENDER: display players in the leaderboard table ─────────────────────
function renderLeaderboard() {
  const body = document.getElementById("leaderboard-body");

  if (players.length === 0) {
    body.innerHTML = `<div class="empty">No players yet — add one above</div>`;
    document.getElementById("total-players").textContent = "0";
    document.getElementById("top-score").textContent     = "—";
    document.getElementById("avg-score").textContent     = "—";
    return;
  }

  const rankIcon = (i) => i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : `#${i + 1}`;

  body.innerHTML = players.map((p, i) => `
    <div class="leaderboard-row">
      <div class="rank">${rankIcon(i)}</div>
      <div class="player-name">${p.username}</div>
      <div class="score">${p.score.toLocaleString()}</div>
      <div class="date">${formatDate(p.created_at)}</div>
    </div>
  `).join("");

  const total = players.length;
  const top   = players[0].score;
  const avg   = Math.round(players.reduce((s, p) => s + p.score, 0) / total);

  document.getElementById("total-players").textContent = total;
  document.getElementById("top-score").textContent     = top.toLocaleString();
  document.getElementById("avg-score").textContent     = avg.toLocaleString();
}

// ── HELPER: format date string ────────────────────────────────────────────
function formatDate(value) {
  if (!value) return "—";
  const d = new Date(value);
  return isNaN(d) ? value : d.toLocaleDateString();
}

// Load players when page opens
loadPlayers();
