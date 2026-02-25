# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import get_settings
from app.api.v1.router import router as api_v1_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

# Allow frontend origins
origins = [
    "http://192.168.0.113:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://192.168.0.103:80"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all v1 routes under /api/v1
app.include_router(api_v1_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Backend root is running"}
