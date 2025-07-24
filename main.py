from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.routes import auth, expenses, reports
from app.utils.exceptions import (
    http_exception_handler, 
    validation_exception_handler, 
    general_exception_handler
)

app = FastAPI(
    title=settings.APP_NAME,
    description="RESTful API for tracking personal expenses with AI-powered insights",
    version=settings.VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this based on your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    close_mongo_connection()

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(expenses.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")



@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": settings.APP_NAME,
        "version": settings.VERSION,
        "docs": "/docs" if settings.DEBUG else "Documentation disabled in production"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "expense-tracker-api",
        "version": settings.VERSION
    }
    
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)