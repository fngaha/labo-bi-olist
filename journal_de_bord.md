
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

### Prochaines étapes

- Préparer les fichiers suivants :
  - `description_dimensions.md`
  - `description_faits.md`
- Concevoir le **schéma en étoile** dans `schema_etoile.drawio`.
- Valider définitivement :
  - le grain de la table de faits,
  - la liste des dimensions,
  - les mesures principales.

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
