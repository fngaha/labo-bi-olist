# Description de la table de faits – F_Ventes_Items

Ce document décrit la table de faits principale du modèle dimensionnel Olist :  
 **F_Ventes_Items**, centrée sur les ventes et dérivée de la table `order_items` du staging.

---

# 1. Grain de la table de faits

Le grain représente le niveau de détail d'une ligne dans la table de faits.

### Grain retenu :
> **1 ligne = 1 article d’une commande**  
> Identifié par le couple *(order_id, order_item_id)*

Ce grain permet d’analyser les ventes au niveau le plus fin :
- par commande  
- par produit  
- par vendeur  
- par client  
- par catégorie  
- par date  
- par type de paiement  
- etc.

Ce choix est conforme au fonctionnement du staging Olist où chaque ligne de `order_items` représente un **article individuel** acheté.

---

# 2. Structure logique de F_Ventes_Items

La table de faits est composée de :

- **Clés techniques (clé substitut)**
- **Clés étrangères vers les dimensions**
- **Mesures (faits)**
- **Informations dégénérées**

---

# 3. Clé substitut

| Colonne | Type | Description |
|---------|------|-------------|
| `SalesItem_SK` | INT (identity) | Identifiant interne de la ligne de fait |

La clé substitut n’a pas de signification métier : elle sert à optimiser l’ETL et les relations.

---

# 4. Clés étrangères (FK) vers les dimensions

| FK | Dimension cible | Source staging | Commentaire |
|----|-----------------|----------------|-------------|
| `DatePurchase_SK` | D_Date | `orders.order_purchase_timestamp` | Date d’achat |
| `DateDelivered_SK` | D_Date | `orders.order_delivered_customer_date` | Date réelle de livraison |
| `DateEstimatedDelivery_SK` | D_Date | `orders.order_estimated_delivery_date` | Date estimée |
| `Product_SK` | D_Product | `order_items.product_id` | Produits vendus |
| `Customer_SK` | D_Customer | `orders.customer_id` + `customers.customer_unique_id` | Client réel |
| `Seller_SK` | D_Seller | `order_items.seller_id` | Vendeur |
| `PaymentType_SK` | D_PaymentType | `order_payments.payment_type` | Mode de paiement principal |
| `OrderStatus_SK` | D_OrderStatus | `orders.order_status` | Statut de la commande |
| `Category_SK` | D_Category | via `products.product_category_name` | Catégorie du produit |

### Notes importantes
- **Plusieurs dates** permettent d’analyser les retards & délais.
- La dimension PaymentType utilise une simplification : on prend le **mode de paiement principal** (souvent la séquence 1).
- La dimension Category est dérivée de D_Product (relation en étoile "produit → catégorie").

---

# 5. Mesures (faits)

Les faits proviennent principalement de `order_items`, mais peuvent être enrichis.

### 5.1 Mesures de base

| Mesure | Type | Source | Description |
|--------|------|--------|-------------|
| `Quantity` | INT | dérivé | Toujours = 1 (1 ligne = 1 article) |
| `Item_Price` | DECIMAL | `order_items.price` | Prix unitaire |
| `Freight_Value` | DECIMAL | `order_items.freight_value` | Frais de livraison pour cet article |
| `Item_Total` | DECIMAL | calculé | `price + freight_value` |

---

### 5.2 Mesures calculées (optionnelles)

| Mesure | Description |
|--------|-------------|
| `Order_Total` | total par commande (calcul dans les rapports) |
| `Revenue_Product` | somme des `Item_Price` |
| `Freight_Total` | somme des `Freight_Value` |
| `Is_Delayed` | indicateur : 1 si livraison réelle > livraison estimée |
| `Item_Total_EUR` | conversion via taux de change (données optionnelles du labo) |

---

# 6. Attributs dégénérés

Ces attributs n’ont pas leur propre dimension, mais sont utiles pour les analyses opérationnelles.

| Colonne | Source | Description |
|---------|--------|-------------|
| `Order_ID` | staging | Identifiant de commande |
| `OrderItem_Number` | staging | Correspond à `order_item_id` |

Ces attributs permettent par exemple :
- d’analyser les ventes par commande
- de remonter aux détails dans les rapports Power BI
- d’avoir une granularité fidèle au staging

---

# 7. Schéma logique de F_Ventes_Items

Ci-dessous une représentation simplifiée du schéma en étoile centré sur la table de faits **F_Ventes_Items** :

```text
                 D_Date
                    ↑
 D_Customer   ←  F_Ventes_Items  →  D_Product  →  D_Category
                    ↓
                 D_Seller

      D_PaymentType        D_OrderStatus

```

---

# 8. Rôle analytique de F_Ventes_Items

La table F_Ventes_Items permet de répondre à toutes les questions BI liées aux ventes :

### Analyses commerciales
- Quels sont les produits les plus vendus ?
- Quelles catégories génèrent le plus de chiffre d’affaires ?
- Quels vendeurs sont les plus performants ?
- Quels clients achètent le plus ?

### Analyses temporelles
- Ventes par jour, mois, trimestre, année
- Saisonnalité des ventes

### Analyses logistiques
- Retards de livraison
- Écarts entre dates estimées et dates réelles
- Performances des vendeurs par délais

### Analyses financières
- Montant du fret
- Répartition des types de paiements
- Conversion en euro (optionnel)

---

# 9. Prochaine étape

Avec ce document, les éléments suivants sont prêts :

- grain ✔️  
- mesures ✔️  
- FK vers dimensions ✔️  
- attributs dégénérés ✔️  

La prochaine étape est :

**Créer le schéma en étoile (`schema_etoile.drawio`)**  
pour visualiser clairement toutes les relations.

