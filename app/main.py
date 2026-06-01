import os
from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.matches import router as matches_router
from app.routes.predictions import router as predictions_router
from app.routes.rankings import router as rankings_router

from fastapi.middleware.cors import CORSMiddleware

#para probar endpoint de la db, borrar la funcion luego del deploy en produccion
from app.seeds.matches_2026 import seed_matches
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="World Cup Prediction API",
    description="API para predicciones públicas del Mundial. Visitantes anónimos o usuarios registrados.",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins_raw = os.getenv("CORS_ORIGINS", "http://localhost:3000,https://worldcup26predictors.netlify.app,https://worldcup26.anuarnazer.com")
allow_origins = [o.strip() for o in origins_raw.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
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


@app.get("/health")
@app.head("/health")
def health():
    return {"status": "ok"}

