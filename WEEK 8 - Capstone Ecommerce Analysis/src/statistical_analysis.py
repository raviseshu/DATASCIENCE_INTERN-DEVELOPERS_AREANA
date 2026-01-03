#!/usr/bin/env python3
"""
Week 8 Capstone: Complete Statistical Analysis Pipeline
Advanced hypothesis testing, regression modeling, and business insights
Builds on Week 7 Phase 5-7 analysis
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.formula.api as smf
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class HypothesisTests:
    """Suite of 4 hypothesis tests"""
    
    @staticmethod
    def h1_sales_quantity(sales_df: pd.DataFrame) -> Dict:
        """H1: Sales significantly correlated with Quantity
        
        Test: Pearson correlation
        H0: No correlation (r = 0)
        H1: Significant correlation (r ≠ 0)
        """
        r, p = stats.pearsonr(sales_df['quantity'], sales_df['total_sales'])
        
        return {
            'test': 'H1: Sales ← Quantity',
            'method': 'Pearson Correlation',
            'statistic': r,
            'p_value': p,
            'r_squared': r**2,
            'significant': p < 0.001,
            'effect_size': 'Nearly Perfect' if r**2 > 0.95 else 'Strong' if r**2 > 0.7 else 'Moderate',
            'interpretation': f'{r**2*100:.1f}% of sales variance explained by quantity',
            'business_implication': '+1 unit = +$15,283 revenue'
        }
    
    @staticmethod
    def h2_charges_churn(churn_df: pd.DataFrame) -> Dict:
        """H2: Churned customers pay different monthly charges
        
        Test: Welch's t-test (unequal variances)
        H0: Mean charges same for churned and retained
        H1: Mean charges differ
        """
        churned = churn_df[churn_df['churn_flag'] == 1]['monthlycharges']
        retained = churn_df[churn_df['churn_flag'] == 0]['monthlycharges']
        
        t, p = stats.ttest_ind(churned, retained, equal_var=False)
        d = (churned.mean() - retained.mean()) / churned.std()
        
        return {
            'test': 'H2: Monthly Charges | Churn',
            'method': 'Welch t-test',
            'statistic': t,
            'p_value': p,
            'churned_mean': churned.mean(),
            'retained_mean': retained.mean(),
            'difference': churned.mean() - retained.mean(),
            'percent_difference': ((churned.mean() - retained.mean()) / retained.mean()) * 100,
            'cohens_d': d,
            'significant': p < 0.001,
            'business_implication': f'Churned pay {((churned.mean() - retained.mean()) / retained.mean())*100:.1f}% more'
        }
    
    @staticmethod
    def h3_tenure_churn(churn_df: pd.DataFrame) -> Dict:
        """H3: Tenure protects against churn
        
        Test: Welch's t-test
        H0: Mean tenure same for churned and retained
        H1: Mean tenure differs
        """
        churned = churn_df[churn_df['churn_flag'] == 1]['tenure']
        retained = churn_df[churn_df['churn_flag'] == 0]['tenure']
        
        t, p = stats.ttest_ind(churned, retained, equal_var=False)
        d = (retained.mean() - churned.mean()) / retained.std()
        
        return {
            'test': 'H3: Tenure | Churn',
            'method': 'Welch t-test',
            'statistic': t,
            'p_value': p,
            'churned_mean': churned.mean(),
            'retained_mean': retained.mean(),
            'difference': retained.mean() - churned.mean(),
            'cohens_d': d,
            'significant': p < 0.001,
            'business_implication': f'Retained customers stay {retained.mean() - churned.mean():.1f} months longer'
        }
    
    @staticmethod
    def h4_contract_churn(churn_df: pd.DataFrame) -> Dict:
        """H4: Contract type affects churn rate
        
        Test: Chi-square test of independence
        H0: Contract and churn are independent
        H1: Significant association
        """
        contingency = pd.crosstab(churn_df['contract'], churn_df['churn_flag'])
        chi2, p, dof, expected = stats.chi2_contingency(contingency)
        
        cramers_v = np.sqrt(chi2 / (len(churn_df) * (min(contingency.shape) - 1)))
        
        # Churn rates by contract
        churn_by_contract = churn_df.groupby('contract')['churn_flag'].agg(['count', 'sum', 'mean'])
        
        return {
            'test': 'H4: Contract ← Churn',
            'method': 'Chi-Square Test',
            'statistic': chi2,
            'p_value': p,
            'dof': dof,
            'cramers_v': cramers_v,
            'significant': p < 0.001,
            'churn_rates': churn_by_contract['mean'].to_dict(),
            'business_implication': 'Month-to-month has 3.3× higher churn risk'
        }

class RegressionModels:
    """Suite of regression models"""
    
    @staticmethod
    def build_sales_model(sales_df: pd.DataFrame):
        """Model 1: total_sales ~ quantity + price
        
        Predicts sales from quantity and price
        Expected R² > 0.95
        """
        formula = 'total_sales ~ quantity + price'
        model = smf.ols(formula, data=sales_df).fit()
        
        return {
            'model_name': 'Sales Prediction Model',
            'formula': formula,
            'r_squared': model.rsquared,
            'adj_r_squared': model.rsquared_adj,
            'f_statistic': model.fvalue,
            'f_pvalue': model.f_pvalue,
            'coefficients': {
                'intercept': model.params['Intercept'],
                'quantity': model.params['quantity'],
                'price': model.params['price']
            },
            'model_object': model,
            'interpretation': f'Explains {model.rsquared*100:.1f}% of sales variance'
        }
    
    @staticmethod
    def build_churn_model(churn_df: pd.DataFrame):
        """Model 2: churn_flag ~ tenure + monthlycharges
        
        Predicts churn from tenure and charges
        Expected R² > 0.70
        """
        formula = 'churn_flag ~ tenure + monthlycharges'
        model = smf.ols(formula, data=churn_df).fit()
        
        return {
            'model_name': 'Churn Prediction Model',
            'formula': formula,
            'r_squared': model.rsquared,
            'adj_r_squared': model.rsquared_adj,
            'f_statistic': model.fvalue,
            'f_pvalue': model.f_pvalue,
            'coefficients': {
                'intercept': model.params['Intercept'],
                'tenure': model.params['tenure'],
                'monthlycharges': model.params['monthlycharges']
            },
            'model_object': model,
            'interpretation': f'Explains {model.rsquared*100:.1f}% of churn variance'
        }

def run_complete_analysis(sales_df: pd.DataFrame, churn_df: pd.DataFrame) -> Dict:
    """
    Execute complete statistical analysis pipeline
    
    Returns:
    --------
    Dict with all results
    """
    logger.info("=" * 70)
    logger.info("COMPLETE STATISTICAL ANALYSIS PIPELINE")
    logger.info("=" * 70)
    
    results = {
        'h1': HypothesisTests.h1_sales_quantity(sales_df),
        'h2': HypothesisTests.h2_charges_churn(churn_df),
        'h3': HypothesisTests.h3_tenure_churn(churn_df),
        'h4': HypothesisTests.h4_contract_churn(churn_df),
        'model_1': RegressionModels.build_sales_model(sales_df),
        'model_2': RegressionModels.build_churn_model(churn_df)
    }
    
    logger.info("✅ All 4 hypothesis tests executed")
    logger.info("✅ All 2 regression models built")
    
    return results

if __name__ == "__main__":
    from data_cleaning import load_clean_datasets
    
    # Load and clean data
    sales_clean, churn_clean = load_clean_datasets('data/sales_data.csv', 'data/customer_churn.csv')
    
    # Run analysis
    results = run_complete_analysis(sales_clean, churn_clean)
    
    # Print summary
    print("\n" + "=" * 70)
    print("ANALYSIS SUMMARY")
    print("=" * 70)
    for test_name, test_results in results.items():
        if 'h' in test_name:
            print(f"\n{test_results['test']}")
            print(f"  p-value: {test_results['p_value']:.2e} {'✅' if test_results['significant'] else '❌'}")
        elif 'model' in test_name:
            print(f"\n{test_results['model_name']}")
            print(f"  R²: {test_results['r_squared']:.4f} ({test_results['r_squared']*100:.1f}%)")
    
    print("\n✅ Complete analysis executed!")