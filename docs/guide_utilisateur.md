# Guide utilisateur — Building Energy Efficiency Analytics

## Prérequis

```bash
pip install -r requirements.txt
```

## Lancer l'analyse complète

```bash
cd building-energy-efficiency-analytics
python notebooks/01_energy_efficiency_analysis.py
```

L'exécution produit :
- **8 figures** dans `figures/`
- **1 rapport Markdown** dans `reports/energy_audit_report_sample.md`
- Les résultats affichés en console (IPE, segmentation, régression, économies)

## Utiliser les classes Python directement

```python
import pandas as pd
from src.energy_analyzer import EnergyAnalyzer
from src.visualization import EnergyVisualizer

buildings = pd.read_csv('data_sample/buildings_characteristics.csv')
consumption = pd.read_csv('data_sample/energy_consumption_monthly.csv')

analyzer = EnergyAnalyzer(buildings, consumption)
annual = analyzer.compute_annual_ipe()

# Top bâtiments énergivores
print(analyzer.detect_high_consumers())

# Potentiel d'économie
print(analyzer.savings_potential(target_ipe=150))

# Régression
reg = analyzer.run_regression()
print(f"R² = {reg['r2']:.3f}")

# Visualisations
viz = EnergyVisualizer(output_dir='figures')
viz.plot_ipe_by_dpe(annual)
viz.plot_savings_potential(analyzer.savings_potential())
```

## Structure des sorties

| Fichier | Contenu |
|---------|---------|
| `figures/fig1_ipe_par_dpe.png` | Boxplot IPE par étiquette DPE |
| `figures/fig2_ipe_par_type_usage.png` | Barh IPE moyen par type |
| `figures/fig3_evolution_temporelle.png` | Tendance 2021–2023 |
| `figures/fig4_conso_vs_dju.png` | Scatter consommation/DJU |
| `figures/fig5_heatmap_ipe.png` | Heatmap bâtiment × année |
| `figures/fig6_potentiel_economies.png` | Économies potentielles top 10 |
| `figures/fig7_repartition_dpe.png` | Donut répartition DPE |
| `figures/fig8_impact_renovation.png` | Avant/après rénovation |
| `reports/energy_audit_report_sample.md` | Rapport Markdown complet |

## Adapter à vos propres données

Remplacez les CSV par vos fichiers en respectant le schéma décrit dans `data_sample/schema_reference.md`. Les colonnes obligatoires sont documentées dans le dictionnaire des données.
