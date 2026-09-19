from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import bonds, portfolio

app = FastAPI(title="Bond Risk API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(bonds.router)
app.include_router(portfolio.router)


@app.get("/")
def root():
    return {"status": "ok"}
