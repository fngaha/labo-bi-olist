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

## Dossier 01_comprehension_donnees/

Contient tout ce qui concerne la compréhension du problème et des données :

- Résumé du document de labo et du contexte Olist
- Analyse des tables de staging
- Schémas/diagrammes du modèle relationnel (staging)

## Dossier 02_modele_dimensionnel/

Contient la conception du modèle dimensionnel :

- Schéma en étoile (fichier .drawio + export .png)
- Description des dimensions (attributs, clés, grain)
- Description des tables de faits (grain, mesures, FK)

## Dossier 03_etl/

Contient tout ce qui concerne l’alimentation du DW :

- Mapping source → cible (staging → dimensions/faits)
- Scripts SQL utiles
- Captures d’écran des flux SSIS (ou autre ETL)
- Notes techniques sur les choix ETL

## Dossier 04_datawarehouse/

Contient :

- Scripts SQL de création des tables du DW
- Scripts de chargement (dimensions, faits)
- Diagramme final du modèle logique/physique

## Dossier 05_reporting/

Contient :

- Fichiers de rapport (ex. Power BI : .pbix)
- Captures d’écran principales des dashboards
- Notes d’analyse (quels indicateurs, quelles conclusions)

---

Technologies et outils

- SGBD : SQL Server
- ETL : SSIS (ou autre outil ETL choisi)
- Reporting : Power BI (ou Qlik / Tableau selon consignes)
- Modélisation : diagrams.net / draw.io pour les schémas

---

Comment naviguer dans ce dépôt

1. Commencer par journal_de_bord.md pour voir la chronologie du travail.
2. Lire les fichiers de 01_comprehension_donnees/ pour comprendre la base de données source.
3. Consulter 02_modele_dimensionnel/ pour le schéma en étoile et les descriptions.
4. Voir 03_etl/ et 04_datawarehouse/ pour l’implémentation technique.
5. Terminer par 05_reporting/ pour les dashboards et l’interprétation des résultats.

---

## Statut du projet

- [x] Compréhension des données terminée
- [ ] Modèle dimensionnel validé
- [ ] ETL implémenté
- [ ] Datawarehouse alimenté
- [ ] Rapports BI créés
- [ ] Documentation finalisée

---

## Author
**Franck Ngaha**  
Developer • Data Science & AI Enthusiast  
[franck.o.ngaha@gmail.com](mailto:franck.o.ngaha@gmail.com)  
[GitHub Profile](https://github.com/fngaha)