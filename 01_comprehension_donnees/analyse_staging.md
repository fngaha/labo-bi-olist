# Analyse du staging Olist

Ce document décrit en détail les tables du staging fournies dans le cadre du labo Olist.  
L’objectif est de comprendre les relations, les clés et le rôle de chaque table afin de concevoir un modèle dimensionnel cohérent.

---

# 1. Vue d’ensemble du staging

Le staging Olist contient **8 tables principales**, plus une table annexe de traduction.  
Ces tables sont dérivées directement du dataset public Kaggle Olist.

Elles couvrent les thèmes suivants :

- **Commandes**
- **Articles de commande**
- **Paiements**
- **Avis clients**
- **Produits**
- **Clients**
- **Vendeurs**
- **Localisation géographique**

Le staging correspond à un modèle relationnel classique.

---

# 2. Analyse détaillée des tables

## 2.1 `orders`

C’est la **table centrale** du dataset.  
Elle décrit le cycle de vie de chaque commande.

| Champ | Description |
|-------|-------------|
| order_id | Identifiant unique de la commande |
| customer_id | Identifiant du client (change à chaque commande) |
| order_status | Statut de la commande (delivered, shipped, canceled...) |
| order_purchase_timestamp | Date et heure d’achat |
| order_approved_at | Date d’approbation du paiement |
| order_delivered_carrier_date | Date de transmission au transporteur |
| order_delivered_customer_date | Date réelle de réception |
| order_estimated_delivery_date | Date estimée de livraison |

### Points importants
- Les dates permettent d’analyser les **délais de livraison** et les **retards**.
- `order_status` est une dimension candidate simple.
- `customer_id` n’est pas stable : le même client peut avoir plusieurs `customer_id`.

---

## 2.2 `order_items`

Détail des articles contenus dans chaque commande.

| Champ | Description |
|-------|-------------|
| order_id | Identifie la commande |
| order_item_id | Numéro d’ordre de l’article dans la commande |
| product_id | Produit acheté |
| seller_id | Vendeur |
| shipping_limit_date | Date limite d’expédition |
| price | Prix unitaire |
| freight_value | Frais de transport pour cet item |

### Points importants
- **Grain naturel du fait** : (order_id, order_item_id)
- Chaque ligne = **un article**.
- Le prix total d’une commande = somme(item.price × quantité).
- Le fret total = somme(freight_value).

`order_items` est la **source principale de la future table des faits**.

---

## 2.3 `order_payments`

Informations sur les paiements des commandes.

| Champ | Description |
|-------|-------------|
| order_id | Référence de la commande |
| payment_sequential | Numéro de séquence de paiement |
| payment_type | Type de paiement (carte, boleto, virement…) |
| payment_installments | Nombre de mensualités |
| payment_value | Valeur du paiement |

### Points importants
- Une commande peut avoir **plusieurs méthodes de paiement**.
- `payment_type` est une bonne **dimension indépendante**.
- Le total des séquences = montant total payé.

---

## 2.4 `order_reviews`

Avis des clients après livraison.

| Champ | Description |
|-------|-------------|
| review_id | Identifiant unique de l’avis |
| order_id | Référence de la commande |
| review_score | Note de 1 à 5 |
| review_comment_title | Titre |
| review_comment_message | Message |
| review_creation_date | Date d’envoi de l’enquête |
| review_answer_timestamp | Date de réponse |

### Points importants
- Les notes permettent d’analyser la **qualité des produits** et des **vendeurs**.
- `order_id` permet de relier review ↔ commande.

---

## 2.5 `products`

Description des produits vendus.

| Champ | Description |
|-------|-------------|
| product_id | Identifiant du produit |
| product_category_name | Catégorie (PT) |
| product_name_lenght | Longueur du nom |
| product_description_lenght | Taille de la description |
| product_photos_qty | Nombre de photos |
| product_weight_g | Poids |
| product_length_cm, product_height_cm, product_width_cm | Dimensions |

### Points importants
- Attributs parfaits pour une **dimension Produit riche**.
- La catégorie est en portugais → besoin de la table de traduction.

---

## 2.6 `sellers`

Informations sur les vendeurs.

| Champ | Description |
|-------|-------------|
| seller_id | Identifiant |
| seller_zip_code_prefix | Code postal (préfixe) |
| seller_city | Ville |
| seller_state | État |

### Points importants
- Les vendeurs sont essentiels pour les analyses de type :
  - meilleurs vendeurs
  - temps de livraison par vendeur
  - qualité des produits livrés par vendeur (via reviews)

---

## 2.7 `customers`

Informations géographiques et ID client.

| Champ | Description |
|-------|-------------|
| customer_id | Identifiant utilisé pour la commande |
| customer_unique_id | Identifiant stable du client |
| customer_zip_code_prefix | Préfixe du code postal |
| customer_city | Ville |
| customer_state | État |

### Points importants
- Pour repérer les **clients fidèles**, utiliser **customer_unique_id**.
- Pour lier aux coordonnées → jointure avec `geolocation`.

---

## 2.8 `geolocation`

Données de latitude/longitude par zone de code postal.

| Champ | Description |
|-------|-------------|
| geolocation_zip_code_prefix | Code postal |
| geolocation_lat | Latitude |
| geolocation_lng | Longitude |
| geolocation_city | Ville |
| geolocation_state | État |

### Points importants
- Le lien avec Customer/Seller se fait via le **zip prefix**.
- Plusieurs lignes peuvent exister pour la même zone → nécessité possible d’agrégation.

---

## 2.9 `product_category_name_translation`

Permet d’obtenir le nom EN des catégories.

| Champ | Description |
|-------|-------------|
| product_category_name | Catégorie en portugais |
| product_category_name_english | Catégorie en anglais |

### Points importants
- Table essentielle pour :  
  - graphes propres  
  - labels intelligibles  
  - regroupements par catégorie

---

# 3. Liens entre les tables

Voici les principales relations du modèle relationnel :

Orders (1) ---- (N) Order_items ---- (N) Products

|
+-----(N) Sellers

Orders (1) ---- (N) Order_payments

Orders (1) ---- (1) Customers

Orders (1) ---- (1) Order_reviews

Customers ----(N)---- Geolocation (via zip prefix)

Sellers ----(N)---- Geolocation (via zip prefix)

Products ----(1)---- Product_category_name_translation

---

# 4. Informations clés pour la modélisation dimensionnelle

### 4.1 Grain de la table de faits
Le grain le plus logique :  
**1 ligne = 1 article d’une commande** → (order_id, order_item_id)

### 4.2 Dimensions candidates

| Dimension | Source |
|----------|--------|
| Date | Dates de `orders` |
| Produit | `products` + traduction catégorie |
| Vendeur | `sellers` |
| Client | `customers` |
| Catégorie | `product_category_name_translation` |
| Paiement | `order_payments` |
| Statut commande | `order_status` |
| Géolocalisation | via `geolocation` |

---

## 5. Schéma du modèle relationnel (staging)

Le schéma complet du staging fourni dans le document Olist est disponible dans :
01_comprehension_donnees/diagrammes/staging_schema.png

Ce schéma illustre visuellement les relations décrites dans ce fichier :

- orders est bien la table centrale du modèle relationnel.
- order_items dépend de orders via order_id, et relie produits et vendeurs.
- order_payments et order_reviews sont rattachés directement à orders.
- products est reliée à la table de traduction des catégories.
- customers et sellers sont liés par leur zip_code_prefix aux données de géolocalisation.

Cette visualisation permet de valider :

1. Les cardinalités :

- 1 commande → N items
- 1 commande → N paiements
- 1 commande → 1 review (optionnelle)
- N clients → N zones géographiques

2. Les clés importantes pour la modélisation dimensionnelle

3. La justification du grain de la future table de faits

4. La liste des dimensions candidates (produit, client, vendeur, catégorie, dates, etc.)

Le diagramme sert de base à la construction du schéma en étoile dans la prochaine étape.

---

# 6. Conclusion

Le staging Olist fournit une base riche et cohérente pour construire un modèle dimensionnel centré sur les ventes.

La prochaine étape consiste à :

- valider le grain de la table de faits,  
- décrire les dimensions,  
- puis produire un **schéma en étoile**.

