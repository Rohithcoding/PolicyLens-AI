from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.policy_routes import router as policy_router
from api.simulation_routes import router as simulation_router
from utils.config import settings
import uvicorn

app = FastAPI(
    title="PolicyLens AI API",
    description="AI-powered policy analysis and simulation platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(policy_router, prefix="/api/policy", tags=["policy"])
app.include_router(simulation_router, prefix="/api/simulation", tags=["simulation"])

@app.get("/")
async def root():
    return {"message": "PolicyLens AI API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
