from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .models import User, LoginLog  # noqa: F401 — registers models with SQLAlchemy Base
from .routers import auth, logs

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Login Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(logs.router)


@app.get("/")
def root():
    return {"message": "Login Tracker API is running"}
