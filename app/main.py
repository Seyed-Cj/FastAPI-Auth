from fastapi import FastAPI
from app.core.db import Base, engine
from app.modules.auth import routes as auth_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Modular Auth")

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    return {"msg": "ok"}