import pandas as pd
from scraper.transform.normalize_workana import normalize_workana
from scraper.transform.normalize_freelancer import normalize_freelancer

df_workana = pd.read_json('./data/raw/projects_workana.json')
df_freelancer = pd.read_json('./data/raw/projects_freelancer.jsonl', lines=True)

def merge_datasets(df_workana, df_freelancer):
    df_workana_normalized = normalize_workana(df_workana)
    df_freelancer_normalized = normalize_freelancer(df_freelancer)

    merge_df = pd.concat([df_workana_normalized, df_freelancer_normalized], ignore_index=True)
    
    with open("data/raw/projects_merged.jsonl", "w", encoding="utf-8") as f:
        merge_df.to_json(f, orient='records', lines=True, force_ascii=False)
    
    return merge_df

merge_datasets(df_workana, df_freelancer)