import pandas as pd
from sklearn.model_selection import train_test_split

def load_and_preprocess(filepath):
    """
    Loads data, drops ID, encodes categoricals, and splits data.
    """
    df = pd.read_csv(filepath)
    
    if 'Property_ID' in df.columns:
        df = df.drop('Property_ID', axis=1)
        
    df_encoded = pd.get_dummies(df, columns=['Location', 'Property_Type'], drop_first=True)
    
    X = df_encoded.drop('Price', axis=1)
    y = df_encoded['Price']
    
    return train_test_split(X, y, test_size=0.2, random_state=42)