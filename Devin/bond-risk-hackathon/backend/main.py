import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import bonds, portfolio

app = FastAPI(title="Bond Risk API")

ALLOWED_ORIGINS = [
    o.strip()
    for o in os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(bonds.router)
app.include_router(portfolio.router)


@app.get("/")
def root():
    return {"status": "ok"}
