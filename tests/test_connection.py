from database.connection import engine
from sqlalchemy import text

with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    for row in result:
        print(row)