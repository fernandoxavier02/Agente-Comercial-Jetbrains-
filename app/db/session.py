from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Para desenvolvimento simples, vamos usar SQLite se a URL for a padrão ou não estiver configurada
database_url = settings.DATABASE_URL
if database_url.startswith("postgresql") or not database_url:
    # Para simplificar o passo a passo, usaremos SQLite síncrono inicialmente
    database_url = "sqlite:///./sql_app.db"

engine = create_engine(
    database_url, connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
