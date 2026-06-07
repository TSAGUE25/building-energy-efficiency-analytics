# Méthodologie — Building Energy Efficiency Analytics

## 1. Calcul de l'IPE

L'Indicateur de Performance Énergétique est calculé en deux étapes :

**Étape 1 — Agrégation annuelle :**
```
conso_annuelle_kwh = Σ consommation_totale_kwh (12 mois)
```

**Étape 2 — Normalisation par surface :**
```
IPE = conso_annuelle_kwh / surface_m2
```

**Étape 3 (optionnelle) — Normalisation climatique DJU :**
```
IPE_normalisé = IPE × (DJU_référence / DJU_réel)
```
Cette étape permet de comparer des bâtiments dans des villes avec des hivers différents (Paris vs Nice).

---

## 2. Détection des énergivores par IQR

La méthode IQR (Interquartile Range) est robuste aux distributions non normales :

```
Q1 = 25e percentile des IPE du parc
Q3 = 75e percentile des IPE du parc
IQR = Q3 - Q1
Borne haute = Q3 + 1.5 × IQR

Énergivore si IPE > Borne haute
```

Avantage vs moyenne+2σ : insensible aux valeurs extrêmes, pas d'hypothèse de normalité.

---

## 3. Régression linéaire

**Variable cible :** IPE (kWh/m²/an)  
**Variables explicatives :**
- `surface_m2` — taille du bâtiment
- `ancienneté` = année_analyse - année_construction
- `dju_annuel` — climat local (chauffage)
- `type_usage` — encodé LabelEncoder (Bureau=0, Commerce=1, …)
- `isolation` — encodé LabelEncoder (Bonne=0, Mauvaise=1, Moyenne=2)

**Limites du modèle linéaire :**
- Suppose une relation linéaire entre variables
- Ne capture pas les interactions (ex. bâtiment ancien + bonne isolation)
- Améliorations possibles : Random Forest, XGBoost, features polynomiales

---

## 4. Analyse d'impact des rénovations

Pour les bâtiments ayant `renovation_realisee = 1` :
- **Avant** = moyenne IPE des années < `annee_renovation`
- **Après** = moyenne IPE des années ≥ `annee_renovation`
- **Gain (%)** = (IPE_avant - IPE_après) / IPE_avant × 100

Limite : avec seulement 3 ans de données (2021–2023), certains bâtiments n'ont que des données "après" rénovation.

---

## 5. Calcul du potentiel d'économie

```
Écart à la cible = max(0, IPE_moyen - IPE_cible)
Économie (kWh/an) = Écart × surface_m2
Économie (€/an) = Économie_kWh × 0.12 €/kWh
```

Le tarif de 0,12 €/kWh est une approximation mixte (gaz + électricité). À ajuster selon les contrats réels.
