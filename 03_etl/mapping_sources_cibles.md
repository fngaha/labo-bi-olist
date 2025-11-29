# Mapping ETL – Olist (staging → datawarehouse)

Ce document décrit les règles de mapping entre les tables du **staging Olist** et les tables du **datawarehouse** (dimensions et table de faits F_Ventes_Items).

L’ETL suit le cycle classique :

1. EXTRACT : lecture des tables de staging
2. TRANSFORM : jointures, agrégations, nettoyages, calculs
3. LOAD : alimentation des dimensions, puis de la table de faits

---

# 1. Ordre de chargement des tables du DW

Ordre recommandé :

1. **D_Date** (script fourni)
2. **D_Category**
3. **D_Product**
4. **D_Customer**
5. **D_Seller**
6. **D_PaymentType**
7. **D_OrderStatus**
9. **F_Ventes_Items**

Chaque dimension doit être remplie avant la table de faits, car F_Ventes_Items contient des FK vers ces dimensions.

---

# 2. Mapping des dimensions

## 2.1 D_Date

> Par le script (`Create_Populate_DateDimension.sql`).

**Source :** aucune table Olist directement (dimension de temps générique).  
**Cible :** `D_Date` dans le DW.

Principes :

- Population de toutes les dates couvrant la période des données Olist (2016–2018).
- Clé substitut : `Date_SK` (généralement AAAAMMJJ ou ID auto).
- Attributs : année, trimestre, mois, jour, nom du jour, etc.

---

## 2.2 D_Category

**Source principale :** `Category_name_translation` (staging)  
**Cible :** `D_Category` (DW)

| Colonne cible       | Source                               | Règles de transformation                           |
|---------------------|--------------------------------------|----------------------------------------------------|
| Category_SK         | (générée dans DW)                   | Clé substitut (IDENTITY ou séquence)              |
| product_category_name | product_category_name              | Valeur telle quelle (PT)                           |
| product_category_name_english | product_category_name_english | Valeur telle quelle (EN)                        |

Règles :

- Charger **une ligne par catégorie distincte**.
- Ajouter une ligne spéciale “Unknown” si nécessaire pour gérer les valeurs NULL ou inconnues.

---

## 2.3 D_Product

**Sources :**  
- `Products`  
- `product_category_name_translation` (via product_category_name)  

**Cible :** `D_Product`

| Colonne cible                 | Source                                 | Règles de transformation                                           |
|------------------------------|----------------------------------------|--------------------------------------------------------------------|
| Product_SK                   | (générée dans DW)                     | Clé substitut                                                     |
| product_id                   | Products.product_id                    | Copie telle quelle                                                |
| Category_SK                  | D_Category.Category_SK                | Lookup via Products.product_category_name                          |
| product_category_name        | Products.product_category_name         | Copie telle quelle                                                |
| product_name_lenght          | Products.product_name_lenght           | Copie telle quelle                                                |
| product_description_lenght   | Products.product_description_lenght    | Copie telle quelle                                                |
| product_photos_qty           | Products.product_photos_qty            | Copie telle quelle                                                |
| product_weight_g             | Products.product_weight_g              | Copie telle quelle                                                |
| product_length_cm            | Products.product_length_cm             | Copie telle quelle                                                |
| product_height_cm            | Products.product_height_cm             | Copie telle quelle                                                |
| product_width_cm             | Products.product_width_cm              | Copie telle quelle                                                |

Règles :

- 1 ligne dans D_Product par `product_id` distinct.
- La colonne `Category_SK` est obtenue via un **lookup** sur D_Category :
  - join sur `product_category_name`.

---

## 2.4 D_Customer

**Source principale :** `Customer`  
**Source géoloc :** `geolocation` (via zip prefix)  

**Cible :** `D_Customer`

| Colonne cible            | Source                          | Règles de transformation                                         |
|--------------------------|---------------------------------|------------------------------------------------------------------|
| Customer_SK              | (générée dans DW)              | Clé substitut                                                    |
| customer_unique_id       | Customer.customer_unique_id    | Utilisé comme clé métier stable                                  |
| customer_id              | Customer.customer_id           | Identifiant par commande (référence staging)                     |
| customer_zip_code_prefix | Customer.customer_zip_code_prefix | Copie telle quelle                                          |
| customer_city            | Customer.customer_city         | Copie telle quelle                                              |
| customer_state           | Customer.customer_state        | Copie telle quelle                                              |
| latitude                 | geolocation.geolocation_lat     | Moyenne de lat par zip prefix (ou première valeur)               |
| longitude                | geolocation.geolocation_lng     | Moyenne de lng par zip prefix (ou première valeur)               |

Règles :

- 1 ligne par `customer_unique_id` (client réel).
- Gérer les cas où un `customer_unique_id` correspond à plusieurs lignes (choisir une valeur de zip/city/state cohérente).
- Possibilité de garder un `customer_id` “récent” ou “premier”.

---

## 2.5 D_Seller

**Source principale :** `Sellers`  
**Source géoloc :** `geolocation`

**Cible :** `D_Seller`

| Colonne cible            | Source                          | Règles de transformation                                         |
|--------------------------|---------------------------------|------------------------------------------------------------------|
| Seller_SK                | (générée dans DW)              | Clé substitut                                                    |
| seller_id                | Sellers.seller_id              | Clé métier                                                       |
| seller_zip_code_prefix   | Sellers.seller_zip_code_prefix | Copie telle quelle                                               |
| seller_city              | Sellers.seller_city            | Copie telle quelle                                               |
| seller_state             | Sellers.seller_state           | Copie telle quelle                                               |
| latitude                 | geolocation.geolocation_lat     | Moyenne de lat par zip prefix (ou première valeur)               |
| longitude                | geolocation.geolocation_lng     | Moyenne de lng par zip prefix (ou première valeur)               |

Règles :

- 1 ligne par vendeur (`seller_id` unique).

---

## 2.6 D_PaymentType

**Source principale :** `Order_payments`

**Cible :** `D_PaymentType`

| Colonne cible   | Source                 | Règles de transformation                                                   |
|-----------------|------------------------|----------------------------------------------------------------------------|
| PaymentType_SK  | (générée dans DW)     | Clé substitut                                                              |
| payment_type    | Order_payments.payment_type | `DISTINCT` sur payment_type                                         |

Règles :

- Charger la liste distincte des `payment_type` rencontrés (ex: credit_card, boleto, voucher…).
- Ajouter éventuellement une catégorie dérivée (carte / non carte) dans une version ultérieure.

---

## 2.7 D_OrderStatus

**Source principale :** `Orders`

**Cible :** `D_OrderStatus`

| Colonne cible      | Source              | Règles de transformation                               |
|--------------------|---------------------|--------------------------------------------------------|
| OrderStatus_SK     | (générée dans DW)  | Clé substitut                                          |
| order_status       | Orders.order_status | Liste distincte des statuts                            |
| status_label_fr    | (dérivée)          | Traduction (delivered → Livrée, shipped → Expédiée…)   |
| status_category    | (dérivée)          | Regroupement : Finalisée / En cours / Annulée          |

Règles :

- 1 ligne par valeur distincte de `order_status`.
- Les libellés FR peuvent être codés “en dur” dans l’ETL ou via une petite table de référence.

---

# 3. Mapping de la table de faits F_Ventes_Items

**Sources principales :**

- `order_items`
- `orders`
- `order_payments`
- `products`
- `customers`
- `sellers`

**Cible :** `F_Ventes_Items`

## 3.1 Jointures logiques

1. `order_items`  
   - join `orders` on `order_items.order_id = orders.order_id`
   - join `products` on `order_items.product_id = products.product_id`
   - join `sellers` on `order_items.seller_id = sellers.seller_id`

2. `orders`  
   - join `customers` on `orders.customer_id = customers.customer_id`
   - join `order_payments` on `orders.order_id = order_payments.order_id`
     - éventuellement filtrer sur `payment_sequential = 1` (mode principal)

3. `products`  
   - join `product_category_name_translation` sur `product_category_name` si besoin

## 3.2 Mapping des colonnes de F_Ventes_Items

### Clé substitut

| Colonne cible | Source | Règles |
|---------------|--------|--------|
| SalesItem_SK  | (générée dans DW) | IDENTITY ou séquence |

---

### Clés étrangères vers dimensions

| Colonne cible             | Source / Règle                                                                 |
|---------------------------|-------------------------------------------------------------------------------|
| DatePurchase_SK           | Lookup dans D_Date à partir de `orders.order_purchase_timestamp`            |
| DateDelivered_SK          | Lookup dans D_Date à partir de `orders.order_delivered_customer_date`       |
| DateEstimatedDelivery_SK  | Lookup dans D_Date à partir de `orders.order_estimated_delivery_date`       |
| Product_SK                | Lookup D_Product via `order_items.product_id`                                |
| Category_SK               | Lookup D_Category via `products.product_category_name`                        |
| Customer_SK               | Lookup D_Customer via `customers.customer_unique_id`                          |
| Seller_SK                 | Lookup D_Seller via `order_items.seller_id`                                  |
| PaymentType_SK            | Lookup D_PaymentType via `order_payments.payment_type` (souvent séquence 1)  |
| OrderStatus_SK            | Lookup D_OrderStatus via `orders.order_status`                               |

Règles :

- Si un lookup échoue (clé non trouvée) → utiliser une clé “Unknown” (ex : `-1` ou `0`) dans chaque dimension.

---

### Attributs dégénérés

| Colonne cible      | Source                             | Règles |
|--------------------|------------------------------------|--------|
| Order_ID           | order_items.order_id               | Copie telle quelle (clé business de la commande) |
| OrderItem_Number   | order_items.order_item_id          | Copie telle quelle                                |

---

### Mesures

| Colonne cible   | Source                    | Règles |
|-----------------|---------------------------|--------|
| Quantity        | (dérivé)                  | Toujours = 1 (1 ligne = 1 article) |
| Item_Price      | order_items.price         | Copie telle quelle                 |
| Freight_Value   | order_items.freight_value | Copie telle quelle                 |
| Item_Total      | (calcul)                  | `price + freight_value`            |

Règles :

- Tous les montants sont initialement en BRL.
- Si souhaité, possibilité de créer des versions EUR dans une étape ultérieure (via table de taux de change).

---

# 4. Gestion des valeurs inconnues / défaut

Pour assurer l’intégrité référentielle :

- Chaque dimension (sauf D_Date) doit contenir une ligne “inconnue” :
  - `Customer_SK = 0`, `customer_unique_id = 'UNKNOWN'`, etc.
  - `Product_SK = 0`, `product_id = 'UNKNOWN'`, etc.

Lors du chargement de F_Ventes_Items :

- Si un lookup ne trouve pas de SK correspondant :
  - utiliser la SK “Unknown” de la dimension concernée.

---

# 5. Résumé de l’ETL

1. Charger D_Date avec le script fourni.
2. Charger successivement D_Category, D_Product, D_Customer, D_Seller, D_PaymentType, D_OrderStatus.
3. Mettre en place les **lookups** nécessaires dans l’ETL (SSIS ou autre).
4. Charger F_Ventes_Items en :
   - lisant `order_items` comme source principale,
   - joignant `orders`, `customers`, `sellers`, `products`, `order_payments`,
   - effectuant les lookups de SK,
   - calculant les mesures (Item_Total, etc.).

Ce mapping constitue la base de tous les flux ETL pour le laboratoire Olist.
