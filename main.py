from fastapi import FastAPI, Depends, status, HTTPException
from contextlib import asynccontextmanager
from app.models import Base, User
from sqlalchemy.orm import Session
from database import get_engine, get_session
from app.services import addUser
from app.responses import (
    ResponseCreateUser,
    UserCreateBody,
    UserCreateResponse,
)
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=get_engine())
    yield
app = FastAPI(lifespan=lifespan)



@app.post(
    "/register/user",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseCreateUser,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "The user already exists"
        }
    },
)
def register(
    user: UserCreateBody,
    session: Session = Depends(get_session),
) -> dict[str, UserCreateResponse]:
    user = addUser(
        session=session, **user.model_dump()
    )
    if not user:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "username or email already exists",
        )
    user_response = UserCreateResponse(
        username=user.username, email=user.email
    )
    return {
        "message": "user created",
        "user": user_response,
    }