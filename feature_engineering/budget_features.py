import pandas as pd

EXCHANGE_RATES = {
    "USD": 1.0,
    "EUR": 1.08,
    "GBP": 1.27,
    "INR": 0.012,
}

def normalize_currency(df):
    df = df.copy()

    rate = df['currency'].map(EXCHANGE_RATES)

    df['budget_min'] = df['budget_min'] * rate
    df['budget_max'] = df['budget_max'] * rate
    df['currency'] = 'USD'

    return df

def create_target(df):
    df = df.copy()

    df['target_price'] = (df['budget_min'] + df['budget_max']) / 2

    return df

def _detect_outliers_single_group(df):
    df = df.copy()
    
    q1 = df['target_price'].quantile(0.25)
    q3 = df['target_price'].quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 3 * iqr
    upper_bound = q3 + 3 * iqr

    out_of_range = (df['target_price'] < lower_bound) | (df['target_price'] > upper_bound)

    counts = df['target_price'].value_counts()
    frecuency = df['target_price'].map(counts)
    rare = frecuency <= 2

    df['is_extreme_outlier'] = out_of_range & rare

    return df
    

def detect_outliers(df):
    df_fixed = df.loc[df['budget_type'] == 'fixed_price']
    df_hourly = df.loc[df['budget_type'] == 'hourly']

    df_fixed = _detect_outliers_single_group(df_fixed)
    df_hourly = _detect_outliers_single_group(df_hourly)

    return pd.concat([df_fixed, df_hourly])