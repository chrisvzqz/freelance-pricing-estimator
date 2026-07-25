import pandas as pd
from database.connection import SessionLocal
from database.models import ProjectRaw

df = pd.read_json("data/raw/projects_merged.jsonl", lines=True)

session = SessionLocal()

for _, row in df.iterrows():
    project = ProjectRaw(
        title=row['title'],
        description=row['description'], 
        budget_min=row['budget_min'] if not pd.isna(row['budget_min']) else None, 
        budget_max=row['budget_max'] if not pd.isna(row['budget_max']) else None, 
        budget_type=row['budget_type'], 
        skills=row['skills'],
        category=row['category'],
        subcategory=row['subcategory'],
        project_url=row['project_url'],
        platform=row['platform'],
        currency=row['currency']
        )
    session.add(project)

session.commit()
session.close()