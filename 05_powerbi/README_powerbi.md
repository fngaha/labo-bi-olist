## Dashboard Power BI – Analyse des ventes Olist

Ce dossier contient le **modèle Power BI** utilisé pour analyser les ventes Olist à partir du datawarehouse Olist_DW.

Le rapport a été construit à partir d’un **schéma en étoile**, entièrement alimenté par un **ETL Python**.

## Thème Power BI

Un thème professionnel personnalisé est appliqué :
```
OlistPro.json
```
Couleurs :

- bleu pétrole,

- turquoise,

- jaune doux,

- orange,

- fond crème,

- texte gris anthracite.

## Contenu du dossier
| Fichier                   | Description                         |
| ------------------------- | ----------------------------------- |
| `Olist_DW_Model.pbit`     | Template Power BI du rapport        |
| `theme_OlistPro.json`     | Thème visuel personnalisé           |
| `dashboard_Olist_Report.pdf` | Page "Clients & Géographie"         |
| `dashboard_model.png`     | Schéma du modèle Power BI           |

## Modèle Power BI

Le rapport utilise les tables suivantes du datawarehouse :

- `F_Ventes_Items` (fact table)

- `D_Date`

- `D_Product`

- `D_Customer`

- `D_Seller`

- `D_PaymentType`

- `D_OrderStatus`

Toutes les relations sont basées sur des **clés substituts (SK)**, conformément au modèle en étoile.

## Pages du Rapport
### Vue d’ensemble

KPI principaux :

- Total des ventes

- Nombre de commandes

- Nombre de clients

- Nombre de produits

- Frais de livraison

Graphiques :

- Ventes par année

- Ventes par statut de commande

### Produits & Catégories

Top 10 catégories

Top produits vendus

Slicers : catégorie, année

### Clients & Géographie

- Ventes par état

- Top villes

- Slicers : année, type de paiement, statut

## Mesures DAX principales

- Total Ventes = SUM(FactVentesItems[total_item_value])
- Total Quantité = SUM(FactVentesItems[quantity])
- Total Delivery = SUM(FactVentesItems[freight_value])
- Nb Commandes = DISTINCTCOUNT(FactVentesItems[order_id])
- Nb Produits = DISTINCTCOUNT(FactVentesItems[Product_SK])
- Nb Clients = DISTINCTCOUNT(FactVentesItems[Customer_SK])
- Poids Total (g) = SUM(FactVentesItems[total_weight_g])

## Pré-requis pour ouvrir le .pbit

1. Avoir SQL Server (accès à la VM TFTIC)

2. La base Olist_DW doit être restaurée / générée

3. Le .pbit demandera la connexion :

    - Serveur : GOS-VDI410\TFTIC

    - Base : Olist_DW