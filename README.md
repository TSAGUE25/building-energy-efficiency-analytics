# Building Energy Efficiency Analytics

> Analyse de l'efficacité énergétique d'un parc de 20 bâtiments pour identifier les leviers de réduction de consommation.  
> **Stack :** Python · pandas · scikit-learn · matplotlib · seaborn · Power BI

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Portfolio](https://img.shields.io/badge/Portfolio-Data%20Science-orange)](https://github.com/TSAGUE25)

---

## Table des matières

1. [Titre et accroche](#1-titre-et-accroche)
2. [Contexte métier](#2-contexte-métier)
3. [Pourquoi ce projet existe](#3-pourquoi-ce-projet-existe)
4. [Problème métier](#4-problème-métier)
5. [Objectifs](#5-objectifs)
6. [Données utilisées](#6-données-utilisées)
7. [Préparation des données](#7-préparation-des-données)
8. [Méthodes et algorithmes](#8-méthodes-et-algorithmes)
9. [Démarche analytique](#9-démarche-analytique)
10. [Métriques clés](#10-métriques-clés)
11. [Explication des métriques](#11-explication-des-métriques)
12. [Résultats obtenus](#12-résultats-obtenus)
13. [Valeur métier](#13-valeur-métier)
14. [Limites du projet](#14-limites-du-projet)
15. [Améliorations possibles](#15-améliorations-possibles)
16. [Architecture du dépôt](#16-architecture-du-dépôt)
17. [README technique](#17-readme-technique)
18. [Version CV](#18-version-cv)
19. [Version entretien](#19-version-entretien)
20. [Version portfolio](#20-version-portfolio)
21. [Post LinkedIn](#21-post-linkedin)
22. [Questions d'entretien](#22-questions-dentretien)
23. [Compétences démontrées](#23-compétences-démontrées)
24. [Tableau compétences / preuves](#24-tableau-compétences--preuves)
25. [Conseils GitHub](#25-conseils-github)

---

## 1. Titre et accroche

**Building Energy Efficiency Analytics** — Un framework Python d'analyse de la performance énergétique des bâtiments, calculant les IPE (kWh/m²/an), détectant les énergivores par méthode IQR, modélisant les leviers par régression et quantifiant le potentiel d'économie du parc.

> *Ce projet démontre la capacité à transformer des données de consommation brutes en recommandations d'action à impact financier mesurable.*

---

## 2. Contexte métier

Les bâtiments représentent **40% de la consommation énergétique finale** en France et constituent le premier gisement d'économies d'énergie identifié par les plans nationaux de rénovation.

Un gestionnaire de parc immobilier ou un énergéticien (collectivité, foncière, industriel) doit :
- Connaître la performance réelle de chaque bâtiment (kWh/m²/an)
- Identifier les bâtiments les plus énergivores parmi des dizaines ou centaines de sites
- Comprendre les causes (ancienneté, isolation, type de chauffage, climat)
- Prioriser les investissements de rénovation selon le ROI énergétique

Ce projet simule ce cas d'usage sur un parc fictif de **20 bâtiments** sur **3 années** (2021–2023), couvrant des typologies variées : bureaux, logements, écoles, hôtels, entrepôts, commerces, hôpitaux, équipements sportifs.

---

## 3. Pourquoi ce projet existe

**Problème concret :** Un gestionnaire de parc reçoit des factures d'énergie mensuelles par bâtiment. Sans normalisation par la surface et sans correction climatique, il est impossible de comparer un entrepôt de 18 000 m² à Lille avec une crèche de 650 m² à Montpellier.

**Ce que ce projet apporte :**
- Calcul automatique de l'IPE (kWh/m²/an) — métrique universelle et réglementaire
- Détection statistique des énergivores sans seuil arbitraire (IQR)
- Modèle explicatif des déterminants de la consommation (régression)
- Quantification du potentiel d'économie en MWh et en euros

---

## 4. Problème métier

> *"Sur notre parc de bâtiments, nous payons chaque mois des factures d'énergie sans savoir quels sites consomment anormalement, ni pourquoi. Comment identifier les priorités d'intervention et estimer le gain financier d'une rénovation ?"*

**Traduction analytique :**
- Calculer et normaliser l'IPE de chaque bâtiment chaque année
- Détecter les outliers (énergivores) de façon objective et reproductible
- Modéliser la part expliquée par l'ancienneté, le climat, l'isolation
- Produire un classement par potentiel d'économie avec estimation ROI

---

## 5. Objectifs

| # | Objectif | Méthode |
|---|----------|---------|
| 1 | Calculer l'IPE annuel de chaque bâtiment | Agrégation pandas + normalisation surface |
| 2 | Détecter les bâtiments énergivores | Méthode IQR (Q3 + 1.5×IQR) |
| 3 | Segmenter le parc par DPE et type d'usage | Groupby + statistiques descriptives |
| 4 | Modéliser les leviers de consommation | Régression linéaire (sklearn) |
| 5 | Quantifier le potentiel d'économie | Calcul écart à la médiane × surface × tarif |
| 6 | Analyser l'impact des rénovations | Comparaison avant/après sur IPE |
| 7 | Visualiser les résultats | 8 figures matplotlib/seaborn |
| 8 | Produire un rapport automatique | Markdown généré par script |

---

## 6. Données utilisées

> **Données entièrement simulées — aucune donnée réelle ou confidentielle.**

### 6.1 buildings_characteristics.csv

20 bâtiments fictifs avec les attributs suivants :

| Colonne | Description | Exemple |
|---------|-------------|---------|
| `id_batiment` | Identifiant unique | B001 |
| `nom_batiment` | Nom fictif | Tour Centrale |
| `type_usage` | Catégorie | Bureau, École, Hôtel... |
| `ville` / `region` | Localisation | Paris, Ile-de-France |
| `surface_m2` | Surface totale | 8 500 m² |
| `annee_construction` | Millésime | 1978 |
| `etiquette_dpe` | Classe DPE | A à G |
| `type_chauffage` | Énergie chauffage | Gaz, Fioul, PAC... |
| `isolation` | Qualité enveloppe | Bonne / Moyenne / Mauvaise |
| `renovation_realisee` | Flag rénovation | 0 / 1 |

![Répartition du parc par étiquette DPE](figures/fig7_repartition_dpe.png)

### 6.2 energy_consumption_monthly.csv

720 lignes — 20 bâtiments × 3 années × 12 mois :

| Colonne | Description |
|---------|-------------|
| `consommation_elec_kwh` | Électricité mensuelle (kWh) |
| `consommation_gaz_kwh` | Gaz mensuel (kWh) |
| `consommation_totale_kwh` | Total (élec + gaz) |
| `dju_chauffage` | DJU mensuel (base 18°C) |

### 6.3 meteo_sample.csv

Données météo mensuelles pour 6 villes (Paris, Lyon, Bordeaux, Rennes, Nice, Grenoble) : température min/moy/max, DJU, précipitations, ensoleillement.

---

## 7. Préparation des données

### 7.1 Contrôles qualité effectués

```python
# Vérification cohérence : total = élec + gaz
consumption['check'] = (
    consumption['consommation_totale_kwh'] ==
    consumption['consommation_elec_kwh'] + consumption['consommation_gaz_kwh']
)

# Détection anomalie : gaz > 0 pour bâtiments élec/PAC
elec_bat = buildings[buildings['type_chauffage'].isin(['Électrique', 'Pompe à chaleur'])]
anomalies = consumption[
    consumption['id_batiment'].isin(elec_bat['id_batiment']) &
    (consumption['consommation_gaz_kwh'] > 0)
]
```

### 7.2 Variables dérivées

```python
# IPE annuel (kWh/m²/an)
annual['ipe_kwh_m2'] = annual['conso_totale_kwh'] / annual['surface_m2']

# IPE normalisé climatiquement
annual['ipe_normalise'] = annual['ipe_kwh_m2'] * (DJU_REF / annual['dju_annuel'])

# Ancienneté
df['anciennete'] = df['annee'] - df['annee_construction']
```

---

## 8. Méthodes et algorithmes

| Méthode | Bibliothèque | Application |
|---------|-------------|-------------|
| Calcul IPE | pandas | Normalisation kWh/m²/an |
| Détection IQR | numpy | Identification énergivores |
| Régression linéaire | scikit-learn | Modélisation des leviers |
| Label Encoding | scikit-learn | Variables catégorielles |
| Corrélation de Pearson | pandas | Relation conso / DJU |
| Agrégation temporelle | pandas | Tendances 2021–2023 |
| Boxplot / Heatmap | matplotlib / seaborn | Visualisation distribution IPE |

---

## 9. Démarche analytique

```
Données brutes (3 CSV)
        │
        ▼
   Contrôle qualité
   (cohérence, anomalies)
        │
        ▼
  Calcul IPE annuel
  (kWh/m²/an + normalisation DJU)
        │
        ├──→ Segmentation (DPE × type usage)
        │
        ├──→ Détection énergivores (IQR)
        │
        ├──→ Corrélation température / conso
        │
        ├──→ Régression linéaire (R², coefficients)
        │
        ├──→ Analyse avant/après rénovation
        │
        └──→ Potentiel d'économie (MWh + €)
                │
                ▼
        Rapport Markdown + 8 figures
```

---

## 10. Métriques clés

| Métrique | Formule | Unité |
|----------|---------|-------|
| **IPE** | Σ conso_annuelle / surface | kWh/m²/an |
| **IPE normalisé** | IPE × (DJU_réf / DJU_réel) | kWh/m²/an |
| **Borne IQR** | Q3 + 1.5 × (Q3 − Q1) | kWh/m²/an |
| **R² régression** | Variance expliquée | 0–1 |
| **MAE** | Erreur absolue moyenne | kWh/m²/an |
| **Gain rénovation** | (IPE_avant − IPE_après) / IPE_avant | % |
| **Économie potentielle** | Écart_cible × surface × tarif | MWh/an, €/an |

---

## 11. Explication des métriques

### IPE (Indicateur de Performance Énergétique)

L'IPE est la métrique centrale de ce projet. En divisant la consommation totale annuelle par la surface, on obtient une valeur comparable entre bâtiments de tailles différentes. Les seuils réglementaires DPE français (décret 2021) définissent les classes A (< 50) à G (>= 450 kWh/m²/an).

### DJU (Degrés Jours Unifiés)

Sans correction climatique, un bâtiment à Lille (hiver rude) semble moins performant qu'un bâtiment identique à Nice — alors que c'est simplement l'effet du climat. La normalisation par DJU corrige ce biais : `IPE_normalisé = IPE × (2400 / DJU_réel)`.

### Méthode IQR

Plus robuste que la règle "moyenne ± 2 écarts-types", l'IQR ne suppose pas de distribution normale et résiste aux valeurs extrêmes. Un bâtiment est qualifié d'énergivore si son IPE dépasse Q3 + 1.5 × (Q3 − Q1), soit environ le top 7% d'une distribution normale.

### R² de la régression

Un R² = 0.71 signifie que 71% de la variabilité de l'IPE entre bâtiments est expliquée par les 5 variables retenues (ancienneté, DJU, surface, type, isolation). Les 29% restants correspondent à des facteurs non capturés : comportement des occupants, équipements intérieurs, maintenance.

---

## 12. Résultats obtenus

### Sur le parc simulé (20 bâtiments, 2021–2023)

| Résultat | Valeur |
|---------|--------|
| IPE moyen du parc | **~218 kWh/m²/an** (classe D) |
| Meilleur bâtiment | **B011** — Siège Nexia (87 kWh/m²/an, DPE A, PAC, 2018) |
| Bâtiment le plus énergivore | **B006** — Gymnase (432 kWh/m²/an, DPE G, fioul, 1975) |
| Bâtiments énergivores (IQR) | **4 bâtiments** |
| R² du modèle de régression | **0.71** |
| Gain moyen des rénovations | **~19%** d'IPE (B002, B010, B016) |
| Économie potentielle totale | **~1.4 GWh/an** (~168 000 €/an) |

### Déterminants principaux identifiés

1. **Ancienneté** : +1 an = environ +2 kWh/m²/an (normes thermiques plus strictes depuis 2000)
2. **Climat (DJU)** : +100 DJU = +8 kWh/m²/an (zone climatique déterminante pour le chauffage)
3. **Isolation "Mauvaise"** vs "Bonne" : écart de 80–120 kWh/m²/an observé en moyenne

### Visualisations des résultats

**Distribution IPE par classe DPE (boxplot) :**

![IPE par étiquette DPE](figures/fig1_ipe_par_dpe.png)

**IPE moyen par type d'usage :**

![IPE par type d'usage](figures/fig2_ipe_par_type_usage.png)

**Évolution de la consommation et de l'IPE moyen (2021–2023) :**

![Évolution temporelle](figures/fig3_evolution_temporelle.png)

**Corrélation consommation mensuelle / DJU par type de chauffage :**

![Consommation vs DJU](figures/fig4_conso_vs_dju.png)

**Heatmap IPE bâtiment × année (kWh/m²/an) :**

![Heatmap IPE](figures/fig5_heatmap_ipe.png)

**Top 10 bâtiments — Potentiel d'économie annuelle :**

![Potentiel d'économie](figures/fig6_potentiel_economies.png)

**Impact des rénovations thermiques (avant / après) :**

![Impact rénovations](figures/fig8_impact_renovation.png)

---

## 13. Valeur métier

### Pour un gestionnaire de parc immobilier
- **Priorisation immédiate** : identifier en 5 minutes quels bâtiments auditer en urgence
- **Budget rénovation objectivé** : ROI estimé en €/an avant engagement
- **Suivi de performance** : constater l'effet réel d'une rénovation sur l'IPE

### Pour un énergéticien / DSI
- **Pipeline automatisable** : le script tourne sur n'importe quel parc en changeant le CSV
- **Connexion Power BI** : les mêmes données alimentent le dashboard de pilotage
- **Base de reporting** réglementaire (DPE, BACS, décret tertiaire)

### Exemple de ROI simulé
Un bâtiment de 8 500 m² avec IPE = 295 kWh/m²/an qui atteindrait la médiane (195) économiserait :  
`(295 - 195) × 8 500 × 0,12 €/kWh = **102 000 €/an**`

---

## 14. Limites du projet

| Limite | Impact | Mitigation |
|--------|--------|-----------|
| Données simulées | Pas de validation terrain | Données réelles via API compteurs |
| Modèle linéaire | Interactions non capturées | Passer à Random Forest / XGBoost |
| 3 ans seulement | Tendances peu robustes | Étendre à 5–10 ans |
| 20 bâtiments | Faible puissance statistique | Déployer sur 200+ sites |
| Tarif unique 0,12 €/kWh | Approximation | Intégrer les vrais contrats d'énergie |
| Pas de CO2 | Bilan carbone absent | Ajouter facteur d'émission (kgCO2/kWh) |

---

## 15. Améliorations possibles

- **Machine Learning avancé** : Random Forest pour capturer les interactions non linéaires
- **Clustering** : K-means pour regrouper les bâtiments par profil de consommation
- **Time Series** : Prophet ou LSTM pour prévision de consommation à 12 mois
- **Données réelles** : connexion API Enedis (électricité) ou GrDF (gaz)
- **Tableau de bord temps réel** : mise à jour mensuelle automatique via GitHub Actions
- **Analyse CO2** : intégration des facteurs d'émission par vecteur énergétique
- **Benchmarking sectoriel** : comparaison aux référentiels ADEME par type de bâtiment

---

## 16. Architecture du dépôt

```
building-energy-efficiency-analytics/
│
├── data_sample/
│   ├── buildings_characteristics.csv    # 20 bâtiments, 13 attributs
│   ├── energy_consumption_monthly.csv   # 720 lignes (20 × 3 ans × 12 mois)
│   ├── meteo_sample.csv                 # 216 lignes (6 villes × 36 mois)
│   └── schema_reference.md             # Dictionnaire + règles métier
│
├── src/
│   ├── __init__.py
│   ├── energy_analyzer.py              # Classe EnergyAnalyzer (8 méthodes)
│   └── visualization.py               # Classe EnergyVisualizer (8 figures)
│
├── notebooks/
│   └── 01_energy_efficiency_analysis.py  # Script complet (10 sections)
│
├── figures/                            # 8 visualisations générées
├── reports/
│   └── energy_audit_report_sample.md   # Rapport de synthèse
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

## 17. README technique

### Installation

```bash
git clone https://github.com/TSAGUE25/building-energy-efficiency-analytics
cd building-energy-efficiency-analytics
pip install -r requirements.txt
```

### Exécution

```bash
python notebooks/01_energy_efficiency_analysis.py
```

### Utilisation directe des classes

```python
import pandas as pd
from src.energy_analyzer import EnergyAnalyzer
from src.visualization import EnergyVisualizer

buildings = pd.read_csv('data_sample/buildings_characteristics.csv')
consumption = pd.read_csv('data_sample/energy_consumption_monthly.csv')

analyzer = EnergyAnalyzer(buildings, consumption)
annual = analyzer.compute_annual_ipe()

print(analyzer.detect_high_consumers())    # Bâtiments énergivores
print(analyzer.savings_potential())        # Potentiel en €/an
reg = analyzer.run_regression()
print(f"R² = {reg['r2']:.3f}")

viz = EnergyVisualizer(output_dir='figures')
viz.plot_ipe_by_dpe(annual)
viz.plot_savings_potential(analyzer.savings_potential())
```

### Dépendances

| Package | Version | Usage |
|---------|---------|-------|
| pandas | >= 1.5 | Manipulation des données |
| numpy | >= 1.23 | Calculs statistiques |
| matplotlib | >= 3.6 | Visualisations |
| seaborn | >= 0.12 | Heatmap, styles |
| scikit-learn | >= 1.2 | Régression, LabelEncoder |

---

## 18. Version CV

> *À copier dans la section "Projets" du CV*

**Building Energy Efficiency Analytics** | Python, scikit-learn, pandas, matplotlib  
Framework d'analyse de la performance énergétique d'un parc de 20 bâtiments.  
Calcul d'IPE (kWh/m²/an), détection d'énergivores par IQR, régression linéaire (R²=0.71), quantification de 1,4 GWh/an d'économies potentielles (~168 000 €/an). Architecture OOP (classes `EnergyAnalyzer`, `EnergyVisualizer`), rapport Markdown automatisé, 8 visualisations.

---

## 19. Version entretien

*Question : "Parlez-moi d'un projet Data Science que vous avez réalisé."*

> "J'ai développé un framework Python d'analyse énergétique pour un parc de bâtiments fictif — qui reproduit exactement les cas d'usage d'un gestionnaire immobilier ou d'un énergéticien.
>
> Le problème de départ : des données de consommation mensuelle brutes. Sans normaliser par la surface et corriger l'effet climatique via les DJU, on ne peut pas comparer un entrepôt de Lille à une crèche de Montpellier.
>
> J'ai calculé l'IPE (kWh/m²/an) pour chaque bâtiment, utilisé la méthode IQR — plus robuste que la moyenne ± 2σ — pour détecter les énergivores, puis une régression linéaire pour identifier les déterminants : l'ancienneté et le DJU expliquent 71% de la variance d'IPE.
>
> Le résultat concret : 4 bâtiments énergivores identifiés, 1,4 GWh/an d'économies potentielles soit ~168 000 €/an. Rapport généré automatiquement en Markdown à chaque run.
>
> Ce qui m'a le plus appris : la valeur de la normalisation. Sans elle, tous les comparatifs sont trompeurs."

---

## 20. Version portfolio

Ce projet illustre la capacité à conduire une **analyse exploratoire structurée** sur des données énergétiques : de l'ingestion CSV jusqu'au rapport d'audit, en passant par la modélisation statistique et la visualisation professionnelle.

**Ce qu'il démontre :**
- Pipeline data complet (ingestion → nettoyage → analyse → visualisation → rapport)
- Rigueur dans la définition des métriques métier (IPE, DJU, IQR)
- Choix de méthodes adaptées (IQR vs zscore, régression interprétable vs black box)
- Code structuré en classes réutilisables, documenté, publiable

**Adapté pour :** EDF, gestionnaires d'actifs immobiliers, collectivités, bureaux d'études énergie, utilities.

---

## 21. Post LinkedIn

> **J'ai construit un framework Python d'audit énergétique bâtiment — voici ce que j'ai appris**
>
> Dans le monde de l'énergie, une question revient constamment : *"Lesquels de nos bâtiments consomment trop, et pourquoi ?"*
>
> Pour répondre rigoureusement, j'ai développé un outil Python qui :
>
> Calcule l'**IPE** (kWh/m²/an) pour chaque bâtiment  
> Détecte les **énergivores** par méthode IQR sans seuil arbitraire  
> Modélise les **leviers** : ancienneté, DJU, isolation, type d'usage (R²=0.71)  
> Quantifie le **potentiel d'économie** en MWh/an et en €/an  
> Génère un **rapport Markdown** automatiquement à chaque run
>
> Sur le parc simulé (20 bâtiments, 3 ans) : 4 énergivores identifiés, 1,4 GWh/an d'économies potentielles — soit ~168 000 €/an.
>
> La leçon clé : sans normalisation par la surface et correction climatique (DJU), tous les comparatifs sont trompeurs. Un bâtiment de Strasbourg sera toujours défavorisé vs son équivalent niçois si on regarde les kWh bruts.
>
> Code disponible sur GitHub  
> #DataScience #EfficaciteEnergetique #Python #BuildingAnalytics #EDF #Portfolio

---

## 22. Questions d'entretien

**Q1 : Pourquoi l'IQR plutôt que moyenne ± 2σ pour détecter les énergivores ?**  
L'IQR est robuste aux valeurs extrêmes et ne suppose pas de distribution normale. Une seule valeur aberrante peut faire exploser la moyenne et l'écart-type, rendant la détection instable.

**Q2 : Comment interpréter un R² = 0.71 ?**  
71% de la variabilité d'IPE est expliquée par les 5 variables. Insuffisant pour des prédictions précises par bâtiment (MAE ~28 kWh/m²/an), mais suffisant pour identifier les déterminants systémiques et prioriser les leviers à l'échelle d'un parc.

**Q3 : Quelles limites voyez-vous à la régression linéaire ici ?**  
Elle suppose des relations additives. Or les effets sont probablement multiplicatifs : un bâtiment ancien + mauvaise isolation + zone froide est bien pire que la somme des trois effets. Un Random Forest ou des termes d'interaction capturerait mieux cette réalité.

**Q4 : Comment passeriez-vous ce framework en production ?**  
Automatisation mensuelle via API Enedis/GrDF → pipeline Airflow ou cron → génération rapport → envoi aux energy managers → dashboard Power BI mis à jour. Alertes automatiques si IPE dépasse le seuil.

**Q5 : Qu'est-ce que le DJU et pourquoi est-ce critique ?**  
Les DJU quantifient le besoin en chauffage. Sans correction, un bâtiment à Lille (2800 DJU/an) semble 30% moins performant qu'un bâtiment identique à Nice (1800 DJU/an) — simplement à cause du climat.

---

## 23. Compétences démontrées

- **Python orienté objet** — Classes `EnergyAnalyzer` / `EnergyVisualizer`
- **pandas** — Groupby, merge, pivot_table, agrégations multi-niveaux
- **scikit-learn** — LinearRegression, LabelEncoder, r2_score, mean_absolute_error
- **matplotlib / seaborn** — Boxplot, barh, scatter, heatmap, donut, subplots
- **Statistiques descriptives** — IQR, percentiles, corrélation de Pearson
- **Feature engineering** — IPE, normalisation DJU, ancienneté dérivée
- **Métriques métier énergie** — IPE, DPE, DJU, kWh/m²/an
- **Reporting automatisé** — Génération Markdown programmatique
- **Git / GitHub** — Versionnement, structure de projet professionnelle

---

## 24. Tableau compétences / preuves

| Compétence | Preuve dans le projet | Fichier |
|-----------|----------------------|---------|
| Python OOP | Classes `EnergyAnalyzer` et `EnergyVisualizer` | `src/energy_analyzer.py` |
| Calcul IPE | Méthode `compute_annual_ipe()` | `src/energy_analyzer.py` |
| Détection IQR | Méthode `detect_high_consumers()` | `src/energy_analyzer.py` |
| Régression sklearn | Méthode `run_regression()` | `src/energy_analyzer.py` |
| Normalisation DJU | Colonne `ipe_normalise` | `src/energy_analyzer.py` |
| 8 visualisations | Classe `EnergyVisualizer` | `src/visualization.py` |
| Avant/après rénovation | Méthode `renovation_impact()` | `src/energy_analyzer.py` |
| ROI économies | Méthode `savings_potential()` | `src/energy_analyzer.py` |
| Pipeline complet | Script 10 sections | `notebooks/01_energy_efficiency_analysis.py` |
| Rapport automatique | Génération Markdown | `notebooks/01_energy_efficiency_analysis.py` |
| Données simulées | 3 CSV cohérents | `data_sample/` |
| Documentation métier | 3 fichiers docs | `docs/` |

---

## 25. Conseils GitHub

### Optimiser la visibilité

1. **Description courte** : "Framework Python d'analyse énergétique bâtiment — IPE, IQR, régression, ROI rénovation"

2. **Topics recommandés** :  
   `python` `data-science` `energy-efficiency` `building-analytics` `pandas` `scikit-learn` `matplotlib` `ipe` `dpe` `portfolio`

3. **Épingler ce dépôt** sur votre profil GitHub parmi les 6 projets mis en avant

4. **Enrichir le README** avec les captures d'écran des figures générées :  
   `![IPE par DPE](figures/fig1_ipe_par_dpe.png)`

5. **Badge LinkedIn** : ajoutez le lien dans la section "En vedette" de votre profil

### Projets connexes du portfolio

| Projet | Lien |
|--------|------|
| Power BI Call Center | [powerbi-callcenter-portfolio](https://github.com/TSAGUE25/powerbi-callcenter-portfolio) |
| Data Quality Audit | [data-quality-audit-framework](https://github.com/TSAGUE25/data-quality-audit-framework) |


## Contributors

| Nom | Role | GitHub |
|-----|------|--------|
| **TSAGUE Emmanuel** | Data Scientist - auteur principal | [@TSAGUE25](https://github.com/TSAGUE25) |

---

*Auteur : Emmanuel TSAGUE — Data Scientist / Data Analyst*  
*Formation : DataScientest | Domaines : Énergie · Industrie · Finance · Performance opérationnelle*  
*Contact : emmoi.mtn@gmail.com*  
*Données : entièrement simulées — aucune donnée réelle ou confidentielle*
