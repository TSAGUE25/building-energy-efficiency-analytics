import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import os

DPE_COLORS = {
    'A': '#00a651', 'B': '#57b947', 'C': '#c6d52a',
    'D': '#ffd800', 'E': '#f7a600', 'F': '#ee1c25', 'G': '#9b1b1b'
}
DPE_ORDER = ['A', 'B', 'C', 'D', 'E', 'F', 'G']


class EnergyVisualizer:
    """Visualisations pour l'analyse énergétique du parc bâtimentaire."""

    def __init__(self, output_dir='figures'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        plt.rcParams.update({'figure.dpi': 120, 'font.family': 'DejaVu Sans'})

    def _save(self, fig, filename):
        path = os.path.join(self.output_dir, filename)
        fig.savefig(path, bbox_inches='tight')
        plt.close(fig)
        print(f"Figure sauvegardée : {path}")
        return path

    # ------------------------------------------------------------------ #
    # Figure 1 : Distribution IPE par DPE
    # ------------------------------------------------------------------ #

    def plot_ipe_by_dpe(self, annual_df):
        fig, ax = plt.subplots(figsize=(10, 6))
        present = [d for d in DPE_ORDER if d in annual_df['etiquette_dpe'].values]
        colors = [DPE_COLORS[d] for d in present]
        data = [annual_df.loc[annual_df['etiquette_dpe'] == d, 'ipe_kwh_m2'].values
                for d in present]
        bp = ax.boxplot(data, labels=present, patch_artist=True, notch=False,
                        medianprops=dict(color='black', linewidth=2))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.75)
        ax.set_xlabel('Étiquette DPE', fontsize=12)
        ax.set_ylabel('IPE (kWh/m²/an)', fontsize=12)
        ax.set_title('Distribution de l\'IPE par étiquette DPE', fontsize=14, fontweight='bold')
        ax.axhline(annual_df['ipe_kwh_m2'].median(), color='navy', linestyle='--',
                   linewidth=1.5, label=f"Médiane parc : {annual_df['ipe_kwh_m2'].median():.0f} kWh/m²/an")
        ax.legend(fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        return self._save(fig, 'fig1_ipe_par_dpe.png')

    # ------------------------------------------------------------------ #
    # Figure 2 : IPE moyen par type d'usage (barh)
    # ------------------------------------------------------------------ #

    def plot_ipe_by_type(self, annual_df):
        seg = (annual_df.groupby('type_usage')['ipe_kwh_m2']
               .mean().sort_values(ascending=True))
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(seg.index, seg.values, color='steelblue', edgecolor='white', height=0.6)
        median = annual_df['ipe_kwh_m2'].median()
        ax.axvline(median, color='crimson', linestyle='--', linewidth=1.5,
                   label=f'Médiane parc : {median:.0f} kWh/m²/an')
        for bar, val in zip(bars, seg.values):
            ax.text(val + 2, bar.get_y() + bar.get_height() / 2,
                    f'{val:.0f}', va='center', fontsize=10)
        ax.set_xlabel('IPE moyen (kWh/m²/an)', fontsize=12)
        ax.set_title('IPE moyen par type d\'usage', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(axis='x', alpha=0.3)
        return self._save(fig, 'fig2_ipe_par_type_usage.png')

    # ------------------------------------------------------------------ #
    # Figure 3 : Évolution temporelle de la consommation
    # ------------------------------------------------------------------ #

    def plot_consumption_trend(self, annual_df):
        trend = (annual_df.groupby('annee')
                 .agg(conso_totale=('conso_totale_kwh', 'sum'),
                      ipe_moyen=('ipe_kwh_m2', 'mean'))
                 .reset_index())
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        ax1.bar(trend['annee'], trend['conso_totale'] / 1e6, color=['#2196F3', '#4CAF50', '#FF9800'],
                edgecolor='white', width=0.5)
        ax1.set_title('Consommation totale du parc (GWh)', fontsize=13, fontweight='bold')
        ax1.set_ylabel('GWh/an', fontsize=11)
        ax1.set_xlabel('Année', fontsize=11)
        for i, row in trend.iterrows():
            ax1.text(row['annee'], row['conso_totale'] / 1e6 + 0.02,
                     f"{row['conso_totale']/1e6:.2f}", ha='center', fontsize=10)
        ax1.grid(axis='y', alpha=0.3)

        ax2.plot(trend['annee'], trend['ipe_moyen'], marker='o', color='crimson',
                 linewidth=2.5, markersize=8)
        ax2.fill_between(trend['annee'], trend['ipe_moyen'], alpha=0.15, color='crimson')
        ax2.set_title('IPE moyen du parc (kWh/m²/an)', fontsize=13, fontweight='bold')
        ax2.set_ylabel('kWh/m²/an', fontsize=11)
        ax2.set_xlabel('Année', fontsize=11)
        for _, row in trend.iterrows():
            ax2.annotate(f"{row['ipe_moyen']:.0f}", (row['annee'], row['ipe_moyen']),
                         textcoords='offset points', xytext=(0, 10), ha='center', fontsize=10)
        ax2.grid(alpha=0.3)

        fig.suptitle('Évolution 2021–2023 du parc bâtimentaire', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return self._save(fig, 'fig3_evolution_temporelle.png')

    # ------------------------------------------------------------------ #
    # Figure 4 : Corrélation consommation / DJU (scatter)
    # ------------------------------------------------------------------ #

    def plot_consumption_vs_dju(self, consumption_df, buildings_df):
        df = consumption_df.merge(
            buildings_df[['id_batiment', 'surface_m2', 'type_chauffage']], on='id_batiment'
        )
        df['conso_m2'] = df['consommation_totale_kwh'] / df['surface_m2']
        palette = {
            'Gaz': '#E53935', 'Fioul': '#8D6E63',
            'Électrique': '#1E88E5', 'Pompe à chaleur': '#43A047'
        }
        fig, ax = plt.subplots(figsize=(10, 6))
        for chauff, grp in df.groupby('type_chauffage'):
            ax.scatter(grp['dju_chauffage'], grp['conso_m2'],
                       alpha=0.5, s=30, label=chauff, color=palette.get(chauff, 'grey'))
        z = np.polyfit(df['dju_chauffage'], df['conso_m2'], 1)
        p = np.poly1d(z)
        x_line = np.linspace(df['dju_chauffage'].min(), df['dju_chauffage'].max(), 100)
        ax.plot(x_line, p(x_line), 'k--', linewidth=1.5, label='Tendance générale')
        ax.set_xlabel('DJU chauffage mensuel', fontsize=12)
        ax.set_ylabel('Consommation mensuelle (kWh/m²)', fontsize=12)
        ax.set_title('Consommation vs DJU par type de chauffage', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3)
        return self._save(fig, 'fig4_conso_vs_dju.png')

    # ------------------------------------------------------------------ #
    # Figure 5 : Heatmap IPE bâtiment × année
    # ------------------------------------------------------------------ #

    def plot_ipe_heatmap(self, annual_df):
        pivot = annual_df.pivot_table(
            index='id_batiment', columns='annee', values='ipe_kwh_m2', aggfunc='mean'
        )
        fig, ax = plt.subplots(figsize=(10, 10))
        sns.heatmap(pivot, annot=True, fmt='.0f', cmap='RdYlGn_r',
                    linewidths=0.5, ax=ax, cbar_kws={'label': 'kWh/m²/an'})
        ax.set_title('IPE par bâtiment et par année (kWh/m²/an)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Année', fontsize=12)
        ax.set_ylabel('Identifiant bâtiment', fontsize=12)
        plt.tight_layout()
        return self._save(fig, 'fig5_heatmap_ipe.png')

    # ------------------------------------------------------------------ #
    # Figure 6 : Potentiel d'économie
    # ------------------------------------------------------------------ #

    def plot_savings_potential(self, savings_df):
        top = savings_df[savings_df['economie_kwh_an'] > 0].head(10)
        fig, ax = plt.subplots(figsize=(11, 6))
        colors = ['#d32f2f' if e > top['economie_kwh_an'].quantile(0.66) else
                  '#f57c00' if e > top['economie_kwh_an'].quantile(0.33) else
                  '#ffd54f' for e in top['economie_kwh_an']]
        bars = ax.barh(top['id_batiment'], top['economie_kwh_an'] / 1000,
                       color=colors, edgecolor='white', height=0.6)
        for bar, (_, row) in zip(bars, top.iterrows()):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                    f"{row['economie_kwh_an']/1000:.0f} MWh/an\n({row['economie_euro_an']:,.0f} €)",
                    va='center', fontsize=9)
        ax.set_xlabel('Économie potentielle annuelle (MWh)', fontsize=12)
        ax.set_title(f'Top 10 bâtiments — Potentiel d\'économie\n(cible : {top["target_ipe"].iloc[0]:.0f} kWh/m²/an)',
                     fontsize=13, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        return self._save(fig, 'fig6_potentiel_economies.png')

    # ------------------------------------------------------------------ #
    # Figure 7 : Répartition DPE (donut)
    # ------------------------------------------------------------------ #

    def plot_dpe_distribution(self, buildings_df):
        counts = buildings_df['etiquette_dpe'].value_counts()
        counts = counts.reindex([d for d in DPE_ORDER if d in counts.index])
        colors = [DPE_COLORS[d] for d in counts.index]
        fig, ax = plt.subplots(figsize=(8, 8))
        wedges, texts, autotexts = ax.pie(
            counts.values, labels=counts.index, colors=colors,
            autopct='%1.0f%%', startangle=90,
            wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2),
            textprops=dict(fontsize=13)
        )
        for at in autotexts:
            at.set_fontsize(11)
            at.set_fontweight('bold')
        ax.set_title('Répartition du parc par étiquette DPE\n(20 bâtiments)',
                     fontsize=14, fontweight='bold')
        patches = [mpatches.Patch(color=DPE_COLORS[d], label=f'DPE {d}')
                   for d in counts.index]
        ax.legend(handles=patches, loc='lower right', fontsize=10)
        return self._save(fig, 'fig7_repartition_dpe.png')

    # ------------------------------------------------------------------ #
    # Figure 8 : Avant / Après rénovation
    # ------------------------------------------------------------------ #

    def plot_renovation_impact(self, impact_df):
        if impact_df.empty:
            print("Aucun bâtiment rénové dans le dataset.")
            return None
        fig, ax = plt.subplots(figsize=(9, 5))
        x = np.arange(len(impact_df))
        w = 0.35
        bars_avant = ax.bar(x - w/2, impact_df.get('Avant', [0]*len(impact_df)),
                            width=w, label='Avant rénovation', color='#E53935', alpha=0.85)
        bars_apres = ax.bar(x + w/2, impact_df.get('Après', [0]*len(impact_df)),
                            width=w, label='Après rénovation', color='#43A047', alpha=0.85)
        ax.set_xticks(x)
        ax.set_xticklabels(impact_df.index, fontsize=11)
        ax.set_ylabel('IPE moyen (kWh/m²/an)', fontsize=12)
        ax.set_title('Impact des rénovations sur l\'IPE', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(axis='y', alpha=0.3)
        if 'gain_pct' in impact_df.columns:
            for i, (idx, row) in enumerate(impact_df.iterrows()):
                if pd.notna(row.get('gain_pct')):
                    ax.text(i, max(row.get('Avant', 0), row.get('Après', 0)) + 2,
                            f"-{row['gain_pct']:.1f}%", ha='center', fontsize=10,
                            color='darkgreen', fontweight='bold')
        plt.tight_layout()
        return self._save(fig, 'fig8_impact_renovation.png')
