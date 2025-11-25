
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

### Prochaines étapes
- Préparer le **mapping ETL** (source → dimensions → faits)
- Créer les scripts SQL pour :
  - les dimensions
  - la table de faits
- Commencer la mise en place du Data Warehouse (tables physiques)

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
