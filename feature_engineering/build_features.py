from feature_engineering.budget_features import normalize_currency, create_target, detect_outliers
from feature_engineering.category_features import normalize_categories, group_rare_subcategories
from feature_engineering.skills_features import create_skills_count, transform_skills_column, filter_frequent_skills, encode_skills
from database.connection import engine
from sqlalchemy import text
import pandas as pd

query = text("SELECT * FROM projects_raw")
df = pd.read_sql_query(query, engine)

# Budget features
df = normalize_currency(df)
df = create_target(df)
df = detect_outliers(df)

# Category features
df = normalize_categories(df)
df = group_rare_subcategories(df)

# Skills features
df = create_skills_count(df)
df = transform_skills_column(df)
df = filter_frequent_skills(df)
df = encode_skills(df)

print(df.columns)