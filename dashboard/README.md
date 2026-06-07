# Dashboard Power BI — Efficacité Énergétique Bâtiments

Ce dossier contient les ressources pour le tableau de bord Power BI complémentaire à l'analyse Python.

## Pages du dashboard (6 pages)

| Page | Titre | Contenu principal |
|------|-------|------------------|
| 1 | Vue Exécutive | IPE moyen parc, carte géographique, répartition DPE (donut), KPIs clés |
| 2 | Analyse par Bâtiment | Table détaillée, filtres multi-critères, jauge IPE vs cible |
| 3 | Évolution Temporelle | Courbes 2021–2023, variation YoY, saisonnalité mensuelle |
| 4 | Segmentation | Matrice DPE × Type d'usage, heatmap IPE, benchmark |
| 5 | Bâtiments Énergivores | Alertes IQR, classement des bâtiments prioritaires |
| 6 | Plan d'Action | Potentiel d'économie, ROI rénovation, feuille de route |

## Modèle de données (schéma étoile)

```
         F_CONSOMMATION_MENSUELLE
        /        |        \
D_BATIMENT   D_DATE    D_METEO
```

### Mesures DAX clés

```dax
IPE_Moyen = 
DIVIDE(
    SUM(F_CONSOMMATION_MENSUELLE[consommation_totale_kwh]),
    SUM(D_BATIMENT[surface_m2])
)

IPE_Annuel = 
CALCULATE(
    [IPE_Moyen],
    FILTER(ALL(D_DATE), D_DATE[annee] = MAX(D_DATE[annee]))
)

Variation_YoY_IPE = 
DIVIDE(
    [IPE_Annuel] - CALCULATE([IPE_Annuel], SAMEPERIODLASTYEAR(D_DATE[date])),
    CALCULATE([IPE_Annuel], SAMEPERIODLASTYEAR(D_DATE[date]))
)

Economie_Potentielle_MWh = 
SUMX(
    D_BATIMENT,
    MAX(0, [IPE_Moyen] - [IPE_Cible]) * D_BATIMENT[surface_m2] / 1000
)

Score_Performance =
SWITCH(
    TRUE(),
    [IPE_Moyen] < 50, "A — Excellent",
    [IPE_Moyen] < 90, "B — Très bon",
    [IPE_Moyen] < 150, "C — Bon",
    [IPE_Moyen] < 230, "D — Moyen",
    [IPE_Moyen] < 330, "E — Médiocre",
    [IPE_Moyen] < 450, "F — Mauvais",
    "G — Très mauvais"
)
```

## Fichier Power BI

Placez votre fichier `.pbix` dans ce dossier et nommez-le :  
`energy_efficiency_dashboard.pbix`

## Captures d'écran

Placez les captures dans `dashboard/screenshots/` :
- `page1_vue_executive.png`
- `page2_analyse_batiment.png`
- `page3_evolution_temporelle.png`
- `page4_segmentation.png`
- `page5_energivores.png`
- `page6_plan_action.png`
