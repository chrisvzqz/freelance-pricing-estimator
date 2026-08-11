CATEGORY_MAPPING = {
    "Websites, It & Software" : "Websites, It & Software",
    "Programación Y Tecnología" : "Websites, It & Software",
    "Artificial Intelligence" : "Artificial Intelligence"
}

def normalize_categories(df):
    df = df.copy()

    df['category'] = df['category'].str.strip().str.title()
    df['subcategory'] = df['subcategory'].str.strip().str.title()

    df['category'] = df['category'].map(CATEGORY_MAPPING)

    return df

def group_rare_subcategories(df, min_freq=5):
    df = df.copy()

    counts = df['subcategory'].value_counts()
    rare_categories = counts[counts < min_freq].index

    df['subcategory'] = df['subcategory'].replace(rare_categories, 'Other')

    return df