import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error


class EnergyAnalyzer:
    """Analyse de l'efficacité énergétique des bâtiments."""

    DPE_THRESHOLDS = {'A': 50, 'B': 90, 'C': 150, 'D': 230, 'E': 330, 'F': 450}
    DPE_ORDER = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    DJU_REFERENCE = 2400  # DJU annuel de référence climatique France

    def __init__(self, buildings_df, consumption_df, meteo_df=None):
        self.buildings = buildings_df.copy()
        self.consumption = consumption_df.copy()
        self.meteo = meteo_df.copy() if meteo_df is not None else None
        self._annual = None
        self._enriched = None

    # ------------------------------------------------------------------ #
    # 1. Agrégation annuelle et calcul IPE
    # ------------------------------------------------------------------ #

    def compute_annual_ipe(self):
        """Agrège la consommation par bâtiment/année et calcule kWh/m²/an."""
        annual = (
            self.consumption
            .groupby(['id_batiment', 'annee'])
            .agg(
                conso_elec_kwh=('consommation_elec_kwh', 'sum'),
                conso_gaz_kwh=('consommation_gaz_kwh', 'sum'),
                conso_totale_kwh=('consommation_totale_kwh', 'sum'),
                dju_annuel=('dju_chauffage', 'sum'),
            )
            .reset_index()
        )
        annual = annual.merge(
            self.buildings[['id_batiment', 'surface_m2', 'etiquette_dpe',
                             'type_usage', 'type_chauffage', 'isolation',
                             'annee_construction', 'renovation_realisee',
                             'annee_renovation', 'ville', 'region']],
            on='id_batiment', how='left'
        )
        annual['ipe_kwh_m2'] = annual['conso_totale_kwh'] / annual['surface_m2']
        annual['ipe_normalise'] = annual.apply(
            lambda r: r['ipe_kwh_m2'] * (self.DJU_REFERENCE / r['dju_annuel'])
            if r['dju_annuel'] > 0 else r['ipe_kwh_m2'],
            axis=1
        )
        self._annual = annual
        return annual

    def get_annual(self):
        if self._annual is None:
            self.compute_annual_ipe()
        return self._annual

    # ------------------------------------------------------------------ #
    # 2. Détection des bâtiments énergivores (IQR)
    # ------------------------------------------------------------------ #

    def detect_high_consumers(self, column='ipe_kwh_m2', factor=1.5):
        """Retourne les bâtiments dont l'IPE dépasse Q3 + factor*IQR."""
        df = self.get_annual()
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        threshold = q3 + factor * iqr
        outliers = df[df[column] > threshold].copy()
        outliers['borne_haute_iqr'] = threshold
        outliers['ecart_borne'] = outliers[column] - threshold
        return outliers.sort_values(column, ascending=False)

    # ------------------------------------------------------------------ #
    # 3. Segmentation par DPE et type d'usage
    # ------------------------------------------------------------------ #

    def segment_by_dpe(self):
        """Statistiques IPE moyen par étiquette DPE."""
        df = self.get_annual()
        seg = (
            df.groupby('etiquette_dpe')['ipe_kwh_m2']
            .agg(['mean', 'median', 'std', 'count'])
            .rename(columns={'mean': 'ipe_moyen', 'median': 'ipe_median',
                             'std': 'ipe_ecart_type', 'count': 'nb_observations'})
            .reindex([d for d in self.DPE_ORDER if d in df['etiquette_dpe'].unique()])
        )
        return seg

    def segment_by_type(self):
        """Statistiques IPE moyen par type d'usage."""
        df = self.get_annual()
        return (
            df.groupby('type_usage')['ipe_kwh_m2']
            .agg(['mean', 'median', 'std', 'count'])
            .rename(columns={'mean': 'ipe_moyen', 'median': 'ipe_median',
                             'std': 'ipe_ecart_type', 'count': 'nb_observations'})
            .sort_values('ipe_moyen', ascending=False)
        )

    # ------------------------------------------------------------------ #
    # 4. Régression linéaire : consommation ~ facteurs
    # ------------------------------------------------------------------ #

    def run_regression(self):
        """
        Régression : IPE ~ surface + ancienneté + DJU + type_usage + isolation.
        Retourne un dict avec le modèle, les coefs et les métriques.
        """
        df = self.get_annual().dropna(subset=['ipe_kwh_m2'])

        df = df.copy()
        df['anciennete'] = df['annee'].astype(int) - df['annee_construction']

        le_type = LabelEncoder()
        le_iso = LabelEncoder()
        df['type_enc'] = le_type.fit_transform(df['type_usage'])
        df['iso_enc'] = le_iso.fit_transform(df['isolation'])

        features = ['surface_m2', 'anciennete', 'dju_annuel', 'type_enc', 'iso_enc']
        X = df[features].values
        y = df['ipe_kwh_m2'].values

        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)

        return {
            'model': model,
            'features': features,
            'r2': r2_score(y, y_pred),
            'mae': mean_absolute_error(y, y_pred),
            'coefficients': dict(zip(features, model.coef_)),
            'intercept': model.intercept_,
            'label_encoders': {'type_usage': le_type, 'isolation': le_iso},
            'df_used': df,
        }

    # ------------------------------------------------------------------ #
    # 5. Analyse avant/après rénovation
    # ------------------------------------------------------------------ #

    def renovation_impact(self):
        """Compare l'IPE avant et après rénovation pour les bâtiments rénovés."""
        df = self.get_annual()
        renovated = self.buildings[self.buildings['renovation_realisee'] == 1][
            ['id_batiment', 'annee_renovation']
        ]
        if renovated.empty:
            return pd.DataFrame()

        df = df.merge(renovated, on='id_batiment', how='inner')
        df['periode'] = df.apply(
            lambda r: 'Avant' if r['annee'] < r['annee_renovation'] else 'Après',
            axis=1
        )
        impact = (
            df.groupby(['id_batiment', 'periode'])['ipe_kwh_m2']
            .mean()
            .unstack('periode')
            .assign(gain_kwh_m2=lambda x: x.get('Avant', 0) - x.get('Après', 0))
            .assign(gain_pct=lambda x: (x['gain_kwh_m2'] / x.get('Avant', 1)) * 100)
        )
        return impact

    # ------------------------------------------------------------------ #
    # 6. Corrélation consommation / température
    # ------------------------------------------------------------------ #

    def temperature_correlation(self):
        """Corrélation mensuelle entre consommation et température/DJU."""
        cols = ['id_batiment', 'annee', 'mois',
                'consommation_totale_kwh', 'temperature_moy_c', 'dju_chauffage']
        df = self.consumption[cols].merge(
            self.buildings[['id_batiment', 'surface_m2']], on='id_batiment'
        )
        df['conso_m2'] = df['consommation_totale_kwh'] / df['surface_m2']
        corr_temp = df[['conso_m2', 'temperature_moy_c', 'dju_chauffage']].corr()
        return corr_temp

    # ------------------------------------------------------------------ #
    # 7. Potentiel d'économie
    # ------------------------------------------------------------------ #

    def savings_potential(self, target_ipe=None):
        """
        Estime l'économie annuelle possible si chaque bâtiment atteignait
        la cible IPE (par défaut : médiane du parc).
        """
        df = (
            self.get_annual()
            .groupby('id_batiment')['ipe_kwh_m2']
            .mean()
            .reset_index()
            .rename(columns={'ipe_kwh_m2': 'ipe_moyen'})
        )
        df = df.merge(self.buildings[['id_batiment', 'surface_m2']], on='id_batiment')

        if target_ipe is None:
            target_ipe = df['ipe_moyen'].median()

        df['ecart_cible'] = (df['ipe_moyen'] - target_ipe).clip(lower=0)
        df['economie_kwh_an'] = df['ecart_cible'] * df['surface_m2']
        df['economie_euro_an'] = df['economie_kwh_an'] * 0.12  # tarif moyen 0,12 €/kWh
        df['target_ipe'] = target_ipe
        return df.sort_values('economie_kwh_an', ascending=False)

    # ------------------------------------------------------------------ #
    # 8. Rapport de synthèse
    # ------------------------------------------------------------------ #

    def summary_report(self):
        """Retourne un dictionnaire de métriques clés du parc."""
        df = self.get_annual()
        report = {
            'nb_batiments': self.buildings['id_batiment'].nunique(),
            'nb_annees': df['annee'].nunique(),
            'surface_totale_m2': self.buildings['surface_m2'].sum(),
            'conso_totale_kwh': df.groupby('annee')['conso_totale_kwh'].sum().to_dict(),
            'ipe_moyen_parc': round(df['ipe_kwh_m2'].mean(), 1),
            'ipe_median_parc': round(df['ipe_kwh_m2'].median(), 1),
            'ipe_min': round(df['ipe_kwh_m2'].min(), 1),
            'ipe_max': round(df['ipe_kwh_m2'].max(), 1),
            'batiment_plus_efficient': df.loc[df['ipe_kwh_m2'].idxmin(), 'id_batiment'],
            'batiment_moins_efficient': df.loc[df['ipe_kwh_m2'].idxmax(), 'id_batiment'],
            'repartition_dpe': self.buildings['etiquette_dpe'].value_counts().to_dict(),
            'nb_renovations': int(self.buildings['renovation_realisee'].sum()),
        }
        return report
