from sqlalchemy import (
    Column, BigInteger, Text, Numeric, String, TIMESTAMP
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ProjectRaw(Base):
    __tablename__ = "projects_raw"

    id = Column(BigInteger, primary_key=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    budget_min = Column(Numeric(12, 2), nullable=True)
    budget_max = Column(Numeric(12, 2), nullable=True)
    budget_type = Column(String(20), nullable=False)
    skills = Column(JSONB, nullable=False)
    category = Column(String, nullable=True)
    subcategory = Column(String, nullable=True)
    project_url = Column(Text, unique=True, nullable=False)
    platform = Column(String(20), nullable=False)
    currency = Column(String(3), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())