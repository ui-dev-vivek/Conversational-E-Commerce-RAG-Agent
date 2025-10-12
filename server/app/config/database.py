from pathlib import Path
from .settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Build a DB URL if MySQL settings are present, otherwise fallback to sqlite
if settings.db_user and settings.db_name:
    # prefer pymysql driver (ensure pymysql is installed)
    DB_DRIVER = "pymysql"
    db_port = settings.db_port or 3306
    database_url = f"mysql+{DB_DRIVER}://{settings.db_user}:{settings.db_password}@{settings.db_host}:{db_port}/{settings.db_name}"
else:
    # fallback to a local sqlite database for development
    db_file = Path(__file__).parent.parent / "local_dev.db"
    database_url = f"sqlite:///{db_file}"


# Create engine
if database_url.startswith("sqlite"):
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
else:
    engine = create_engine(database_url, echo=settings.debug)


# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()