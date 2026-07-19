from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

env_vars = {
    "DB_NAME": os.getenv("DB_NAME"),
    "DB_USER": os.getenv("DB_USER"),
    "DB_PASSWORD": os.getenv("DB_PASSWORD"),
    "DB_PORT": os.getenv("DB_PORT"),
    "DB_HOST": os.getenv("DB_HOST")
}

for key, variable in env_vars.items():
    if variable is None:
        raise ValueError(f"Environment variable {key} is not set.")
    
db_name = env_vars["DB_NAME"]
db_user = env_vars["DB_USER"]
db_password = env_vars["DB_PASSWORD"]
db_port = env_vars["DB_PORT"]
db_host = env_vars["DB_HOST"]

DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)