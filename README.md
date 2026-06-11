# Building Energy Efficiency Analytics

> Framework Python d'analyse de la performance énergétique d'un parc de 20 bâtiments : calcul d'IPE, détection d'énergivores, modélisation des leviers et quantification du ROI des rénovations.
> **Stack :** Python · pandas · scikit-learn · matplotlib · seaborn

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Portfolio](https://img.shields.io/badge/Portfolio-TSAGUE%20Emmanuel-purple)](https://github.com/TSAGUE25)

---

## Table des matières

1. [Contexte métier](#1-contexte-métier)
2. [Problème résolu](#2-problème-résolu)
3. [Données utilisées](#3-données-utilisées)
4. [Méthodes et algorithmes](#4-méthodes-et-algorithmes)
5. [Démarche analytique](#5-démarche-analytique)
6. [Métriques clés](#6-métriques-clés)
7. [Résultats obtenus](#7-résultats-obtenus)
8. [Valeur métier](#8-valeur-métier)
9. [Architecture du projet](#9-architecture-du-projet)
10. [Installation et usage](#10-installation-et-usage)
11. [Compétences démontrées](#11-compétences-démontrées)
12. [Limites et améliorations](#12-limites-et-améliorations)
13. [Contributors](#13-contributors)

---

## 1. Contexte métier

Les bâtiments représentent **40% de la consommation énergétique finale** en France et constituent le premier gisement d'économies d'énergie identifié par les plans nationaux de rénovation.

Un gestionnaire de parc immobilier ou un énergéticien (collectivité, foncière, industriel) doit :
- Connaître la performance réelle de chaque bâtiment (kWh/m²/an)
- Identifier les bâtiments les plus énergivores parmi des dizaines ou centaines de sites
- Comprendre les causes (ancienneté, isolation, type de chauffage, climat)
- Prioriser les investissements de rénovation selon le ROI énergétique

Ce projet simule ce cas d'usage sur un parc fictif de **20 bâtiments** sur **3 années** (2021–2023), couvrant des typologies variées : bureaux, logements, écoles, hôtels, entrepôts, commerces, hôpitaux, équipements sportifs.

---

## 2. Problème résolu

> *"Sur notre parc, nous payons chaque mois des factures d'énergie sans savoir quels sites consomment anormalement, ni pourquoi. Comment identifier les priorités d'intervention et estimer le gain financier d'une rénovation ?"*

Ce projet apporte :
- **Calcul automatique de l'IPE** (kWh/m²/an) — métrique universelle et réglementaire
- **Détection statistique des énergivores** sans seuil arbitraire (méthode IQR)
- **Modèle explicatif** des déterminants de la consommation (régression linéaire, R²=0.71)
- **Quantification du potentiel d'économie** en MWh et en euros par bâtiment

| Objectif | Méthode |
|----------|---------|
| Calculer l'IPE annuel par bâtiment | Agrégation pandas + normalisation surface |
| Détecter les énergivores | Méthode IQR (Q3 + 1.5×IQR) |
| Segmenter le parc par DPE / usage | Groupby + statistiques descriptives |
| Modéliser les leviers de consommation | Régression linéaire (sklearn) |
| Quantifier le potentiel d'économie | Écart à la médiane × surface × tarif |
| Analyser l'impact des rénovations | Comparaison avant/après IPE |

---

## 3. Données utilisées

> **Données entièrement simulées — aucune donnée réelle ou confidentielle.**

### `buildings_characteristics.csv` — 20 bâtiments

| Colonne | Description | Exemple |
|---------|-------------|---------|
| `id_batiment` | Identifiant unique | B001 |
| `type_usage` | Catégorie | Bureau, École, Hôtel... |
| `surface_m2` | Surface totale | 8 500 m² |
| `annee_construction` | Millésime | 1978 |
| `etiquette_dpe` | Classe DPE | A à G |
| `type_chauffage` | Énergie chauffage | Gaz, Fioul, PAC... |
| `isolation` | Qualité enveloppe | Bonne / Moyenne / Mauvaise |

![Répartition du parc par étiquette DPE](figures/fig7_repartition_dpe.png)

### `energy_consumption_monthly.csv` — 720 lignes (20 bâtiments × 3 ans × 12 mois)

| Colonne | Description |
|---------|-------------|
| `consommation_elec_kwh` | Électricité mensuelle (kWh) |
| `consommation_gaz_kwh` | Gaz mensuel (kWh) |
| `consommation_totale_kwh` | Total (élec + gaz) |
| `dju_chauffage` | DJU mensuel (base 18°C) |

### `meteo_sample.csv` — 6 villes × 36 mois

Température min/moy/max, DJU, précipitations, ensoleillement pour Paris, Lyon, Bordeaux, Rennes, Nice, Grenoble.

---

## 4. Méthodes et algorithmes

| Méthode | Bibliothèque | Application |
|---------|-------------|-------------|
| Calcul IPE | pandas | Normalisation kWh/m²/an |
| Détection IQR | numpy | Identification énergivores (Q3 + 1.5×IQR) |
| Régression linéaire | scikit-learn | Modélisation des leviers (ancienneté, DJU, isolation) |
| Label Encoding | scikit-learn | Variables catégorielles |
| Corrélation de Pearson | pandas | Relation conso / DJU |
| Normalisation DJU | numpy | Correction biais climatique |

**Choix IQR vs z-score :** l'IQR est robuste aux valeurs extrêmes et ne suppose pas de distribution normale — adapté à un parc hétérogène (entrepôt vs crèche).

---

## 5. Démarche analytique

```
Données brutes (3 CSV — 20 bâtiments, 3 ans)
        │
        ▼
   Contrôle qualité (cohérence total = élec + gaz, anomalies gaz/PAC)
        │
        ▼
  Calcul IPE annuel (kWh/m²/an + normalisation DJU)
        │
        ├──→ Segmentation (DPE × type usage)
        ├──→ Détection énergivores (IQR)
        ├──→ Corrélation température / conso
        ├──→ Régression linéaire (R², coefficients)
        ├──→ Analyse avant/après rénovation
        └──→ Potentiel d'économie (MWh + €)
                │
                ▼
        Rapport Markdown + 8 figures
```

---

## 6. Métriques clés

| Métrique | Formule | Unité |
|----------|---------|-------|
| **IPE** | Σ conso_annuelle / surface | kWh/m²/an |
| **IPE normalisé** | IPE × (DJU_réf / DJU_réel) | kWh/m²/an |
| **Borne IQR** | Q3 + 1.5 × (Q3 − Q1) | kWh/m²/an |
| **R² régression** | Variance expliquée | 0–1 |
| **Gain rénovation** | (IPE_avant − IPE_après) / IPE_avant | % |
| **Économie potentielle** | Écart_cible × surface × tarif | MWh/an, €/an |

**DJU — pourquoi normaliser ?** Sans correction, un bâtiment à Lille (2 800 DJU/an) semble 30% moins performant qu'un bâtiment identique à Nice (1 800 DJU/an) — uniquement à cause du climat. La normalisation élimine ce biais.

---

## 7. Résultats obtenus

| Résultat | Valeur |
|---------|--------|
| IPE moyen du parc | **~218 kWh/m²/an** (classe D) |
| Meilleur bâtiment | **B011** — Siège Nexia (87 kWh/m²/an · DPE A · PAC · 2018) |
| Bâtiment le plus énergivore | **B006** — Gymnase (432 kWh/m²/an · DPE G · fioul · 1975) |
| Bâtiments énergivores détectés (IQR) | **4 bâtiments** |
| R² du modèle de régression | **0.71** |
| Gain moyen des rénovations | **~19%** d'IPE (B002, B010, B016) |
| Économie potentielle totale | **~1.4 GWh/an** (~168 000 €/an) |

**Déterminants principaux :**
1. **Ancienneté** : +1 an ≈ +2 kWh/m²/an
2. **Climat (DJU)** : +100 DJU ≈ +8 kWh/m²/an
3. **Isolation "Mauvaise" vs "Bonne"** : écart de 80–120 kWh/m²/an

**Exemple de ROI simulé :** un bâtiment de 8 500 m² avec IPE = 295 qui atteindrait la médiane (195) économiserait `(295 − 195) × 8 500 × 0.12 = **102 000 €/an**`.

### Visualisations

![IPE par étiquette DPE](figures/fig1_ipe_par_dpe.png)
![IPE par type d'usage](figures/fig2_ipe_par_type_usage.png)
![Évolution temporelle](figures/fig3_evolution_temporelle.png)
![Consommation vs DJU](figures/fig4_conso_vs_dju.png)
![Heatmap IPE](figures/fig5_heatmap_ipe.png)
![Potentiel d'économie](figures/fig6_potentiel_economies.png)
![Impact rénovations](figures/fig8_impact_renovation.png)

---

## 8. Valeur métier

### Pour un gestionnaire de parc immobilier
- **Priorisation immédiate** : identifier en 5 minutes quels bâtiments auditer en urgence
- **Budget rénovation objectivé** : ROI estimé en €/an avant tout engagement
- **Suivi de performance** : mesurer l'effet réel d'une rénovation sur l'IPE

### Pour un énergéticien / DSI
- **Pipeline automatisable** : le script tourne sur n'importe quel parc en changeant le CSV
- **Connexion Power BI** : les mêmes données alimentent le dashboard de pilotage
- **Base de reporting réglementaire** : DPE, BACS, décret tertiaire

**Adapté pour :** EDF, gestionnaires d'actifs immobiliers, collectivités, bureaux d'études énergie, utilities.

---

## 9. Architecture du projet

```
building-energy-efficiency-analytics/
│
├── data_sample/
│   ├── buildings_characteristics.csv    # 20 bâtiments, 13 attributs
│   ├── energy_consumption_monthly.csv   # 720 lignes (20 × 3 ans × 12 mois)
│   ├── meteo_sample.csv                 # 216 lignes (6 villes × 36 mois)
│   └── schema_reference.md
│
├── src/
│   ├── __init__.py
│   ├── energy_analyzer.py              # Classe EnergyAnalyzer (8 méthodes)
│   └── visualization.py               # Classe EnergyVisualizer (8 figures)
│
├── notebooks/
│   └── 01_energy_efficiency_analysis.py  # Pipeline complet (10 sections)
│
├── figures/                            # 8 visualisations générées
├── reports/
│   └── energy_audit_report_sample.md
│
├── docs/
│   ├── dictionnaire_donnees.md
│   ├── methodologie.md
│   └── guide_utilisateur.md
│
├── dashboard/
│   └── README.md                       # Modèle DAX Power BI
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## 10. Installation et usage

```bash
git clone https://github.com/TSAGUE25/building-energy-efficiency-analytics
cd building-energy-efficiency-analytics
pip install -r requirements.txt
python notebooks/01_energy_efficiency_analysis.py
```

**Utilisation directe des classes :**

```python
import pandas as pd
from src.energy_analyzer import EnergyAnalyzer
from src.visualization import EnergyVisualizer

buildings   = pd.read_csv('data_sample/buildings_characteristics.csv')
consumption = pd.read_csv('data_sample/energy_consumption_monthly.csv')

analyzer = EnergyAnalyzer(buildings, consumption)
annual   = analyzer.compute_annual_ipe()

print(analyzer.detect_high_consumers())   # Bâtiments énergivores
print(analyzer.savings_potential())       # Potentiel en €/an
reg = analyzer.run_regression()
print(f"R² = {reg['r2']:.3f}")

viz = EnergyVisualizer(output_dir='figures')
viz.plot_ipe_by_dpe(annual)
viz.plot_savings_potential(analyzer.savings_potential())
```

**Sorties produites :**
- `figures/` — 8 visualisations PNG
- `reports/energy_audit_report_sample.md` — rapport Markdown auto-généré

---

## 11. Compétences démontrées

| Compétence | Mise en œuvre | Fichier |
|-----------|--------------|---------|
| **Python OOP** | Classes `EnergyAnalyzer`, `EnergyVisualizer` | `src/` |
| **Calcul IPE** | Méthode `compute_annual_ipe()` + normalisation DJU | `src/energy_analyzer.py` |
| **Détection IQR** | Méthode `detect_high_consumers()` | `src/energy_analyzer.py` |
| **Régression sklearn** | `run_regression()` — R²=0.71, MAE ~28 kWh/m²/an | `src/energy_analyzer.py` |
| **ROI rénovation** | `savings_potential()` + `renovation_impact()` | `src/energy_analyzer.py` |
| **Visualisation avancée** | 8 figures : boxplot, heatmap, barh, scatter | `src/visualization.py` |
| **Reporting automatisé** | Génération Markdown programmatique | `notebooks/` |
| **Domaine énergie** | IPE, DPE, DJU, kWh/m²/an, décret tertiaire | `docs/` + README |

**Stack technique :** `pandas` · `numpy` · `scikit-learn` (LinearRegression, LabelEncoder) · `matplotlib` · `seaborn`

---

## 12. Limites et améliorations

**Limites actuelles :**

| Limite | Impact |
|--------|--------|
| Données simulées | Pas de validation terrain |
| Modèle linéaire | Interactions non capturées |
| 20 bâtiments | Faible puissance statistique |
| Tarif unique 0,12 €/kWh | Approximation des coûts réels |

**Pistes d'amélioration :**
- **Random Forest / XGBoost** : capturer les interactions non linéaires (ancienneté × isolation)
- **Clustering K-means** : regrouper les bâtiments par profil de consommation
- **API Enedis / GrDF** : connexion aux données réelles de consommation
- **GitHub Actions** : automatisation mensuelle du pipeline + alertes IPE
- **Analyse CO2** : intégration des facteurs d'émission par vecteur énergétique

---

## Ce projet démontre

- La capacité à appliquer une **méthodologie d'audit énergétique** complète : calcul IPE, normalisation DJU, détection IQR, sans seuil arbitraire
- La maîtrise de **scikit-learn** dans un contexte métier réglementé (DPE, décret tertiaire) : régression linéaire, LabelEncoder, R²=0.71
- La **quantification du ROI** d'une rénovation en MWh/an et €/an — directement exploitable pour un plan d'investissement
- La détection robuste d'**énergivores via la méthode IQR** : insensible aux distributions asymétriques, applicable sur parc hétérogène
- Un pipeline **automatisable** : changer le CSV suffit pour auditer tout nouveau parc (collectivité, foncière, industriel)
- La **traduction de données techniques** (kWh, DJU, étiquette DPE) en décision de gestion d'actifs immobiliers

---

## 13. Contributors

| Nom | Rôle | GitHub |
|-----|------|--------|
| **TSAGUE Emmanuel** | Data Scientist — auteur principal | [@TSAGUE25](https://github.com/TSAGUE25) |

---

*Auteur : Emmanuel TSAGUE — Data Scientist / Data Analyst*
*Formation : DataScientest | Domaines : Énergie · Industrie · Finance · Performance opérationnelle*
*Contact : emmatsague@yahoo.fr | [LinkedIn](https://www.linkedin.com/in/emmanuel-tsague-114295414)*
*Données : entièrement simulées — aucune donnée réelle ou confidentielle*
