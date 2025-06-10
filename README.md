# "Building Energy Savings Guide: Spotting Best Upgrade Opportunities"
# Phase 3 Machine Learning Project
![[Image_bfc2d7bfc2d7bfc2.jpg](attachment:Image_bfc2d7bfc2d7bfc2.jpg)](https://github.com/elvis07jr/cbecs-energy-efficiency-analyzer/blob/main/DATA/Image_bfc2d7bfc2d7bfc2.jpg)
## Business Understanding

### Stakeholder:
Energy Efficiency Program Managers / Building Owners

### Business Problem:
To identify commercial buildings with unusually high heating energy consumption compared to similar buildings, thereby pinpointing optimal targets for energy efficiency retrofits. The goal is to provide actionable insights for focused interventions to reduce energy use, operating expenses, and environmental impact.

### Dataset:
U.S. Energy Information Administration's (EIA) Commercial Buildings Energy Consumption Survey (CBECS) 2018 public-use microdata.

---

## Data Understanding

### Initial Exploration:
Initial data exploration involved loading the dataset, inspecting its structure, and identifying special codes (-2, -9) representing missing or suppressed values.

### Data Cleaning:
Special codes for missing values were replaced with `np.nan`. Targeted imputation was performed for `RENOV` and `BASEMNT` columns, handling string 'nan' and `np.nan` values by replacing them with 'UNKNOWN_CATEGORY'.

### Feature Engineering:
- Calculated `TOTAL_BTU` for various end-uses (e.g., heating, cooling).
- Defined peer groups for buildings based on `PBA` (Principal Building Activity), `PUBCLIM` (Public Climate Region), and `SQFT_BINNED` (binned Square Footage).
- Calculated peer group medians and standard deviations for energy consumption.
- Created the target variable `HIGH_HEATING_POTENTIAL` based on a building's heating consumption exceeding peer group thresholds (ratio and Z-score).
- Mapped `PBA` numerical codes to descriptive string labels for better interpretability.

---

## Data Preparation

### Train-Test Split:
The dataset was split into training and testing sets (`X_scaled` and `y['HIGH_HEATING_POTENTIAL']`) using `train_test_split` with an 80/20 ratio and stratification to maintain class distribution.

### Scaling:
Numerical features were scaled using `StandardScaler` to ensure they contribute equally to the model.

### Preventing Data Leakage:
- SMOTE (Synthetic Minority Over-sampling Technique) was applied only to the training data (`X_train_resampled`, `y_train_resampled`) to address class imbalance for the `HIGH_HEATING_POTENTIAL` target, preventing data leakage from the test set.
- Categorical features were one-hot encoded using `pd.get_dummies` after handling missing values.
- Features were selected based on prior feature importance analysis to streamline the dataset.

---

## Modeling

For this project, a Decision Tree Classifier was chosen as the model type. Key metrics used for evaluation included Accuracy, Precision, Recall, F1-score, and ROC AUC Score for both the training and test sets. The model was trained with specific hyperparameters (`max_depth=8`, `min_samples_leaf=20`, `random_state=42`) after applying SMOTE to the training data. The classification report provides detailed precision, recall, and F1-scores for both classes, while the test set's ROC AUC score (typically observed around 0.78) indicates the model's ability to distinguish between high and low heating potential buildings is better than random, with the train ROC AUC also reported to check for potential overfitting.

---

## Evaluation

### Model Performance:
The Decision Tree Classifier's performance is evaluated using:
- **Classification Report**: Provides precision, recall, f1-score, and support for class 0 (No Potential) and class 1 (High Potential).
- **ROC Curve and AUC Score**: Visualizes the trade-off between True Positive Rate and False Positive Rate.
- **Confusion Matrix**: Shows the counts of True Positives, True Negatives, False Positives, and False Negatives.

### Visualizations:
- **ROC Curve**: Plots the classifier's performance against a random classifier.
- **Confusion Matrix**: Clearly shows the model's prediction accuracy and types of errors (false positives and false negatives).
- **Decision Tree Diagram**: A simplified visual representation of the trained Decision Tree, showing key splits and decision rules.

---

## Conclusion

### Recommendations:
- **Prioritized Outreach**: Use model predictions to target high-potential buildings for retrofits first, maximizing ROI.
- **Tailored Solutions**: Follow up with targeted energy audits based on model insights (e.g., roof/wall construction) to propose precise solutions.
- **Data-Driven Decisions**: Leverage the model for informed investment decisions and to demonstrate tangible energy savings.
- **Addressing Missed Opportunities**: Explore strategies to reduce false negatives in future model iterations to capture more high-value targets.
- **Long-Term Strategy**: Integrate this model as a foundational element for continuous energy management and carbon footprint reduction.

### Next Steps:
- Implement systematic hyperparameter tuning (e.g., `GridSearchCV`) to find optimal model parameters.
- Employ cross-validation for more robust model evaluation and to reduce bias.
- Explore other classification algorithms (e.g., Gradient Boosting, SVM) and ensemble methods.
- Investigate the specific impact of each one-hot encoded feature on predictions (e.g., specific `PBA` types).
- Develop a user-friendly interface for building energy managers to input data and receive predictions.

---

## Contacts

- **Name**: Elvis Tile
- **Email**: [Email](tile.pc@hotmail.com)
- **LinkedIn**: [[LinkedIn](https://www.linkedin.com/in/elvis-kiprono-0617747b/)]
- **GitHub**: [[GitHub](https://github.com/elvis07jr)]
