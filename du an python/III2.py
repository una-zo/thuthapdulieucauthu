import sqlite3
import pandas as pd
import numpy as np
import argparse

DB_FILE = "football_data.db"
OUTPUT_FILE = "Dinhgiacaccauthu.csv"

NON_NUMERIC_COLS = ["Player", "Nation", "Pos", "club"]

#Lay du lieu tu bang
def load_data(db_file):
    conn = sqlite3.connect(db_file)

    query = """
    SELECT *
    FROM fbref_player_stats
    WHERE Min > 90
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


# Xu ly cac du lieu N/a thanh Nan = 0
def clean_data(df):
    df.replace("N/a", np.nan, inplace=True)

    numeric_cols = df.columns.difference(NON_NUMERIC_COLS)
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    df.fillna(0, inplace=True)
    return df


# neu ko co du lieu cho bang 0
def get_col(df, col):
    if col in df.columns:
        return df[col]
    return pd.Series(0, index=df.index)


# dua cac du lieu ve cung 1 don vi
def normalize(series):
    min_val = series.min()
    max_val = series.max()

    if max_val != min_val:
        return (series - min_val) / (max_val - min_val)
    else:
        return pd.Series(0, index=series.index)


# tinh gia cac cau thu
def compute_value(df):

    attack = normalize(get_col(df, 'Gls/90'))
    creative = normalize(get_col(df, 'Ast/90'))
    minutes = normalize(get_col(df, 'Min'))

    # performance score
    performance = (
        0.7 * attack +
        0.3 * creative
    )

    # age factor
    if 'Age' in df.columns:
        age_factor = df['Age'].apply(
            lambda x: 1.2 if x < 23 else (1.0 if x <= 28 else 0.8)
        )
    else:
        age_factor = 1.0

    # cong thuc tinh
    estimated_value = (
        performance *
        age_factor *
        (1 + minutes) * 100
    )

    df['estimated_value'] = estimated_value

    return df

def run_pipeline(db_file, output_file):
    df = load_data(db_file)
    df = clean_data(df)
    df = compute_value(df)

    df_output = df[['Player', 'estimated_value']]
    df_output = df_output.sort_values('estimated_value', ascending=False)

    df_output.to_csv(output_file, index=False)

    print("Done!")


# MAIN
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=DB_FILE)
    parser.add_argument("--out", default=OUTPUT_FILE)

    args = parser.parse_args()

    run_pipeline(args.db, args.out)
