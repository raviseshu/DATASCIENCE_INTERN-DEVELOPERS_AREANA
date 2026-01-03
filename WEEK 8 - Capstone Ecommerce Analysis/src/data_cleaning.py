#!/usr/bin/env python3
"""
Week 8 Capstone: Production Data Cleaning Pipeline
Handles sales_data.csv + customer_churn.csv automatically
Complete ETL with validation and quality checks
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_sales_data(filepath: str) -> pd.DataFrame:
    """
    Clean sales data with full validation
    
    Parameters:
    -----------
    filepath : str
        Path to raw sales CSV file
    
    Returns:
    --------
    pd.DataFrame
        Cleaned and validated sales data
    """
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Loaded {len(df)} raw sales records")
        
        # Standardize columns
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Parse dates (handles DD-MM-YYYY format)
        df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
        df['month'] = df['date'].dt.to_period('M').astype(str)
        df['year_month'] = df['date'].dt.to_period('M')
        
        # Numeric conversion with error handling
        numeric_cols = ['quantity', 'price', 'total_sales', 'totalsales']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove invalid records
        df_clean = df.dropna(subset=['date', 'quantity', 'price', 'total_sales'])
        
        # Validation checks
        valid_count = len(df_clean)
        total_count = len(df)
        retention_rate = (valid_count / total_count) * 100
        
        logger.info(f"✅ Sales cleaned: {valid_count}/{total_count} records ({retention_rate:.1f}% retained)")
        
        # Data quality metrics
        logger.info(f"   Mean Sales: ${df_clean['total_sales'].mean():,.0f}")
        logger.info(f"   Mean Quantity: {df_clean['quantity'].mean():.2f} units")
        
        return df_clean
        
    except Exception as e:
        logger.error(f"Error cleaning sales data: {e}")
        raise

def clean_churn_data(filepath: str) -> pd.DataFrame:
    """
    Clean churn data with full validation
    
    Parameters:
    -----------
    filepath : str
        Path to raw churn CSV file
    
    Returns:
    --------
    pd.DataFrame
        Cleaned and validated churn data
    """
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Loaded {len(df)} raw churn records")
        
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Binary churn flag
        if 'churn' in df.columns:
            df['churn_flag'] = df['churn'].map({'Yes': 1, 'No': 0}).fillna(0).astype(int)
        else:
            logger.warning("'churn' column not found")
        
        # Numeric conversion
        for col in ['tenure', 'monthlycharges', 'totalcharges']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Senior citizen flag
        if 'seniorcitizen' in df.columns:
            df['senior_flag'] = (df['seniorcitizen'] == 1).astype(int)
        
        # Remove invalid records
        df_clean = df.dropna(subset=['tenure', 'monthlycharges', 'churn_flag'])
        
        valid_count = len(df_clean)
        total_count = len(df)
        retention_rate = (valid_count / total_count) * 100
        
        logger.info(f"✅ Churn cleaned: {valid_count}/{total_count} records ({retention_rate:.1f}% retained)")
        
        # Churn rate
        churn_rate = df_clean['churn_flag'].mean()
        logger.info(f"   Churn Rate: {churn_rate*100:.1f}% ({df_clean['churn_flag'].sum()} churned)")
        logger.info(f"   Avg Tenure: {df_clean['tenure'].mean():.1f} months")
        
        return df_clean
        
    except Exception as e:
        logger.error(f"Error cleaning churn data: {e}")
        raise

def load_clean_datasets(sales_path: str, churn_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Main entry point - load and clean both datasets
    
    Parameters:
    -----------
    sales_path : str
        Path to sales data CSV
    churn_path : str
        Path to churn data CSV
    
    Returns:
    --------
    Tuple[pd.DataFrame, pd.DataFrame]
        Cleaned sales and churn dataframes
    """
    logger.info("=" * 60)
    logger.info("DATA CLEANING PIPELINE STARTING")
    logger.info("=" * 60)
    
    sales_clean = clean_sales_data(sales_path)
    churn_clean = clean_churn_data(churn_path)
    
    # Save cleaned versions
    sales_clean.to_csv('data/sales_data_clean.csv', index=False)
    churn_clean.to_csv('data/churn_data_clean.csv', index=False)
    logger.info("✅ Cleaned datasets saved to data/")
    
    logger.info("=" * 60)
    logger.info("DATA CLEANING COMPLETE")
    logger.info("=" * 60)
    
    return sales_clean, churn_clean

if __name__ == "__main__":
    # Usage example
    sales_clean, churn_clean = load_clean_datasets('data/sales_data.csv', 'data/customer_churn.csv')
    print("\n🎉 Data cleaning pipeline complete!")
    print(f"Sales: {len(sales_clean)} records")
    print(f"Churn: {len(churn_clean)} records")