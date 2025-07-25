"""Minimal API service for FollowUp.ai."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    """Return a welcome message."""
    return {"message": "FollowUp API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
