import streamlit as st
import pandas as pd


import gdown
import pandas as pd

from dotenv import load_dotenv
import os

# load_dotenv()  # Load variables from .env file
# google_sheet_key = os.getenv("GOOGLE_SHEET_KEY")
google_sheet_key = st.secrets["GOOGLE_SHEET_KEY"]
if not google_sheet_key:
    raise ValueError("GOOGLE_SHEET_KEY environment variable is not set!")

url = f"https://docs.google.com/spreadsheets/d/{google_sheet_key}/export?format=xlsx"
output = "sheet.xlsx"
gdown.download(url, output, quiet=False)
df = pd.read_excel(output)

df = df.query("Type!='Amical'").copy()

df['points'] = df["Résultat"].apply(lambda x: 4 if x == "V" else 2 if x == "N" else 1)

df_player = df.groupby("Joueur").agg({"Buteur": "sum", "Passeur": "sum", "Match": "count", "points": "sum"}).sort_values("points", ascending=False)
for metric in ["Buteur", "Passeur", "points"]:
    df_player[f'{metric}_per_match'] = df_player[metric] / df_player["Match"]

st.write(df_player)