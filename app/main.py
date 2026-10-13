from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.db.base import Base, load_models
from app.db.session import engine

# Convenient for local development. Use Alembic migrations for production deployments.
load_models()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
register_exception_handlers(app)
app.include_router(api_router, prefix="/api/v1")

FRONTEND = Path(__file__).parent / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND), name="static")

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND / "index.html")

@app.get("/login", include_in_schema=False)
def login_page():
    return FileResponse(FRONTEND / "login.html")

@app.get("/cart", include_in_schema=False)
def cart_page():
    return FileResponse(FRONTEND / "cart.html")

@app.get("/health")
def health():
    return {"status": "ok"}
