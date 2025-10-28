from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.core.db import get_session
from app.utils import send_welcome_email

router = APIRouter()

@router.post("/users", response_model=UserOut)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/users", response_model=list[UserOut])
def get_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()


@router.post("/send_welcome")
async def send_email_endpoint(email: str):
    await send_welcome_email(
        to_email=email,
        username="nabin",
        password="secret123",
        link="https://myapp.com/dashboard"
    )
    return {'status': "email sent"}