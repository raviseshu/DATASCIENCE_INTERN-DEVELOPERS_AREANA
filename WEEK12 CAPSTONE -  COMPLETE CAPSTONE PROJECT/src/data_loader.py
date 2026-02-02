"""
Week 12 Capstone: Multi-Dataset Loader
Supports: customer_churn.csv[file:312], sales_data.csv[file:208], house_prices.csv[file:210]
"""
import pandas as pd
import numpy as np
import os
from typing import Dict, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """Production-ready data loader for all capstone datasets"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.cache = {}

    def load_churn(self, file_path: str = None) -> pd.DataFrame:
        """Load customer churn dataset [file:312] - 500 customers"""
        if file_path:
            df = pd.read_csv(file_path)
        else:
            df = pd.read_csv(os.path.join(self.data_dir, "customer_churn.csv"))

        # Data validation & cleaning
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
        logger.info(f"✅ Churn loaded: {df.shape} | Churn rate: {df['Churn'].mean():.1%}")
        return df

    def load_sales(self) -> pd.DataFrame:
        """Load sales dataset [file:208]"""
        df = pd.read_csv(os.path.join(self.data_dir, "sales_data.csv"))
        logger.info(f"✅ Sales loaded: {df.shape}")
        return df

    def load_house_prices(self) -> pd.DataFrame:
        """Load house prices [file:210]"""
        df = pd.read_csv(os.path.join(self.data_dir, "house_prices.csv"))
        logger.info(f"✅ House prices loaded: {df.shape}")
        return df

    def load_all(self) -> Dict[str, pd.DataFrame]:
        """Load all 3 capstone datasets"""
        datasets = {
            'churn': self.load_churn(),
            'sales': self.load_sales(),
            'house_prices': self.load_house_prices()
        }
        self.cache = datasets
        logger.info("✅ All datasets cached")
        return datasets

    def get_dataset_summary(self) -> pd.DataFrame:
        """Summary statistics for portfolio showcase"""
        summary = []
        for name, df in self.cache.items():
            summary.append({
                'dataset': name,
                'rows': df.shape[0],
                'columns': df.shape[1],
                'memory_mb': df.memory_usage(deep=True).sum() / 1024**2
            })
        return pd.DataFrame(summary)
