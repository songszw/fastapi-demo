from app.db.base_class import Base
from app.db.session import engine


def init_db():
    import app.models
    Base.metadata.create_all(bind=engine)
