from database.models import Base
from database.connection import engine

Base.metadata.create_all(engine)