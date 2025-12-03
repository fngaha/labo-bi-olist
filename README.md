# 🇫🇷 Labo BI Olist — Datawarehouse, ETL Python & Dashboard Power BI

Ce projet a été réalisé dans le cadre du module **"Labo modélisation de données"** de la formation **Développeur orienté IA** (Technofutur TIC).
Il constitue un pipeline BI complet, similaire à ce qui est fait dans une vraie équipe Data Engineering.

- Modèle dimensionnel (schéma en étoile)
- ETL Python structuré (extract / transform / load)
- Datawarehouse SQL Server
- Dashboard Power BI professionnel (multi-pages)
- Qualité de code : Black, Ruff, pre-commit
- Architecture prête pour Airflow/Pipelines

---

## 1. Objectifs du projet

- Analyser le dataset Olist (e-commerce brésilien).

- Concevoir un schéma en étoile autour des ventes.

- Construire un staging et un datawarehouse sur SQL Server.

- Développer un ETL Python structuré en extract / transform / load.

- Créer un dashboard Power BI interactif basé sur le DW.

- Appliquer les bonnes pratiques professionnelles de data engineering.

---

## 2. Architecture du projet

```text
labo-bi-olist/
  01_comprehension_donnees/     # Analyse des datasets Olist
  02_modele_dimensionnel/       # Star schema, dimensions et fact
  03_etl/
    etl/
      db_connection.py          # Connexion SQLAlchemy/pyodbc
      extract_staging.py        # Extract : staging SQL Server
      extract_dw.py             # Extract : lookup dimensions DW
      transform_dimensions.py   # Transform : dimensions
      transform_facts.py        # Transform : F_Ventes_Items
      load_dimensions.py        # Load : tables dimensionnelles
      load_facts.py             # Load : fact table
      main.py                   # Orchestration ETL (run_etl_all)
    test_connexion.py
  04_datawarehouse/
    Create_D_*.sql              # Scripts SQL des dimensions
    Create_F_Ventes_Items.sql   # Script SQL table de faits
  05_powerbi/
    Olist_DW_Model.pbit         # Template Power BI
    theme_OlistPro.json         # Thème pro personnalisé
    dashboard_*png|pdf          # Captures du dashboard
    README_powerbi.md           # Documentation du modèle Power BI
  journal_de_bord.md            # Notes du labo
  README.md                     # Ce fichier

```

---

## 3. Modèle dimensionnel (Star Schema)

### Dimensions :

- D_Date : calendrier complet (Date_SK, année, mois, etc.)

- D_Product : produits et catégories

- D_Category : catégories produit

- D_Customer : clients

- D_Seller : vendeurs

- D_PaymentType : types de paiements

- D_OrderStatus : statuts commandes


## Table de faits :

- F_Ventes_Items
  - Grain : 1 ligne = (order_id, order_item_id)
  - Mesures : price, freight_value, quantity, total_item_value, total_weight_g
  - Liens SK → toutes les dimensions

  Les relations ont été automatiquement détectées dans Power BI car les FK SQL étaient correctement définies dans le DW.

---

## 4. ETL Python — Pattern Extract / Transform / Load

Le projet suit une architecture claire :

### Extractors

Lire les données depuis :

- le staging SQL Server

- les dimensions du DW pour les SK lookups

Code : `extract_staging.py` & `extract_dw.py`

### Transformers

Logique métier :

- jointures orders + order_items + customers

- enrichissement produits & vendeurs

- dérivation de la date

- assignation des SK

- calcul des mesures

Code : `transform_dimensions.py` & `transform_facts.py`

### Loaders

Chargement propre dans SQL Server :

- DELETE + INSERT

- respect des FK

- qualité des types SQL

Code : `load_dimensions.py` & `load_facts.py`

### Orchestration

`main.py` fournit :

````
run_etl_dimensions()
run_etl_fact_ventes_items()
run_etl_all()  # pipeline complet
````

L’ETL utilise maintenant :

- logging professionnel

- contrôles qualité automatiques (SK NULL, nombre de lignes…)

- structure prête pour Airflow

---

## 5. Dashboard Power BI

Le dashboard inclus :

### 1. Page Vue d’ensemble

- Total Ventes, Nb Commandes, Nb Clients, Nb Produits

- Ventes par année

- Ventes par statut

### 2. Page Produits & Catégories

- Top catégories

- Top produits

- Slicer catégorie

### 3. Page Clients & Géographie

- Ventes par état

- Top villes

- Slicers : année, type de paiement

### Thème personnalisé (OlistPro)

Disponible dans :

```
05_powerbi/theme_OlistPro.json
```

### Captures d’écran

(disponibles dans `05_powerbi/*.png|pdf`)

---

## 6. Qualité du code (Black, Ruff, pre-commit)

Le projet utilise :

- Black : formatage automatique

- Ruff : lint + tri des imports (isort-like)

- pre-commit : exécution automatique avant chaque commit

Configuration dans :

- `pyproject.toml`

- `.pre-commit-config.yaml`

---

## 7. Comment exécuter l’ETL

1. Installer les dépendances

```
pip install -r requirements.txt
```

2. Vérifier la connexion SQL Server

```python
python etl/test_connexion.py
```

3. Lancer l’ETL complet

```python
python -m 03_etl.etl.main --job all
```

ou :

```python
python -m 03_etl.etl.main
```

---

## 6. Améliorations possibles

- ajout de tests unitaires (pytest)

- migration Airflow (DAG Python)

- ajout d'un Data Lake (bronze → silver → gold)

- enrichissement du modèle BI

- automatisation des contrôles qualité avancés

## 👤 Auteur
Franck Ngaha  
Développeur orienté IA – Data Engineering & BI  
🎓 Formation Technofutur TIC  
🌐 LinkedIn : https://www.linkedin.com/in/franck-ngaha

---

# 🇬🇧 Olist BI Lab — Data Warehouse, Python ETL & Power BI Dashboard

This project was developed for the Data Modelling Lab within the AI-Oriented Developer training.
It implements a fully functional enterprise-grade BI pipeline.

- SQL Server Data Warehouse (star schema)
- Python ETL pipeline (structured ETL pattern)
- Professional Power BI Dashboard
- Black + Ruff + pre-commit code quality
- Architecture ready for Airflow DAGs

## 1. Project Objectives

- Analyze the Brazilian Olist e-commerce dataset

- Design a star schema (dimensions + fact table)

- Build a staging and a data warehouse in SQL Server

- Develop a fully modular Python ETL pipeline

- Create a multi-page Power BI report

- Follow modern data engineering best practices

## 2. Project Architecture

(identical to the FR version — folder tree)

## 3. Star Schema

Dimensions: Date, Product, Category, Customer, Seller, PaymentType, OrderStatus

Fact table: F_Ventes_Items (grain = order_id, order_item_id)

The Power BI model automatically detected relationships thanks to SQL FK constraints.

## 4. ETL Architecture (Extractor / Transformer / Loader)

- Extract from SQL staging

- Transform business logic (joins, SK mapping, measures)

- Load into SQL DW with referential integrity

The ETL is fully orchestrated via main.py and ready to be converted into an Airflow DAG.

## 5. Power BI Dashboard

Three pages:

1. Overview

2. Products & Categories

3. Customers & Geography

Includes a custom theme **(theme_OlistPro.json)** and reusable template **(.pbit)**.

## 6. Code Quality

- Black: auto-format

- Ruff: lint + import sorting

- pre-commit hooks

## 7. Running the ETL

```python
python -m 03_etl.etl.main --job all
```

## 8. Future Enhancements

- Airflow orchestration

- Advanced data quality checks

- Incremental loads

- Lakehouse architecture

## 👤 Author
**Franck Ngaha**  
AI-Oriented Developer – Data Engineering & Business Intelligence  
🎓 Technofutur TIC Training Program  
🌐 LinkedIn: https://www.linkedin.com/in/franck-ngaha