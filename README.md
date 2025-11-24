# Labo BI – Olist (Marketplace brésilien)

Ce dépôt contient mon travail pour le **labo de Business Intelligence Olist** réalisé dans le cadre de la formation *Développeur orienté IA* (Technofutur TIC).

L’objectif est de partir d’un **staging relationnel** (données publiques du e-commerce brésilien Olist) pour construire :
- un **modèle dimensionnel** (schéma en étoile),
- un **datawarehouse**,
- un **ensemble de rapports BI** (ex. Power BI),
permettant de répondre à différentes questions business.

Les données Olist proviennent du dataset public :
- Kaggle – *Brazilian E-Commerce Public Dataset by Olist*.

---

## Objectifs du projet

- Comprendre la structure des données Olist (staging).
- Concevoir un **modèle dimensionnel** centré sur les **ventes**.
- Mettre en place un **ETL** pour alimenter les dimensions et la table de faits.
- Construire un **datawarehouse** exploitable.
- Créer des **dashboards / rapports** pour répondre à des questions business :
  - Montants et quantités par catégorie de produits  
  - Meilleurs clients, meilleurs vendeurs  
  - Produits les plus vendus  
  - Évolution des ventes dans le temps  
  - Types de paiements les plus utilisés  
  - Livraisons à temps / en retard  
  - Produits / vendeurs les mieux notés  
  - etc.

---

## Organisation du dépôt

```text
labo-bi-olist/
│
├── 01_comprehension_donnees/
│   ├── lecture_document_olist.md
│   ├── analyse_staging.md
│   └── diagrammes/
│       └── staging_schema.png
│
├── 02_modele_dimensionnel/
│   ├── schema_etoile.drawio
│   ├── schema_etoile.png
│   ├── description_dimensions.md
│   └── description_faits.md
│
├── 03_etl/
│   ├── mapping_sources_cibles.md
│   ├── scripts_sql/
│   │   ├── create_dimensions.sql
│   │   ├── create_fact_ventes.sql
│   │   ├── load_dimensions.sql
│   │   └── load_fact_ventes.sql
│   ├── ssis_screenshots/
│   └── notes_etl.md
│
├── 04_datawarehouse/
│   ├── creation_tables_dw.sql
│   ├── insertion_dimensions.sql
│   ├── insertion_faits.sql
│   └── diagramme_modele_final.png
│
├── 05_reporting/
│   ├── powerbi/
│   │   └── rapports.pbix
│   ├── visuals_screenshots/
│   └── analyses.md
│
├── journal_de_bord.md
│
└── README.md
```

---

## Author
**Franck Ngaha**  
Developer • Data Science & AI Enthusiast  
[franck.o.ngaha@gmail.com](mailto:franck.o.ngaha@gmail.com)  
[GitHub Profile](https://github.com/fngaha)