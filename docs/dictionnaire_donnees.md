# Dictionnaire des données — Building Energy Efficiency Analytics

> Données entièrement simulées à des fins pédagogiques.

---

## IPE — Indicateur de Performance Énergétique

**Définition :** Consommation annuelle totale du bâtiment (kWh) divisée par sa surface (m²).  
**Formule :** `IPE = Σ consommation_mensuelle_kwh / surface_m2`  
**Unité :** kWh/m²/an  
**Interprétation :**

| Seuil IPE | Classe DPE | Qualité |
|-----------|-----------|---------|
| < 50 | A | Excellent |
| 50–90 | B | Très bon |
| 90–150 | C | Bon |
| 150–230 | D | Moyen |
| 230–330 | E | Médiocre |
| 330–450 | F | Mauvais |
| ≥ 450 | G | Très mauvais |

---

## DJU — Degrés Jours Unifiés

**Définition :** Indicateur météorologique mesurant l'écart entre la température extérieure et une température de référence (18°C).  
**Formule :** `DJU_mois = Σ max(0, 18 - T_moy_jour)` sur tous les jours du mois  
**Utilisation :** Normalisation climatique de la consommation. Permet de comparer deux bâtiments situés dans des zones climatiques différentes.  
**Exemple :** Un bâtiment parisien (DJU ≈ 2400/an) consomme davantage pour le chauffage qu'un bâtiment niçois (DJU ≈ 1500/an) à performance égale.

---

## DPE — Diagnostic de Performance Énergétique

**Définition :** Label réglementaire français évaluant la performance énergétique d'un bâtiment sur une échelle de A (très efficace) à G (très énergivore).  
**Base réglementaire :** Décret n° 2021-872 du 30 juin 2021 (DPE opposable).  
**Composantes :** Consommation d'énergie primaire + Émissions de CO2 (double seuil depuis 2021).

---

## Variables du modèle de régression

| Variable | Rôle | Justification |
|----------|------|---------------|
| `surface_m2` | Explicative | Les grands bâtiments consomment plus en absolu mais pas nécessairement en kWh/m² |
| `annee_construction` | Explicative | Les bâtiments anciens ont moins d'isolation, normes moins strictes |
| `dju_annuel` | Explicative | Climat local — principale variable explicative du chauffage |
| `type_usage` | Catégorielle | Un hôpital (24/7) n'a pas le même profil qu'un entrepôt |
| `isolation` | Catégorielle | Qualité de l'enveloppe thermique |

---

## Glossaire métier

| Terme | Définition |
|-------|-----------|
| **Bâtiment énergivore** | IPE > Q3 + 1,5 × IQR du parc analysé |
| **Rénovation performante** | Gain IPE ≥ 15% après rénovation |
| **Économie potentielle** | (IPE_actuel - IPE_cible) × surface_m2 |
| **Normalisation climatique** | IPE ajusté en fonction du ratio DJU_réel / DJU_référence |
| **IQR** | Interquartile Range : Q3 - Q1, mesure de dispersion robuste |
