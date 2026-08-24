from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import index, search, extract

app = FastAPI(
    title="GovDoc Hub API",
    description="Backend API for local document processing and extraction.",
    version="1.0.0"
)

# CORS middleware for Tauri frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, restrict this to Tauri's local origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(index.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
app.include_router(extract.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "GovDoc Hub Backend is running"}
