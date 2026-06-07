# Schéma de référence — Building Energy Efficiency Analytics

> Données entièrement simulées à des fins pédagogiques. Aucune donnée réelle.

---

## Table 1 : `buildings_characteristics.csv`

| Colonne | Type | Description | Valeurs / Contraintes |
|---------|------|-------------|----------------------|
| `id_batiment` | string | Identifiant unique | B001–B020, non nul, unique |
| `nom_batiment` | string | Nom fictif du bâtiment | Non nul |
| `type_usage` | string | Catégorie d'usage | Bureau, Logement collectif, École, Entrepôt, Hôtel, Commerce, Hôpital, Sport |
| `ville` | string | Ville d'implantation | Paris, Lyon, Bordeaux, Rennes, Nice, Grenoble, Strasbourg, Lille, Nantes, Besançon, Toulouse, Metz, Rouen, Caen, Marseille, Montpellier, La Défense |
| `region` | string | Région administrative | 13 régions métropolitaines |
| `surface_m2` | integer | Surface totale en m² | 650–22 000, > 0 |
| `annee_construction` | integer | Année de construction | 1960–2020 |
| `etiquette_dpe` | string | Étiquette DPE | A, B, C, D, E, F, G |
| `type_chauffage` | string | Énergie principale de chauffage | Gaz, Fioul, Électrique, Pompe à chaleur |
| `isolation` | string | Qualité de l'isolation | Bonne, Moyenne, Mauvaise |
| `nb_occupants_moyen` | integer | Nombre moyen d'occupants | > 0 |
| `renovation_realisee` | integer | Rénovation effectuée (flag) | 0 = Non, 1 = Oui |
| `annee_renovation` | integer | Année de la rénovation | 2015–2023, null si renovation_realisee = 0 |

**Cardinalité :** 20 bâtiments

---

## Table 2 : `energy_consumption_monthly.csv`

| Colonne | Type | Description | Valeurs / Contraintes |
|---------|------|-------------|----------------------|
| `id_batiment` | string | Identifiant du bâtiment | FK → buildings_characteristics.id_batiment |
| `annee` | integer | Année | 2021, 2022, 2023 |
| `mois` | integer | Mois (numérique) | 1–12 |
| `consommation_elec_kwh` | integer | Consommation électrique mensuelle (kWh) | ≥ 0 |
| `consommation_gaz_kwh` | integer | Consommation gaz mensuelle (kWh) | ≥ 0, 0 si chauffage non gaz |
| `consommation_totale_kwh` | integer | Consommation totale (élec + gaz) | = elec + gaz |
| `temperature_moy_c` | float | Température mensuelle moyenne (°C) | -5 à 35 |
| `dju_chauffage` | integer | Degrés Jours Unifiés chauffage (base 18°C) | ≥ 0, 0 en été |

**Cardinalité :** 720 lignes (20 bâtiments × 3 ans × 12 mois)

**Note DJU :** DJU = Σ max(0, 18 - T_moy_jour). Valeur nulle si T_moy_mois ≥ 18°C.

---

## Table 3 : `meteo_sample.csv`

| Colonne | Type | Description | Valeurs / Contraintes |
|---------|------|-------------|----------------------|
| `ville` | string | Ville | Correspond aux villes de buildings_characteristics |
| `region` | string | Région | Correspond aux régions de buildings_characteristics |
| `annee` | integer | Année | 2021, 2022, 2023 |
| `mois` | integer | Mois | 1–12 |
| `temperature_moy_c` | float | Température mensuelle moyenne (°C) | |
| `temperature_min_c` | float | Température minimale mensuelle (°C) | ≤ temperature_moy_c |
| `temperature_max_c` | float | Température maximale mensuelle (°C) | ≥ temperature_moy_c |
| `dju_chauffage` | integer | DJU chauffage mensuel | ≥ 0 |
| `precipitation_mm` | integer | Précipitations mensuelles (mm) | ≥ 0 |
| `ensoleillement_h` | integer | Heures d'ensoleillement mensuelles | ≥ 0 |

**Cardinalité :** 6 villes × 3 ans × 12 mois = 216 lignes (villes : Paris, Lyon, Bordeaux, Rennes, Nice, Grenoble)

---

## Relations entre tables

```
buildings_characteristics
    id_batiment (PK)
         │
         ├──→ energy_consumption_monthly.id_batiment (FK)
         │
         └──→ [jointure ville] meteo_sample.ville
```

---

## Métriques dérivées (calculées dans l'analyse)

| Métrique | Formule | Unité | Interprétation |
|----------|---------|-------|----------------|
| **IPE** (Indicateur de Performance Énergétique) | consommation_annuelle_kwh / surface_m2 | kWh/m²/an | Plus bas = plus performant |
| **IPE normalisé DJU** | IPE / (DJU_annuel / DJU_référence) | kWh/m²/an | Corrige l'effet climatique |
| **Classe DPE calculée** | Seuils réglementaires sur IPE | A–G | A < 50, B < 90, C < 150, D < 230, E < 330, F < 450, G ≥ 450 |
| **Variation YoY** | (IPE_N - IPE_N-1) / IPE_N-1 | % | Tendance annuelle |

---

## Règles métier

1. Un bâtiment avec `etiquette_dpe` = G et `isolation` = Bonne est incohérent → signaler
2. Si `renovation_realisee` = 1 et `annee_renovation` est null → anomalie
3. Si `consommation_gaz_kwh` > 0 pour un bâtiment `type_chauffage` = Électrique ou Pompe à chaleur → vérifier
4. `consommation_totale_kwh` doit toujours = `consommation_elec_kwh` + `consommation_gaz_kwh`
5. Les DJU chauffage doivent être 0 pour les mois où `temperature_moy_c` ≥ 18°C

---

*Données simulées — Emmanuel TSAGUE — Data Scientist / Data Analyst*
