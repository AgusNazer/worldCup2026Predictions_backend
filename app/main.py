import os
from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.matches import router as matches_router
from app.routes.predictions import router as predictions_router
from app.routes.rankings import router as rankings_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="World Cup Prediction API",
    description="API para predicciones públicas del Mundial. Visitantes anónimos o usuarios registrados.",
    version="1.0.0",
)

# CORS - Restrict to frontend origin only
print("CORS_ORIGINS =", os.getenv("CORS_ORIGINS"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


app.include_router(auth_router)
app.include_router(matches_router)
app.include_router(predictions_router)
app.include_router(rankings_router)

@app.get("/")
def home():
    return {"message": "World Cup Predictor API"}