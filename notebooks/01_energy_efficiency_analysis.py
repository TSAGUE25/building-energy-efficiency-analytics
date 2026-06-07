"""
Analyse de l'efficacité énergétique des bâtiments
Cas 1 — Portfolio Data Science | Emmanuel TSAGUE
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from src.energy_analyzer import EnergyAnalyzer
from src.visualization import EnergyVisualizer

# ======================================================================
# 0. CHARGEMENT DES DONNÉES
# ======================================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data_sample')
FIGURES_DIR = os.path.join(BASE_DIR, 'figures')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

buildings = pd.read_csv(os.path.join(DATA_DIR, 'buildings_characteristics.csv'))
consumption = pd.read_csv(os.path.join(DATA_DIR, 'energy_consumption_monthly.csv'))
meteo = pd.read_csv(os.path.join(DATA_DIR, 'meteo_sample.csv'))

print(f"Bâtiments : {buildings.shape}")
print(f"Consommations mensuelles : {consumption.shape}")
print(f"Données météo : {meteo.shape}")

# ======================================================================
# 1. EXPLORATION DES DONNÉES (EDA)
# ======================================================================

print("\n" + "="*60)
print("1. EXPLORATION DES DONNÉES")
print("="*60)

print("\n--- Bâtiments par type d'usage ---")
print(buildings['type_usage'].value_counts())

print("\n--- Répartition DPE ---")
print(buildings['etiquette_dpe'].value_counts().sort_index())

print("\n--- Types de chauffage ---")
print(buildings['type_chauffage'].value_counts())

print("\n--- Surface (m²) ---")
print(buildings['surface_m2'].describe())

print("\n--- Valeurs manquantes (consommation) ---")
print(consumption.isnull().sum())

# Vérification de la cohérence : conso_totale = elec + gaz
consumption['check'] = (
    consumption['consommation_totale_kwh'] ==
    consumption['consommation_elec_kwh'] + consumption['consommation_gaz_kwh']
)
print(f"\nCohérence élec+gaz=total : {consumption['check'].all()} "
      f"({consumption['check'].sum()}/{len(consumption)} lignes OK)")

# Bâtiments avec chauffage électrique ou PAC mais consommation gaz > 0
elec_batiments = buildings[buildings['type_chauffage'].isin(['Électrique', 'Pompe à chaleur'])]['id_batiment']
anomalie_gaz = consumption[
    consumption['id_batiment'].isin(elec_batiments) &
    (consumption['consommation_gaz_kwh'] > 0)
]
print(f"\nAnomalies gaz pour bâtiments élec/PAC : {len(anomalie_gaz)} lignes")

# ======================================================================
# 2. CALCUL DES IPE ET ANALYSE ANNUELLE
# ======================================================================

print("\n" + "="*60)
print("2. CALCUL DES IPE (kWh/m²/an)")
print("="*60)

analyzer = EnergyAnalyzer(buildings, consumption, meteo)
annual = analyzer.compute_annual_ipe()

print("\n--- IPE annuel (kWh/m²/an) — aperçu ---")
print(annual[['id_batiment', 'annee', 'ipe_kwh_m2', 'ipe_normalise', 'etiquette_dpe', 'type_usage']].to_string(index=False))

summary = analyzer.summary_report()
print(f"\n--- Synthèse du parc ---")
print(f"Nombre de bâtiments      : {summary['nb_batiments']}")
print(f"Surface totale           : {summary['surface_totale_m2']:,} m²")
print(f"IPE moyen parc           : {summary['ipe_moyen_parc']} kWh/m²/an")
print(f"IPE médian parc          : {summary['ipe_median_parc']} kWh/m²/an")
print(f"IPE min (meilleur)       : {summary['ipe_min']} kWh/m²/an → {summary['batiment_plus_efficient']}")
print(f"IPE max (moins efficient): {summary['ipe_max']} kWh/m²/an → {summary['batiment_moins_efficient']}")
print(f"Répartition DPE          : {summary['repartition_dpe']}")

# ======================================================================
# 3. SEGMENTATION
# ======================================================================

print("\n" + "="*60)
print("3. SEGMENTATION")
print("="*60)

print("\n--- IPE par étiquette DPE ---")
print(analyzer.segment_by_dpe().round(1))

print("\n--- IPE par type d'usage ---")
print(analyzer.segment_by_type().round(1))

# ======================================================================
# 4. DÉTECTION DES BÂTIMENTS ÉNERGIVORES (IQR)
# ======================================================================

print("\n" + "="*60)
print("4. BÂTIMENTS ÉNERGIVORES (IQR)")
print("="*60)

outliers = analyzer.detect_high_consumers()
print(f"\n{len(outliers)} bâtiments dépassent la borne IQR :")
print(outliers[['id_batiment', 'annee', 'ipe_kwh_m2', 'borne_haute_iqr',
                'ecart_borne', 'etiquette_dpe', 'type_usage']].to_string(index=False))

# ======================================================================
# 5. CORRÉLATION CONSOMMATION / TEMPÉRATURE
# ======================================================================

print("\n" + "="*60)
print("5. CORRÉLATION CONSOMMATION / TEMPÉRATURE")
print("="*60)

corr = analyzer.temperature_correlation()
print("\nMatrice de corrélation :")
print(corr.round(3))

# ======================================================================
# 6. RÉGRESSION LINÉAIRE
# ======================================================================

print("\n" + "="*60)
print("6. RÉGRESSION LINÉAIRE : IPE ~ facteurs")
print("="*60)

reg = analyzer.run_regression()
print(f"\nR² : {reg['r2']:.3f}")
print(f"MAE : {reg['mae']:.1f} kWh/m²/an")
print("\nCoefficients :")
for feat, coef in reg['coefficients'].items():
    print(f"  {feat:15s} : {coef:+.4f}")
print(f"  {'Intercept':15s} : {reg['intercept']:+.4f}")

print("\nInterprétation :")
print(f"  → +1 an d'ancienneté = {reg['coefficients'].get('anciennete', 0):+.2f} kWh/m²/an")
print(f"  → +100 DJU = {reg['coefficients'].get('dju_annuel', 0)*100:+.2f} kWh/m²/an")

# ======================================================================
# 7. IMPACT DES RÉNOVATIONS
# ======================================================================

print("\n" + "="*60)
print("7. IMPACT DES RÉNOVATIONS")
print("="*60)

impact = analyzer.renovation_impact()
if not impact.empty:
    print("\nGain IPE avant/après rénovation :")
    print(impact.round(1))
else:
    print("Données insuffisantes pour comparaison avant/après.")

# ======================================================================
# 8. POTENTIEL D'ÉCONOMIE
# ======================================================================

print("\n" + "="*60)
print("8. POTENTIEL D'ÉCONOMIE")
print("="*60)

savings = analyzer.savings_potential()
print(f"\nCible IPE retenue : {savings['target_ipe'].iloc[0]:.0f} kWh/m²/an (médiane du parc)")
print(f"Économie totale potentielle : {savings['economie_kwh_an'].sum()/1e6:.2f} GWh/an")
print(f"Économie financière estimée : {savings['economie_euro_an'].sum():,.0f} €/an")
print("\nTop 5 bâtiments à fort potentiel :")
print(savings[['id_batiment', 'ipe_moyen', 'ecart_cible',
               'economie_kwh_an', 'economie_euro_an']].head(5).round(0).to_string(index=False))

# ======================================================================
# 9. VISUALISATIONS
# ======================================================================

print("\n" + "="*60)
print("9. GÉNÉRATION DES FIGURES")
print("="*60)

viz = EnergyVisualizer(output_dir=FIGURES_DIR)

viz.plot_dpe_distribution(buildings)
viz.plot_ipe_by_dpe(annual)
viz.plot_ipe_by_type(annual)
viz.plot_consumption_trend(annual)
viz.plot_consumption_vs_dju(consumption, buildings)
viz.plot_ipe_heatmap(annual)
viz.plot_savings_potential(savings)
if not impact.empty:
    viz.plot_renovation_impact(impact)

print("\n8 figures générées dans le dossier figures/")

# ======================================================================
# 10. RAPPORT SYNTHÈSE (Markdown)
# ======================================================================

print("\n" + "="*60)
print("10. GÉNÉRATION DU RAPPORT")
print("="*60)

os.makedirs(REPORTS_DIR, exist_ok=True)

rapport_path = os.path.join(REPORTS_DIR, 'energy_audit_report_sample.md')

rapport_lines = [
    "# Rapport d'Audit Énergétique — Parc Bâtimentaire",
    "",
    f"**Date :** 2024-12-15  ",
    f"**Périmètre :** {summary['nb_batiments']} bâtiments | 3 années (2021–2023)  ",
    f"**Surface totale :** {summary['surface_totale_m2']:,} m²",
    "",
    "> *Données simulées à des fins pédagogiques — aucune donnée réelle.*",
    "",
    "---",
    "",
    "## 1. Synthèse exécutive",
    "",
    "| Indicateur | Valeur |",
    "|-----------|--------|",
    f"| IPE moyen du parc | **{summary['ipe_moyen_parc']} kWh/m²/an** |",
    f"| IPE médian | **{summary['ipe_median_parc']} kWh/m²/an** |",
    f"| Meilleur bâtiment | **{summary['batiment_plus_efficient']}** — {summary['ipe_min']} kWh/m²/an |",
    f"| Bâtiment le moins efficace | **{summary['batiment_moins_efficient']}** — {summary['ipe_max']} kWh/m²/an |",
    f"| Économie potentielle | **{savings['economie_kwh_an'].sum()/1e6:.2f} GWh/an** ({savings['economie_euro_an'].sum():,.0f} €) |",
    "",
    "---",
    "",
    "## 2. Bâtiments énergivores détectés",
    "",
    "| Bâtiment | Année | IPE (kWh/m²/an) | Borne IQR | Écart | DPE | Type |",
    "|----------|-------|-----------------|-----------|-------|-----|------|",
]

for _, row in outliers.iterrows():
    rapport_lines.append(
        f"| {row['id_batiment']} | {int(row['annee'])} | {row['ipe_kwh_m2']:.0f} | "
        f"{row['borne_haute_iqr']:.0f} | +{row['ecart_borne']:.0f} | "
        f"{row['etiquette_dpe']} | {row['type_usage']} |"
    )

rapport_lines += [
    "",
    "---",
    "",
    "## 3. Régression linéaire",
    "",
    f"- **R² = {reg['r2']:.3f}** — le modèle explique {reg['r2']*100:.1f}% de la variance de l'IPE",
    f"- **MAE = {reg['mae']:.1f} kWh/m²/an**",
    "",
    "| Facteur | Coefficient | Interprétation |",
    "|---------|-------------|----------------|",
    f"| Ancienneté (ans) | {reg['coefficients'].get('anciennete', 0):+.3f} | +1 an → {reg['coefficients'].get('anciennete', 0):+.2f} kWh/m²/an |",
    f"| DJU annuel | {reg['coefficients'].get('dju_annuel', 0):+.4f} | +100 DJU → {reg['coefficients'].get('dju_annuel', 0)*100:+.2f} kWh/m²/an |",
    f"| Surface (m²) | {reg['coefficients'].get('surface_m2', 0):+.6f} | Effet faible |",
    "",
    "---",
    "",
    "## 4. Recommandations prioritaires",
    "",
    "1. **Rénovation thermique** des bâtiments DPE F et G (chauffage fioul, isolation mauvaise)",
    "2. **Remplacement des chaudières fioul** par pompes à chaleur ou gaz condensation",
    "3. **Suivi mensuel** des bâtiments dépassant 300 kWh/m²/an",
    "4. **Audit approfondi** des bâtiments B006 (Gymnase) et B007 (Mairie) en priorité",
    "",
    "---",
    "",
    "*Rapport généré automatiquement — Building Energy Efficiency Analytics*  ",
    "*Auteur : Emmanuel TSAGUE — Data Scientist / Data Analyst*",
]

with open(rapport_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(rapport_lines))

print(f"Rapport sauvegardé : {rapport_path}")
print("\n=== ANALYSE TERMINÉE ===")
