from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from components.api.v1.api import api_router

app = FastAPI(
    title="Interview Prep AI Platform",
    description="AI-powered interview preparation platform using Gemini 2.0 Flash",
    version="1.0.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Interview Prep AI Platform",
        "status": "online",
        "model": "Gemini 2.0 Flash"
    }

# Include API router
# app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
