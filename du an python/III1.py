import sqlite3
import pandas as pd
import numpy as np
import argparse
import os

#Dinh nghia
DB = "football_data.db"
TABLE = "fbref_player_stats"
OUTPUT = "output"

NON_NUMERIC_COLS = ["Player", "Nation", "Pos", "Squad"]


#Lay du lieu
def load_data(db_path, table):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    conn.close()
    return df


#Xu ly du lieu
def clean_data(df):
    df = df.replace("N/a", np.nan)

    drop_cols = ["Rk", "Matches", "Born"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    for col in df.columns:
        if col not in NON_NUMERIC_COLS:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


#thong ke
def compute_stats(df):
    grouped = df.groupby("Squad")

    trungbinh = grouped.mean(numeric_only=True)
    trungvi = grouped.median(numeric_only=True)
    dolechchuan = grouped.std(numeric_only=True)

    return trungbinh, trungvi, dolechchuan


#doi co chi so cao
def compute_top_teams(mean_df):
    result = []

    for col in mean_df.columns:
        if mean_df[col].notna().any():
            top_team = mean_df[col].idxmax()
            top_value = mean_df[col].max()
            result.append([col, top_team, top_value])

    return pd.DataFrame(result, columns=["Stat", "Topteam", "Value"])


#luu file
def save_outputs(trungbinh, trungvi, dolechchuan, top_df):
    os.makedirs(OUTPUT, exist_ok=True)

    def format_df(df):
        df = df.copy()
        for col in df.select_dtypes(include=["float", "int"]).columns:
            df[col] = df[col].round(3)
        return df.reset_index()

    format_df(trungbinh).to_csv(f"{OUTPUT}/trungbinh.csv", index=False, encoding="utf-8-sig")
    format_df(trungvi).to_csv(f"{OUTPUT}/trungvi.csv", index=False, encoding="utf-8-sig")
    format_df(dolechchuan).to_csv(f"{OUTPUT}/dolechchuan.csv", index=False, encoding="utf-8-sig")
    top_df.to_csv(f"{OUTPUT}/topchiso.csv", index=False, encoding="utf-8-sig")


#main
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=DB)
    parser.add_argument("--table", default=TABLE)
    args = parser.parse_args()

    df = load_data(args.db, args.table)
    df = clean_data(df)
    trungbinh, trungvi, dolechchuan = compute_stats(df)
    top_df = compute_top_teams(trungbinh)
    save_outputs(trungbinh, trungvi, dolechchuan, top_df)

    print("\n Xem kết quả trong thư mục: output/")


if __name__ == "__main__":
    main()
