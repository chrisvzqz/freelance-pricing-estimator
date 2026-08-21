import time
from deep_translator import GoogleTranslator
import re

def clean_text(df):
    df = df.copy()

    for col in ['title', 'description']:
        df[col] = (
            df[col]
            .str.replace(r'\r\n|\r|\n', ' ', regex=True)
            .str.replace(r'[*_#]+', ' ', regex=True)
            .str.replace(r'\s+', ' ', regex=True)
            .str.strip()
        )

    return df

def safe_translate(text, translator, max_retries=3, delay=0.5):
    for intento in range(max_retries):
        try:
            resultado = translator.translate(text)
            time.sleep(delay)
            return resultado
        except Exception:
            time.sleep(delay * 2)
    return text


def translate_column(serie, translator):
    return [safe_translate(texto, translator) for texto in serie]


def translate_text(df):
    df = df.copy()
    translator = GoogleTranslator(source='es', target='en')

    mask = df['platform'] == 'Workana'

    df.loc[mask, 'title'] = translate_column(df.loc[mask, 'title'], translator)
    df.loc[mask, 'description'] = translate_column(df.loc[mask, 'description'], translator)

    return df