from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router

app = FastAPI(title="Medical Research RAG API", version="0.1.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    # Use explicit origins when allow_credentials=True to satisfy CORS
    allow_origins=[
        "https://medical-research-assistant.netlify.app",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)


@app.get("/")
async def root():
    return {"status": "ok", "service": "medical-research-rag"}
