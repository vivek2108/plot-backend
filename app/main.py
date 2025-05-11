import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.api import auth_router, buyers, users, plots
from app.config.database import Base, engine

# Setting up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,  # Set level to INFO or DEBUG for more detailed logs
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add GZipMiddleware for compressing responses of size > 1400 bytes
app.add_middleware(GZipMiddleware, minimum_size=1400)

# Configure CORS middleware for allowing cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,  # Allow cookies and credentials
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include routers for authentication, users, and buyers
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(buyers.router, prefix="/buyers", tags=["buyers"])
app.include_router(plots.router, prefix="/plots", tags=["plots"])

# Create all database tables defined in the Base class
Base.metadata.create_all(bind=engine)

logger.info("FastAPI application started and database tables created.")
