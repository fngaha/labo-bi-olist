# Description des dimensions – Modèle dimensionnel Olist

Ce document décrit l’ensemble des **dimensions retenues** pour la modélisation BI centrée sur les ventes du dataset Olist.  
Chaque dimension est définie selon les principes du Data Warehousing : clé substitut, clés métiers, attributs, source et rôle analytique.

---

# 1. D_Date

### Clé substitut
- `Date_SK` (type INT, format AAAAMMJJ)

### Clé métier
- `date` (date réelle)

### Description
Dimension de temps permettant d’analyser les ventes, livraisons et achats selon différentes granularités (année, trimestre, mois, semaine, jour).

### Attributs principaux
- `FullDate`
- `Year`
- `Quarter`
- `Month`
- `Month_Name`
- `Week_Year`
- `Day`
- `DayOfWeek`
- `Day_Name`
- `IsWeekend`
- etc.

### Source
Script fourni dans le labo : `Create_Populate_DateDimension.sql`.

### Rôle analytique
Analyse temporelle des ventes, livraisons, retards.

---

# 2. D_Product

### Clé substitut
- `Product_SK`

### Clé métier
- `product_id`

### Description
Dimension décrivant les produits vendus sur la marketplace Olist.

### Attributs potentiels
Depuis `products` :
- `product_id`
- `product_category_name`
- `product_name_lenght`
- `product_description_lenght`
- `product_photos_qty`
- `product_weight_g`
- `product_length_cm`
- `product_height_cm`
- `product_width_cm`

Mesures dérivées possibles :
- `product_volume_cm3` (longueur × hauteur × largeur)

### Source
Table `products` (staging).

### Rôle analytique
- identifier les produits les plus vendus  
- analyser les performances par type de produit  
- relier les ventes aux caractéristiques du produit  

---

# 3. D_Category

### Clé substitut
- `Category_SK`

### Clé métier
- `product_category_name` (PT)

### Description
Dimension des catégories de produits, incluant la traduction en anglais.

### Attributs
- `product_category_name` (PT)
- `product_category_name_english` (EN)

### Source
Table `product_category_name_translation`.

### Rôle analytique
- regroupements par catégorie  
- analyses des montants/quantités par catégorie  
- meilleure lisibilité des rapports (noms anglais)

---

# 4. D_Customer

### Clé substitut
- `Customer_SK`

### Clé métier
- `customer_unique_id`

(et non `customer_id`, car celui-ci change à chaque commande)

### Description
Représente le client réel de la marketplace.

### Attributs retenus
Depuis `customers` :
- `customer_unique_id`
- `customer_id`  
- `customer_zip_code_prefix`
- `customer_city`
- `customer_state`

Facultatif, si on ajoute la géolocalisation :
- `latitude`
- `longitude`

### Source
Table `customers`, jointure possible sur `geolocation`.

### Rôle analytique
- identifier les meilleurs clients  
- analyser les zones géographiques les plus actives  
- mesurer la fidélité des clients  

---

# 5. D_Seller

### Clé substitut
- `Seller_SK`

### Clé métier
- `seller_id`

### Description
Dimension des vendeurs de la marketplace.

### Attributs retenus
Depuis `sellers` :
- `seller_id`
- `seller_zip_code_prefix`
- `seller_city`
- `seller_state`

Avec géolocalisation (optionnel) :
- `latitude`
- `longitude`

### Source
Table `sellers`, jointure possible avec `geolocation`.

### Rôle analytique
- analyser les vendeurs les plus actifs  
- comparer les performances par localisation  
- fournir des statistiques de qualité via les reviews  

---

# 6. D_PaymentType

### Clé substitut
- `PaymentType_SK`

### Clé métier
- `payment_type`

### Description
Liste des modes de paiement utilisés sur Olist.

### Attributs retenus
Depuis `order_payments` :
- `payment_type`  
- Optionnel :  
  - `is_card`  
  - `is_installment`  
  - `payment_category` (carte, cash-like, virement…)

### Source
Table `order_payments`.

### Rôle analytique
- identifier les types de paiement les plus utilisés  
- analyser les corrélations paiement ↔ retards, ventes, catégories  

---

# 7. D_OrderStatus

### Clé substitut
- `OrderStatus_SK`

### Clé métier
- `order_status`

### Description
Dimension représentant l’état final ou intermédiaire des commandes.

### Attributs possibles
- `order_status` (valeur brute)  
- `status_label_fr` (ex. Livrée, Expédiée, Annulée)  
- `status_category` (Finalisée / En cours / Annulée)

### Source
Table `orders`.

### Rôle analytique
- taux de commandes livrées à temps  
- analyses qualité par statut  
- calcul de KPIs opérationnels  

---

# 8. (Optionnel) D_Geolocation

### Clé substitut
- `Geo_SK`

### Clé métier
- `geolocation_zip_code_prefix`

### Description
Cette dimension regroupe latitude et longitude d’un préfixe postal.

### Attributs retenus
Depuis `geolocation` :
- `zip_code_prefix`
- `latitude`
- `longitude`
- `city`
- `state`

(Moyennage nécessaire si plusieurs lignes par zip prefix.)

### Source
Table `geolocation`.

### Rôle analytique
- analyses spatiales (cartes Power BI)  
- distances entre clients et vendeurs  
- distribution géographique des ventes  

---

# 9. Synthèse des dimensions retenues

| Dimension | Source | Rôle |
|----------|--------|-------|
| **D_Date** | Script fourni | Analyses temporelles |
| **D_Product** | products | Infos produit |
| **D_Category** | product_category_name_translation | Catégorie produit |
| **D_Customer** | customers + geolocation | Client réel |
| **D_Seller** | sellers + geolocation | Vendeur |
| **D_PaymentType** | order_payments | Mode de paiement |
| **D_OrderStatus** | orders | Statut commande |
| **D_Geolocation** (optionnel) | geolocation | Analyses spatiales |

---