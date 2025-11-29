
# Journal de bord – Labo BI Olist

Ce journal retrace, étape par étape, la réalisation du labo BI Olist :
- Compréhension des données
- Conception du modèle dimensionnel
- Mise en place de l’ETL et du datawarehouse
- Réalisation des rapports BI

---

## Séance 1 – [2025-11-24]

### Objectif principal
Comprendre en profondeur les données Olist et analyser le staging fourni (première étape du labo).

---

### Tâches réalisées

- Lecture complète du document explicatif *Labo BI Olist* fourni par le formateur.
- Création du fichier `lecture_document_olist.md` :
  - Résumé du contexte Olist.
  - Description des ressources fournies (staging, scripts, fichiers optionnels).
  - Présentation des 9 datasets principaux.
  - Liste des questions business visées par le labo.
  - Synthèse des recommandations du document.
- Création du fichier `analyse_staging.md` :
  - Analyse détaillée de chaque table du staging : orders, order_items, order_payments, order_reviews, products, sellers, customers, geolocation, et catégorie.
  - Reconstitution des relations entre tables (modèle relationnel).
  - Identification des clés importantes (PK, FK).
  - Définition du rôle fonctionnel de chaque table.
- Identification des premières directions pour le modèle dimensionnel :
  - Grain pressenti du fait : **1 ligne = 1 article de commande (order_id, order_item_id)**.
  - Dimensions candidates : Date, Produit, Client, Vendeur, Catégorie, Paiement, Géolocalisation, OrderStatus.
- Préparation pour la prochaine étape (modélisation dimensionnelle).

---

### Décisions importantes

- Le point d’entrée central du modèle = table `orders`.
- La table `order_items` définira le **grain de la future table de faits F_Ventes_Items**.
- `customer_unique_id` sera utilisé pour identifier un client réel, contrairement à `customer_id`.
- `payment_type`, `product_category_name`, `order_status` deviennent naturellement des dimensions.
- La géolocalisation pourra être intégrée dans les dimensions Customer/Seller ou dans une dimension séparée.

---

### Difficultés rencontrées

- Compréhension de la différence entre `customer_id` (par commande) et `customer_unique_id` (client réel).
- Multiplicité des lignes dans `order_payments` pour une même commande.
- Données de géolocalisation non agrégées (plusieurs lignes par zip prefix).
- Volume des données nécessitant une organisation stricte.

---

## Séance 2 – [2025-11-25]

### Objectif principal
Concevoir entièrement le modèle dimensionnel du projet Olist : dimensions, table de faits et schéma en étoile.

---

### Tâches réalisées

- Création du fichier `description_dimensions.md` décrivant en détail toutes les dimensions du modèle :
  - D_Date  
  - D_Product  
  - D_Category  
  - D_Customer  
  - D_Seller  
  - D_PaymentType  
  - D_OrderStatus  

- Création du fichier `description_faits.md` :
  - Validation du grain : **1 ligne = 1 article d’une commande (order_id, order_item_id)**  
  - Définition des mesures : Quantity, Item_Price, Freight_Value, Item_Total  
  - Définition des FK vers dimensions  
  - Ajout des attributs dégénérés  

- Conception du schéma en étoile :
  - Création du fichier `schema_etoile.drawio`
  - Export en PNG `schema_etoile.png`
  - Ajout de toutes les dimensions et connecteurs PK/FK
  - Vérification de la disposition et du rendu professionnel

---

### Décisions importantes

- Le grain de la table de faits est fixé à **l’article de commande** (niveau le plus fin).
- Les dimensions définitives sont validées :
  - Date (plusieurs rôles : achat, livraison réelle, livraison estimée)
  - Produit
  - Catégorie
  - Client
  - Vendeur
  - Type de paiement
  - Statut de commande
- Les mesures principales validées :
  - Quantity = 1  
  - Item_Price  
  - Freight_Value  
  - Item_Total  

---

### Difficultés rencontrées
- Trouver la meilleure manière de représenter plusieurs dates dans un schéma en étoile.
- Organiser proprement les attributs dans diagrams.net.
- Décider si D_Geolocation devait être intégrée ou séparée.

---

## Séance 3 – [2025-11-29]

### Objectif principal
Mettre en place un premier flux ETL 100 % Python (SQLAlchemy + pandas) entre le staging Olist et le datawarehouse, en commençant par la dimension D_Category.

---

### Tâches réalisées

- Définition du mapping ETL entre le staging Olist et le datawarehouse

- Création de la base de datawarehouse :
  - Création de la base `Olist_DW` dans SQL Server.

- Création des tables de dimension dans `Olist_DW` :
  - `D_Date` (via le script `Create_Populate_DateDimension.sql`)
  - `D_Category`
  - `D_Product`
  - `D_Customer`
  - `D_Seller`
  - `D_PaymentType`
  - `D_OrderStatus`

- Mise en place de l’architecture ETL Python dans `03_etl/etl/` :
  - `config.yaml` : paramètres de connexion à SQL Server (staging + DW)
  - `db_connection.py` : connexion via SQLAlchemy + pyodbc, authentification Windows (`Trusted_Connection`)
  - `extract_staging.py` : lecture des tables de staging (`products`, `customers`, `sellers`, `orders`, `order_payments`, `product_category_name_translation`, …)
  - `extract_dw.py` : lecture de certaines dimensions déjà chargées (ex : `D_Category` pour récupérer `Category_SK`)
  - `transform_dimensions.py` : logique de transformation pour :
    - `D_Category` (distinct des catégories à partir de `product_category_name_translation`)
    - `D_Product` (join avec `D_Category` pour récupérer `Category_SK`)
    - `D_Customer` (1 ligne par `customer_unique_id`)
    - `D_Seller` (1 ligne par `seller_id`)
    - `D_PaymentType` (liste distincte des `payment_type`)
    - `D_OrderStatus` (liste distincte des `order_status`)
  - `load_dimensions.py` : chargement des DataFrames dans les tables DW (`TRUNCATE` + `to_sql`)
  - `main.py` : fonctions `run_etl_d_category`, `run_etl_d_product`, `run_etl_d_customer`, `run_etl_d_seller`, `run_etl_d_payment_type`, `run_etl_d_order_status`
  - `test_connexion.py` : script de test de la connexion à `Olist_Staging` via SQLAlchemy.

- Mise en place d’un petit script de test de connexion :
  - `test_connexion.py` pour valider l’accès à `Olist_Staging` via SQLAlchemy.

- Exécution et validation des ETL dimensionnels :
  - Lancement des ETL Python dimension par dimension.
  - Vérification dans SQL Server que les tables suivantes sont correctement alimentées :
    - `Olist_DW.dbo.D_Category`
    - `Olist_DW.dbo.D_Product`
    - `Olist_DW.dbo.D_Customer`
    - `Olist_DW.dbo.D_Seller`
    - `Olist_DW.dbo.D_PaymentType`
    - `Olist_DW.dbo.D_OrderStatus`

---

### Points techniques importants

- Utilisation de **SQLAlchemy** avec le driver ODBC `ODBC Driver 17 for SQL Server` et authentification Windows sur l’instance nommée `GOS-VDI410\TFTIC` (`Trusted_Connection=yes`).
- Découpage clair de l’ETL :
  - EXTRACT (staging, DW)
  - TRANSFORM (construction des dimensions)
  - LOAD (insertion dans le DW)
- Respect du grain choisi :
  - `D_Product` : 1 ligne par `product_id`
  - `D_Customer` : 1 ligne par `customer_unique_id`
  - `D_Seller` : 1 ligne par `seller_id`
  - `D_PaymentType` : 1 ligne par `payment_type`
  - `D_OrderStatus` : 1 ligne par `order_status`

---

### Prochaines étapes

- Créer le script SQL de la table de faits `F_Ventes_Items` dans `Olist_DW`.
- Implémenter l’ETL Python pour la table de faits à partir des tables de staging (`order_items`, `orders`, `order_payments`, `products`, `customers`, `sellers`).
- Vérifier l’intégrité référentielle (lookups vers toutes les dimensions) et les mesures calculées.

---

## Séance 3 – [2025-11-29]

### Objectif principal
Créer la table de faits `F_Ventes_Items` dans le datawarehouse `Olist_DW` et implémenter l’ETL Python complet permettant de charger les ventes au niveau du détail des lignes de commande (grain : 1 ligne par item de commande).

---

### Tâches réalisées

- Création de la table de faits dans `Olist_DW` :
  - Script SQL `Create_F_Ventes_Items.sql` avec :
    - Clé technique `Fact_SK` (IDENTITY)
    - Clés étrangères vers :
      - `D_Date` (`Date_SK`)
      - `D_Product` (`Product_SK`)
      - `D_Customer` (`Customer_SK`)
      - `D_Seller` (`Seller_SK`)
      - `D_PaymentType` (`PaymentType_SK`)
      - `D_OrderStatus` (`OrderStatus_SK`)
    - Identifiants opérationnels :
      - `order_id`, `order_item_id`
    - Mesures :
      - `price`, `freight_value`, `quantity`
      - colonne calculée `total_item_value = price * quantity`
      - `total_weight_g`
    - Timestamps :
      - `order_purchase_timestamp`
      - `order_delivered_customer_date`

- Mise en place de l’ETL Python pour la table de faits dans `03_etl/etl/` :
  - `extract_staging.py` :
    - ajout de `extract_order_items()` pour lire `order_items`
  - `extract_dw.py` :
    - ajout de fonctions de lecture des dimensions avec leurs SK :
      - `read_d_date()`
      - `read_d_product()`
      - `read_d_customer()`
      - `read_d_seller()`
      - `read_d_payment_type()`
      - `read_d_order_status()`
  - `transform_facts.py` :
    - fonction `build_fact_ventes_items(...)` qui :
      - joint `order_items` et `orders` (client, statut, timestamps)
      - enrichit avec `customers` (customer_unique_id), `products` (poids), `sellers`
      - identifie le paiement principal via `order_payments` (`payment_sequential = 1`)
      - dérive la date d’achat (`order_purchase_date`) et fait le lookup vers `D_Date` (via `Date_Actual`)
      - fait les lookups SK vers :
        - `D_Product` (via `product_id`)
        - `D_Customer` (via `customer_unique_id`)
        - `D_Seller` (via `seller_id`)
        - `D_PaymentType` (via `payment_type`)
        - `D_OrderStatus` (via `order_status`)
      - calcule les mesures :
        - `quantity` (1 par ligne de `order_items`)
        - `total_weight_g = product_weight_g * quantity`
  - `load_facts.py` :
    - fonction `load_fact_ventes_items(...)` avec :
      - `TRUNCATE TABLE dbo.F_Ventes_Items`
      - insertion via `to_sql` dans `Olist_DW.dbo.F_Ventes_Items`
  - `main.py` :
    - ajout de la fonction `run_etl_fact_ventes_items()` orchestrant :
      - EXTRACT des tables de staging nécessaires
      - EXTRACT des dimensions DW
      - TRANSFORM via `build_fact_ventes_items(...)`
      - LOAD via `load_fact_ventes_items(...)`

- Exécution et validation de l’ETL de la table de faits :
  - Lancement de `run_etl_fact_ventes_items()` dans la VM.
  - Vérification dans SQL Server :
    - `SELECT TOP 10 * FROM Olist_DW.dbo.F_Ventes_Items;`
    - `SELECT COUNT(*) FROM Olist_DW.dbo.F_Ventes_Items;`
  - Constat : la table de faits est correctement alimentée avec toutes les SK et les mesures.

---

### Points techniques importants

- L’ETL de la table de faits repose sur les dimensions déjà chargées au préalable.
- La table de faits utilise `order_purchase_timestamp` comme base pour le lien vers `D_Date`.
- Le type de paiement utilisé est le paiement principal (`payment_sequential = 1`) pour affecter `PaymentType_SK`.
- Le grain de la fact est bien : **1 ligne par combinaison (`order_id`, `order_item_id`)**.

---

### Prochaines étapes

- Connecter `Olist_DW` à Power BI pour construire les premiers rapports (ventes par produit, par vendeur, par client, par type de paiement, par statut, par période…).

---

## Bilan final

**Résumé global :**

- Ce que j’ai appris sur :
  - le modèle relationnel vs dimensionnel
  - les faits et dimensions
  - la mise en place d’un DW
  - la création de rapports BI

**Améliorations possibles :**

- Si je devais recommencer, je ferais : …
- Pistes de prolongement du labo : …
