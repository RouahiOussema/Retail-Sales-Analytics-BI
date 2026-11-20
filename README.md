# 🛒 Retail Sales Analytics & Business Intelligence (BI)

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/)
[![Package Manager](https://img.shields.io/badge/package%20manager-uv-blueviolet.svg)](https://docs.astral.sh/uv/)
[![Data Processing](https://img.shields.io/badge/data-pandas%20%7C%20pyarrow-orange.svg)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Pipeline complet d'ingestion, d'exploration (EDA), de nettoyage et d'analyse décisionnelle (BI) à partir d'un jeu de données e-commerce international réel (*Online Retail Dataset*).

Ce projet couvre l'ensemble du cycle de vie de la donnée : depuis l'ingestion brute et le benchmarking des formats de fichiers jusqu'au calcul d'indicateurs clés de performance (KPI) pour le pilotage stratégique de l'entreprise.

---

## 📋 Table des Matières

- [Aperçu du Projet](#-aperçu-du-projet)
- [Architecture du Dépôt](#-architecture-du-dépôt)
- [Description du Dataset](#-description-du-dataset)
- [Pipeline de Données & Méthodologie](#-pipeline-de-données--méthodologie)
- [Indicateurs Clés & Insights BI](#-indicateurs-clés--insights-bi)
- [Sécurité & Données (.gitignore)](#-sécurité--bonnes-pratiques-gitignore)
- [Technologies Utilisées](#-technologies-utilisées)
- [Installation & Démarrage Rapide](#-installation--démarrage-rapide)
- [Auteur](#-auteur)

---

## 🎯 Aperçu du Projet

L'objectif de ce projet est d'extraire de la valeur décisionnelle à partir de plus de **540 000 transactions e-commerce** réparties dans 38 pays. 

Les principaux défis relevés sont :
1. **Performance de lecture** : Optimisation du temps de chargement et de la mémoire grâce à l'adoption du format Parquet vs CSV et Excel.
2. **Qualité de la donnée** : Détection des anomalies, gestion des valeurs manquantes, identification des annulations et filtrage des codes techniques.
3. **Analytique & Visualisation** : Calcul des métriques de vente, segmentation géographique, analyse de saisonnalité et identification du catalogue produit le plus rentable.

---

## 📂 Architecture du Dépôt

```plaintext
Retail-Sales-Analytics-BI/
│
├── data/
│   ├── raw/                  # Données brutes (Online Retail.xlsx / .csv)
│   ├── clean/                # Données nettoyées (ventes.csv, annulations.csv)
│   └── marts/                # Données agrégées et marts prêts pour le reporting BI
│
├── NoteBooks/
│   └── 01_exploration.ipynb   # Notebook pas-à-pas (EDA, Nettoyage, KPIs & Graphiques)
│
├── src/
│   └── retail_bi/            # Package applicatif Python
│       └── __init__.py
│
├── .gitignore                # Exclusion des jeux de données, secrets et environnements
├── .python-version           # Version Python requise (>= 3.13)
├── main.py                   # Script d'ingestion multi-formats et d'audit rapide
├── pyproject.toml            # Configuration du projet et dépendances
├── uv.lock                   # Verrouillage déterministe des dépendances (uv)
└── README.md                 # Documentation du projet
```

---

## 📊 Description du Dataset

Le projet exploite le célèbre jeu de données **Online Retail** (transactions enregistrées entre le 01/12/2010 et le 09/12/2011) :

| Colonne | Type | Description |
| :--- | :--- | :--- |
| `InvoiceNo` | Chaîne (Nominal) | Identifiant unique de facture. Préfixé d'un `'C'` en cas d'annulation. |
| `StockCode` | Chaîne (Nominal) | Code produit unique attribué à chaque article. |
| `Description` | Chaîne (Texte) | Désignation commerciale du produit. |
| `Quantity` | Entier | Quantité commandée par transaction. Négative lors d'une annulation. |
| `InvoiceDate` | Datetime | Horodatage précis de la commande. |
| `UnitPrice` | Décimal | Prix unitaire du produit en livres sterling (£). |
| `CustomerID` | Décimal / ID | Identifiant client unique (nullable pour les achats invités). |
| `Country` | Chaîne | Pays de résidence du client (38+ pays). |

---

## ⚙️ Pipeline de Données & Méthodologie

Le workflow analytique implémenté dans `NoteBooks/01_exploration.ipynb` et automatisé dans `main.py` comprend 4 phases :

### 1. Ingestion & Benchmark des formats
Le projet implémente un chargement hiérarchique optimisé :
$$\text{Parquet} \longrightarrow \text{CSV} \longrightarrow \text{Excel}$$
* Le format **Parquet** réduit l'espace disque de plus de 90 % par rapport au CSV et accélère les temps de lecture d'un facteur 5x à 10x.

### 2. Diagnostic de Qualité (Data Profiling)
- **Valeurs manquantes** : Identification d'environ ~25 % de `CustomerID` manquants (transactions anonymes) et quelques descriptions absentes.
- **Doublons** : Détection et élimination des enregistrements dupliqués stricts.
- **Anomalies de prix & quantités** : Détection de prix nuls (`UnitPrice = 0`) et de quantités négatives.

### 3. Nettoyage & Transformation
- **Gestion des annulations** : Isolation des commandes annulées (`InvoiceNo` commençant par `C` ou `Quantity < 0`) dans un fichier dédié : `data/clean/annulations.csv`.
- **Filtrage des codes hors-commerce** : Retrait des lignes techniques (frais de port `POST`, ajustements bancaires `BANK CHARGES`, remises manuelles `D`, `M`).
- **Création de la métrique de chiffre d'affaires** :
  $$\text{Montant} = \text{Quantity} \times \text{UnitPrice}$$
- **Sauvegarde du dataset propre** dans `data/clean/ventes.csv`.

### 4. Indicateurs Clés de Performance (KPIs)
- **Volume d'activité** : Chiffre d'affaires total, total de commandes nettes, volume d'articles vendus.
- **Comportement client** : Panier moyen (*Average Order Value*), nombre de clients uniques, fréquence de commande.
- **Segmentation géographique** : Répartition du CA par pays (Royaume-Uni dominant à plus de 80 %, suivi de l'Allemagne, la France, les Pays-Bas, etc.).
- **Analyse temporelle & saisonnalité** : Suivi de l'évolution mensuelle montrant une forte accélération au quatrième trimestre (Q4 / pic de fin d'année).

---

## 🔒 Sécurité & Bonnes Pratiques (.gitignore)

Un fichier `.gitignore` robuste et exhaustif a été mis en place pour garantir la sécurité et la légèreté du dépôt :

- 🚫 **Fichiers de données volumineux exclus** (`*.xlsx`, `*.csv`, `*.parquet`, `*.db`) :
  - Respect des limites GitHub (seuil d'avertissement à 50 Mo, blocage à 100 Mo).
  - Prévention de la fuite de données confidentielles ou nominatives (RGPD / GDPR).
  - Préservation de l'architecture des dossiers grâce aux balises `.gitkeep` (`data/raw/`, `data/clean/`, `data/marts/`).
- 🚫 **Environnements virtuels exclus** (`.venv/`, `venv/`) pour éviter d'embarquer des dépendances locales lourdes.
- 🚫 **Secrets et clés d'API protégés** (`.env`, `*.key`, `*.pem`, `credentials.json`).
- 🚫 **Caches et résidus de développement exclus** (`__pycache__/`, `.ipynb_checkpoints/`, `.pytest_cache/`).

---

## 🛠️ Technologies Utilisées

- **Langage** : Python 3.13+
- **Gestionnaire d'environnement & paquets** : [uv](https://github.com/astral-sh/uv)
- **Traitement & Analyse de données** : [Pandas](https://pandas.pydata.org/), [PyArrow](https://arrow.apache.org/docs/python/)
- **Visualisation de données** : [Matplotlib](https://matplotlib.org/)
- **Fichiers tabulaires** : [OpenPyXL](https://openpyxl.readthedocs.io/)
- **Environnement interactif** : [Jupyter / IPyKernel](https://jupyter.org/)

---

## 🚀 Installation & Démarrage Rapide

### 1. Cloner le dépôt
```bash
git clone https://github.com/RouahiOussema/Retail-Sales-Analytics-BI.git
cd Retail-Sales-Analytics-BI
```

### 2. Configuration de l'environnement virtuel

#### Avec `uv` (Recommandé - Ultra rapide) :
```bash
# Synchroniser l'environnement virtuel à partir du fichier de verrouillage
uv sync
```

#### Avec Python standard (`venv`) :
```bash
python -m venv .venv

# Sous Windows (PowerShell) :
.venv\Scripts\Activate.ps1

# Sous Linux/macOS :
source .venv/bin/activate

# Installer les dépendances
pip install -e .
```

### 3. Placer le dataset
Téléchargez le fichier `Online Retail.xlsx` (ex: depuis Kaggle ou UCI Machine Learning Repository) et déposez-le dans :
```plaintext
data/raw/Online Retail.xlsx
```

### 4. Exécuter le projet

#### Test de chargement rapide :
```bash
python main.py
```

#### Lancer le notebook analytique :
```bash
jupyter lab NoteBooks/01_exploration.ipynb
```

---

## 👤 Auteur

**Oussema Rouahi**
- GitHub : [@RouahiOussema](https://github.com/RouahiOussema)
- Email : [rouahi.oussama.tn@gmail.com](mailto:rouahi.oussama.tn@gmail.com)
