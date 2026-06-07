# Rapport d'Audit Énergétique — Parc Bâtimentaire

**Date :** 2024-12-15  
**Périmètre :** 20 bâtiments | 3 années (2021–2023)  
**Surface totale :** 127 150 m²

> *Données simulées à des fins pédagogiques — aucune donnée réelle.*

---

## 1. Synthèse exécutive

| Indicateur | Valeur |
|-----------|--------|
| IPE moyen du parc | **218 kWh/m²/an** |
| IPE médian | **195 kWh/m²/an** |
| Bâtiment le plus efficace | **B011 (Siège Nexia)** — 87 kWh/m²/an (DPE A) |
| Bâtiment le moins efficace | **B006 (Gymnase Municipal)** — 432 kWh/m²/an (DPE G) |
| Bâtiments énergivores détectés | **4 bâtiments** (IQR) |
| Économie potentielle | **1,42 GWh/an** (170 400 €/an) |
| Rénovations réalisées | **3 bâtiments** (B002, B010, B016) |

---

## 2. Répartition DPE du parc

| DPE | Nb bâtiments | % parc | IPE moyen |
|-----|-------------|--------|-----------|
| A | 2 | 10% | 80 kWh/m²/an |
| B | 2 | 10% | 105 kWh/m²/an |
| C | 3 | 15% | 132 kWh/m²/an |
| D | 5 | 25% | 188 kWh/m²/an |
| E | 4 | 20% | 265 kWh/m²/an |
| F | 2 | 10% | 358 kWh/m²/an |
| G | 2 | 10% | 428 kWh/m²/an |

**Constat :** 30% du parc est en DPE F ou G, représentant les leviers de réduction les plus importants.

---

## 3. Bâtiments énergivores détectés (méthode IQR)

| Bâtiment | IPE (kWh/m²/an) | Borne IQR | Écart | DPE | Type | Action recommandée |
|----------|-----------------|-----------|-------|-----|------|--------------------|
| B006 — Gymnase Municipal | 432 | 368 | +64 | G | Sport | Audit urgent — remplacement chaudière fioul |
| B007 — Mairie Annexe | 415 | 368 | +47 | G | Bureau | Isolation toiture + remplacement menuiseries |
| B003 — École Jean Moulin | 388 | 368 | +20 | F | École | Passage au gaz condensation |
| B014 — École Primaire Pasteur | 372 | 368 | +4 | F | École | Isolation façade prioritaire |

---

## 4. Modèle de régression linéaire

**IPE ~ surface + ancienneté + DJU + type_usage + isolation**

| Métrique | Valeur |
|---------|--------|
| R² | **0.71** |
| MAE | **28,4 kWh/m²/an** |

| Facteur | Coefficient | Interprétation |
|---------|-------------|----------------|
| Ancienneté (+1 an) | +1.85 | Un bâtiment plus vieux d'un an consomme ~2 kWh/m²/an de plus |
| DJU annuel (+100 DJU) | +8.20 | Chaque 100 DJU supplémentaires = +8 kWh/m²/an |
| Surface (m²) | -0.0008 | Légère économie d'échelle pour les grands bâtiments |

**Conclusion :** L'ancienneté et le climat (DJU) sont les deux principaux déterminants de l'IPE.

---

## 5. Impact des rénovations réalisées

| Bâtiment | Rénovation | IPE avant | IPE après | Gain |
|----------|-----------|-----------|-----------|------|
| B002 — Résidence Les Pins | 2019 | 210 kWh/m²/an | 172 kWh/m²/an | **-18%** |
| B010 — Lycée Victor Hugo | 2018 | 285 kWh/m²/an | 228 kWh/m²/an | **-20%** |
| B016 — Résidence du Parc | 2021 | 248 kWh/m²/an | 198 kWh/m²/an | **-20%** |

---

## 6. Potentiel d'économie — Top 5 priorités

| Bâtiment | IPE actuel | Écart cible (195) | Économie (MWh/an) | Économie (€/an) |
|----------|-----------|-------------------|-------------------|-----------------|
| B006 — Gymnase Municipal | 432 | 237 | 427 | 51 240 € |
| B020 — Tour Horizon | 312 | 117 | 2 574 | 308 880 € |
| B007 — Mairie Annexe | 415 | 220 | 264 | 31 680 € |
| B003 — École Jean Moulin | 388 | 193 | 405 | 48 600 € |
| B001 — Tour Centrale | 295 | 100 | 850 | 102 000 € |

---

## 7. Recommandations prioritaires

### Court terme (< 6 mois)
1. **Audit thermique** des bâtiments B006 et B007 (DPE G, chauffage fioul)
2. **Remplacement des chaudières fioul** : B003, B006, B007, B014
3. **Contrat de performance énergétique (CPE)** pour B020 (22 000 m² — fort enjeu financier)

### Moyen terme (6–24 mois)
4. **Programme d'isolation** pour les 6 bâtiments à isolation "Mauvaise"
5. **Déploiement de compteurs communicants** pour le suivi mensuel automatisé
6. **Tableau de bord de pilotage** Power BI (modèle disponible dans `/dashboard`)

### Long terme (> 2 ans)
7. **Transition vers pompes à chaleur** pour les bâtiments gaz anciens
8. **Certification ISO 50001** (Système de Management de l'Énergie) pour le parc
9. **Extension de l'analyse** à 100+ bâtiments avec automatisation du pipeline

---

## 8. Gouvernance des données énergétiques

- Mettre en place une **collecte mensuelle automatisée** via API compteurs
- Définir un **score seuil d'alerte** : tout bâtiment dépassant 300 kWh/m²/an déclenche une revue
- Nommer un **Energy Manager** par région avec tableau de bord dédié
- Documenter les **hypothèses de calcul** (tarif €/kWh, DJU de référence) dans le dictionnaire de données

---

*Rapport généré automatiquement par le Building Energy Efficiency Analytics Framework*  
*Auteur : Emmanuel TSAGUE — Data Scientist / Data Analyst*  
*Source : données simulées — aucune donnée réelle ou confidentielle*
