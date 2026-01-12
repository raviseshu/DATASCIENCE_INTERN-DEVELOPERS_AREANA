# Technical Report: House Price Prediction System

## 1. Introduction
This report documents the development of a regression model to predict residential property prices. The project utilized the `house_prices.csv` dataset containing 300 records.

## 2. Data Methodology
### 2.1 Data Description
* **Features:** Area (sq ft), Bedrooms, Bathrooms, Age, Location, Property Type.
* **Target:** Price.
* **Size:** 300 rows, 8 columns.

### 2.2 Preprocessing
* **Encoding:** Categorical variables (`Location`, `Property_Type`) were transformed using One-Hot Encoding (drop_first=True) to avoid multicollinearity.
* **Splitting:** Data was split into Training (80%) and Testing (20%) sets using a random seed of 42.

## 3. Exploratory Data Analysis (EDA)
* **Correlations:** Strong positive correlation (0.8+) observed between `Price` and `Area`.
* **Distributions:** Price follows a roughly normal distribution but with a right skew due to luxury properties.

## 4. Model Development
Two algorithms were tested:
1.  **Linear Regression:** Assumes a straight-line relationship.
2.  **Random Forest Regressor:** An ensemble method using decision trees to capture non-linearities.

## 5. Evaluation Results

| Metric | Linear Regression | Random Forest |
| :--- | :--- | :--- |
| **R² Score** | 0.9406 | **0.9711** |
| **MAE** | $2,188,736 | **$1,493,949** |
| **RMSE** | $2,907,633 | **$2,029,855** |

### 5.1 Interpretation
The Random Forest model reduced the Mean Absolute Error by approximately **32%** compared to Linear Regression. This suggests that the relationship between price and features like "Age" or "Location" is not strictly linear.

## 6. Feature Importance
Analysis of the Random Forest model revealed the following feature weights:
1.  **Area:** 69.3%
2.  **Location (Rural):** 20.1%
3.  **Location (Suburb):** 7.3%
4.  **Bedrooms:** 1.9%

## 7. Conclusion
The Random Forest model is the superior choice. It effectively captures the dominant impact of property size while nuancedly handling location-based price shifts.