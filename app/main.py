from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users, events, sessions, quizzes, badges

app = FastAPI(title="Stomata Labs Gamification API", version="1.0.0")

# ---------------------------------------------------------
# CORS (allow Streamlit frontend)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------
app.include_router(users.router)
app.include_router(events.router)
app.include_router(sessions.router)
app.include_router(quizzes.router)
app.include_router(badges.router)


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------
@app.get("/health", tags=["System"])
def health_check() -> dict:
    return {"status": "ok"}
