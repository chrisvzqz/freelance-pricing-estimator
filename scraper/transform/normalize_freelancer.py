import pandas as pd

df = pd.read_json('./data/raw/projects_freelancer.jsonl', lines=True)

def normalize_freelancer(df):
    df['budget_min'] = df['budget_min'].astype(float)

    return df