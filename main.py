import pandas as pd
from pathlib import Path

# Chargement optimisé (Parquet > CSV > Excel)
parquet_file = Path("data/online_retail.parquet")
csv_file = Path("data/online_retail.csv")
excel_file = Path("Online Retail.xlsx")

if parquet_file.exists():
    print(f"Chargement optimisé depuis {parquet_file}...")
    df = pd.read_parquet(parquet_file)
elif csv_file.exists():
    print(f"Chargement depuis {csv_file}...")
    df = pd.read_csv(csv_file)
else:
    print(f"Lecture du fichier Excel {excel_file}...")
    df = pd.read_excel(excel_file)

# Afficher les 5 premières lignes
print("\n--- LES 5 PREMIÈRES LIGNES ---")
print(df.head())

# Afficher le nombre de lignes et colonnes
print("\n--- DIMENSIONS DU FICHIER ---")
print(df.shape)

# Afficher les noms des colonnes
print("\n--- NOMS DES COLONNES ---")
print(df.columns)

# Afficher les informations générales
print("\n--- INFORMATIONS DU FICHIER ---")
df.info()

# Vérifier les valeurs manquantes
print("\n--- VALEURS MANQUANTES ---")
print(df.isnull().sum())
