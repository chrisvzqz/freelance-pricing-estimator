import pandas as pd

df = pd.read_json('./data/raw/projects_workana.json')

def normalize_workana(df):
    df = df.drop_duplicates(subset=['project_url'], keep='first')
    df = df.drop('scope_project', axis=1)
    df['currency'] = 'USD'

    return df