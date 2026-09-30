"""
Controller Layer (FastAPI Application)
=====================================
Receives HTTP requests, validates request payloads with Pydantic,
and delegates execution to UserService.

NOTE: This file has ZERO OpenTelemetry code.
Everything is auto-instrumented from the outside!
"""

import logging
from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from database import init_db, get_db
from repository import UserRepository
from service import UserService

# Optional: ship logs to Loki if loki_logger is present
try:
    import loki_logger
except Exception:
    pass

logger = logging.getLogger("user-service")


# ------------------------------------------------------------------------------
# Pydantic Schemas
# ------------------------------------------------------------------------------
class UserCreateRequest(BaseModel):
    name: str
    email: EmailStr
    role: str = "member"


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str


# ------------------------------------------------------------------------------
# Lifespan: Auto-initialize Database Tables
# ------------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure tables exist and seed demo data
    init_db()
    logger.info("Database initialized successfully.")
    yield


# ------------------------------------------------------------------------------
# Dependency Injection: Controller -> Service -> Repository
# ------------------------------------------------------------------------------
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)


app = FastAPI(
    title="Phase 1: Layered Architecture (Controller -> Service -> Repo -> DB)",
    description="Vanilla FastAPI application with zero OpenTelemetry code inside.",
    lifespan=lifespan,
)


# ------------------------------------------------------------------------------
# Controllers (Routes)
# ------------------------------------------------------------------------------
@app.get("/")
def home():
    logger.info("Healthcheck endpoint called.")
    return {
        "status": "healthy",
        "message": "Welcome to Layered Architecture API (Controller -> Service -> Repository -> PostgreSQL)",
        "endpoints": {
            "get_user": "GET /users/{user_id}",
            "list_users": "GET /users",
            "create_user": "POST /users",
            "swagger": "GET /docs",
        },
    }


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    """
    Controller: Receives request for a user by ID.
    Calls UserService.get_user() -> UserRepository.get_by_id() -> PostgreSQL.
    """
    logger.info("Controller: Handling GET /users/%s", user_id)
    try:
        user = service.get_user(user_id)
        return user
    except ValueError as exc:
        logger.warning("Controller: User %s not found: %s", user_id, str(exc))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@app.get("/users", response_model=List[UserResponse])
def list_users(service: UserService = Depends(get_user_service)):
    """
    Controller: Receives request to list all users.
    Calls UserService.get_all_users() -> UserRepository.list_all() -> PostgreSQL.
    """
    logger.info("Controller: Handling GET /users")
    return service.get_all_users()


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreateRequest, service: UserService = Depends(get_user_service)):
    """
    Controller: Receives request to create a new user.
    Calls UserService.create_user() -> UserRepository.create() -> PostgreSQL.
    """
    logger.info("Controller: Handling POST /users for email '%s'", payload.email)
    try:
        user = service.create_user(name=payload.name, email=payload.email, role=payload.role)
        return user
    except ValueError as exc:
        logger.warning("Controller: User creation failed: %s", str(exc))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
