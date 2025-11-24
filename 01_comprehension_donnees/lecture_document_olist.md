# Lecture du document Olist – Compréhension du cas d’étude

Ce document résume et structure les informations clés issues du fichier *Labo BI Olist [FR].pdf*, afin de préparer la conception du modèle dimensionnel et du datawarehouse.

---

# 1. Contexte général

Le dataset Olist contient des données réelles issues du marketplace brésilien **Olist**, couvrant environ **100 000 commandes** entre **2016 et 2018**.  
Ces données sont anonymisées, mais conservent les relations commerciales réelles.

Olist est une plateforme permettant à des petits vendeurs de vendre leurs produits via le marketplace et de les expédier via des partenaires logistiques.

À la réception d’une commande, le client reçoit une enquête de satisfaction contenant :
- une **note** (1 à 5),
- un **commentaire**,
- des dates liées à l’expérience d’achat.

---

# 2. Ressources du labo

Le labo fournit :

### 1. Un *staging* déjà prêt  
Les données brutes (CSV) ont été transformées en **tables SQL** reproduisant exactement les schémas publics de Kaggle.

### 2. Un backup SQL : `Olist_Staging.bak`  
À restaurer dans SQL Server :

### 3. Deux scripts SQL fournis :  
- `Create_Populate_DateDimension.sql`  
- `Create_Populate_TimeDimension.sql`  

### 4. Ressources optionnelles  
- Excel : États brésiliens (abréviations et noms complets)  
- CSV : taux de change BRL → EUR (2016-2018)

---

# 3. Liste des tables du staging

Voici les **8 tables principales** (plus 1 table annexe de traduction) :  
*(les descriptions ci-dessous viennent du document)*

## 3.1 Customers
Contient :
- `customer_id` (identifiant pour chaque commande, pas unique par client)
- `customer_unique_id` (identifiant unique du client)
- `customer_zip_code_prefix`
- `customer_city`
- `customer_state`

**Important :**  
Un client reçoit un **customer_id différent par commande**, mais un **customer_unique_id stable**.

---

## 3.2 Geolocation
Coordonnées géographiques par zone de code postal :
- `geolocation_zip_code_prefix`
- `geolocation_lat`
- `geolocation_lng`
- `geolocation_city`
- `geolocation_state`

Une même zone postale peut apparaître plusieurs fois (données non agrégées).

---

## 3.3 Orders
Table centrale du dataset :

- `order_id`
- `customer_id`
- `order_status`
- `order_purchase_timestamp`
- `order_approved_at`
- `order_delivered_carrier_date`
- `order_delivered_customer_date`
- `order_estimated_delivery_date`

Permet de reconstituer tout le cycle de vie d’une commande.

---

## 3.4 Order_items
Détail des articles d’une commande :

- `order_id`
- `order_item_id` (numérotation séquentielle)
- `product_id`
- `seller_id`
- `shipping_limit_date`
- `price`
- `freight_value`

Exemple dans le document :  
Une commande avec 3 items → on additionne prix × quantité + fret × quantité pour obtenir le total.

---

## 3.5 Order_payments
Informations sur le paiement :

- `order_id`
- `payment_sequential`
- `payment_type` (carte, boleto, virement…)
- `payment_installments`
- `payment_value`

Une commande peut avoir **plusieurs séquences de paiement**.

---

## 3.6 Order_reviews
Avis des clients :

- `review_id`
- `order_id`
- `review_score`
- `review_comment_title`
- `review_comment_message`
- `review_creation_date`
- `review_answer_timestamp`

---

## 3.7 Products
Données descriptives d’un produit :

- `product_id`
- `product_category_name`
- `product_name_lenght`
- `product_description_lenght`
- `product_photos_qty`
- `product_weight_g`
- `product_length_cm`, `product_height_cm`, `product_width_cm`

---

## 3.8 Sellers
Informations sur les vendeurs :

- `seller_id`
- `seller_zip_code_prefix`
- `seller_city`
- `seller_state`

---

## 3.9 Product_category_name_translation
Permet de traduire les catégories portugaises → anglais :

- `product_category_name`
- `product_category_name_english`

---

# 4. Questions business à adresser

Le but du labo est de transformer le modèle relationnel en **modèle dimensionnel** pour répondre à des questions telles que :

- Montants et quantités par catégorie de produits  
- Identification des meilleurs clients  
- Meilleurs vendeurs  
- Produits les plus vendus  
- Évolution des ventes dans le temps  
- Types de paiements les plus utilisés  
- Commandes livrées à temps vs en retard  
- Produits / vendeurs les mieux notés  
- Distribution géographique des ventes  
- Etc.

Ces questions guideront la structure du **DW** (dimensions + faits).

---

# 5. Recommandations du document

### 5.1 Planning idéal (6–7 jours)

- **Jour 1** : compréhension des données (**c’est ce document**)  
- **Jour 2** : réflexion + schéma du modèle dimensionnel  
- **Jour 3-5** : mise en place du DW via ETL/SSIS  
- **Jour 6-7** : construction de rapports BI

### 5.2 Conseils clés
- Commencer petit → se concentrer sur **les ventes**  
- Plusieurs choix de modèle sont possibles selon l’angle d’analyse  
- Atteindre au moins un modèle “similaire” pour toute la classe  
- Ne pas hésiter à demander de l’aide si on se perd

---

# 6. Premières conclusions pour la suite

À partir de ce document, les éléments importants pour la prochaine étape (modèle dimensionnel) sont :

✔ Entité centrale : **Orders**, enrichie par `order_items`  
✔ Tables satellites : Customers, Sellers, Products, Payments, Reviews  
✔ Grain naturel de la table de faits : **lignes de order_items**  
✔ Dimensions candidates :  
- Date  
- Produit  
- Client  
- Vendeur  
- Catégorie  
- Paiement  
- OrderStatus  
- Géolocalisation  

---
