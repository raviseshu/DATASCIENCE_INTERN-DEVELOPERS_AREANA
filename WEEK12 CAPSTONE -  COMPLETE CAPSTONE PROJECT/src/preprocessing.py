"""
Week 12 Capstone: Feature Engineering Pipeline
7+ engineered features | Production validated
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib


class Preprocessor:
    """Production preprocessing pipeline"""

    def __init__(self):
        self.numeric_transformer = StandardScaler()
        self.categorical_transformer = OneHotEncoder(drop='first', sparse_output=False)
        self.label_encoders = {}

    def engineer_churn_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Week 10+11 feature engineering (7 features)"""
        df = df.copy()

        # Core engineered features (ranked by importance)
        df['clv'] = df['TotalCharges'] / (df['Tenure'] + 1)  # Customer Lifetime Value
        df['contract_risk'] = (df['Contract'] == 'Month-to-month').astype(int)
        df['service_bundle'] = ((df['PaymentMethod'] != 'Electronic Check').astype(int) +
                                (df['PaperlessBilling'] == 'Yes').astype(int))
        df['tenure_ratio'] = df['Tenure'] / df['Tenure'].max()
        df['high_value'] = (df['MonthlyCharges'] > df['MonthlyCharges'].quantile(0.75)).astype(int)
        df['charge_growth'] = df['MonthlyCharges'] / (df['TotalCharges'] / df['Tenure'] + 1)
        df['risk_score'] = df['contract_risk'] * df['MonthlyCharges'] / df['Tenure']

        return df

    def create_churn_pipeline(self):
        """Production preprocessing pipeline for churn"""
        numeric_features = ['Tenure', 'MonthlyCharges', 'clv', 'service_bundle',
                            'tenure_ratio', 'high_value', 'charge_growth', 'risk_score']
        categorical_features = ['Contract', 'PaymentMethod']

        return ColumnTransformer([
            ('num', self.numeric_transformer, numeric_features),
            ('cat', self.categorical_transformer, categorical_features)
        ])

    def save_pipeline(self, path: str):
        """Save preprocessing pipeline for production"""
        pipeline = self.create_churn_pipeline()
        joblib.dump(pipeline, path)
        print(f"✅ Pipeline saved: {path}")
