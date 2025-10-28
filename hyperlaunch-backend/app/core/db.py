from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# SQLite needs 'check_same_thread' for FastAPI multi-threaded mode
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG, connect_args=connect_args)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
