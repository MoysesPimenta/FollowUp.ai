"""Minimal API implementation for FollowUp.ai backend."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root() -> dict[str, str]:
    """Return a basic health check payload."""
    return {"status": "ok"}
