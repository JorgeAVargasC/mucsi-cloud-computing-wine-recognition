"""REST microservice that exposes the wine model through FastAPI."""

from fastapi import FastAPI

app = FastAPI(title="Wine Recognition API")


@app.get("/")
def health_check() -> dict:
    """Confirms the service is running."""
    return {"status": "ok"}
