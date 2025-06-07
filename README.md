# "Building Energy Savings Guide: Spotting Best Upgrade Opportunities"

![[Image_bfc2d7bfc2d7bfc2.jpg](attachment:Image_bfc2d7bfc2d7bfc2.jpg)](https://github.com/elvis07jr/cbecs-energy-efficiency-analyzer/blob/main/DATA/Image_bfc2d7bfc2d7bfc2.jpg)
## Project Overview

This project aims to leverage the U.S. Energy Information Administration's (EIA) Commercial Buildings Energy Consumption Survey (CBECS) 2018 dataset to identify commercial buildings with significant, targeted energy efficiency retrofit potential. Unlike traditional energy consumption prediction or general benchmarking, this project focuses on pinpointing specific end-uses (e.g., heating, cooling, lighting) where a building's energy consumption is disproportionately high compared to similar buildings, indicating a clear opportunity for specific interventions.

## Problem Statement

In order to determine where energy efficiency improvements are most needed, how can we use the CBECS dataset to identify commercial buildings that consume particularly high amounts of energy in particular areas (such as lighting, heating, or cooling) when compared to similar buildings?

## Motivation

Finding buildings that can increase their energy efficiency is essential for lowering overall energy use, operating expenses, and environmental effect. Present methods frequently concentrate on wide benchmarking or overall energy consumption intensity (EUI). A building may, however, have an average EUI but be extremely inefficient in one area (such as old lighting systems) and extremely efficient in another. By identifying particular areas of inefficiency, this research aims to deliver more detailed, actionable information that will enable more focused and successful retrofit efforts.

## My Dataset

I worked with the **Commercial Buildings Energy Consumption Survey (CBECS) 2018** dataset, which I obtained from the **U.S. Energy Information Administration (EIA)**. This was a comprehensive national survey where EIA collected detailed information on U.S. commercial buildings, including their energy use and associated costs. What was particularly useful for my project was that it provided energy consumption broken down by specific end-uses, such as heating, cooling, lighting, and refrigeration.

* **Name:** Commercial Buildings Energy Consumption Survey (CBECS) 2018
* **Source:** U.S. Energy Information Administration (EIA)
* **Description:** This dataset provided detailed information on the U.S. commercial building stock, covering energy use and expenditures, with breakdowns for various end-uses.
* **Availability:** I accessed it directly from the [EIA CBECS Data page](https://www.eia.gov/consumption/commercial/data/2018/).

## My Methodology (My High-Level Plan)

Here's how I approached this project, step-by-step:

1.  **Data Acquisition & Loading:** I started by downloading the CBECS 2018 public-use microdata file and loaded it into my analysis environment.
2.  **Exploratory Data Analysis (EDA):**
    * I spent time understanding the dataset's structure, the types of variables it contained, and the distribution of values.
    * I carefully identified and handled missing values, especially those represented by special codes like `-2` ('Not Applicable') and `-9` ('Don't Know'), converting them to standard `NaN` values.
3.  **Feature Engineering:** This was a crucial phase where I built the core components for my prediction:
    * I defined "peer groups" for buildings based on key shared characteristics, such as building type, climate zone, size range, and typical operating hours. This allowed for fair comparisons.
    * For each major energy end-use (like electricity for space heating (`BTUELSPH`), cooling (`BTUELCOL`), or lighting (`BTUELLGT`)), I calculated a "disproportionate consumption" metric. This involved things like comparing a building's end-use consumption to the median or mean of its defined peer group, or calculating a Z-score to see how much it deviated from the average. I also defined a threshold (e.g., if consumption was in the top 20% of its peer group).
    * Based on these metrics, I defined my **dependent variable (my target)**. I classified buildings into categories like "High Heating Efficiency Potential," "High Cooling Efficiency Potential," "High Lighting Efficiency Potential," or "Low Overall Efficiency Potential." I anticipated this would be set up as a multi-label classification problem, as a single building might have multiple areas of high potential.
4.  **Feature Selection:** I carefully selected the relevant independent variables (the features) that I believed would influence end-use consumption. These included details like building age, square footage, specific equipment types, climate data, weekly operating hours, and the principal building activity.
5.  **Model Selection:** I explored various machine learning classification models for this task. I considered options like Logistic Regression, Random Forest, and Gradient Boosting Machines (such as LightGBM or XGBoost).
    * I specifically considered multi-label classification approaches given that a single building might present several high-potential areas for improvement.
6.  **Model Training & Evaluation:**
    * I split my prepared data into training and testing sets to ensure my model learned from one part and was tested on unseen data.
    * I then trained the selected models on the training data.
    * Finally, I evaluated the models' performance using appropriate metrics like Precision, Recall, F1-score, and ROC-AUC for each specific end-use classification.
7.  **Interpretation & Insights:** After training and evaluating, I analyzed the model outputs to understand which specific building features or operational aspects were the strongest drivers of disproportionate consumption in each end-use. This was where I extracted actionable insights for targeted retrofits.

## Key Variables I Used (Examples)

Here are the main variables I focused on in my analysis:

* **My Target Variables (What I Predicted):**
    * `Heating_Retrofit_Potential` (e.g., indicating High or Low potential for heating upgrades)
    * `Cooling_Retrofit_Potential` (e.g., High or Low potential for cooling upgrades)
    * `Lighting_Retrofit_Potential` (e.g., High or Low potential for lighting upgrades)
    * *(These were derived from the original `BTUELSPH`, `BTUELCOL`, `BTUELLGT` values, compared to peer groups.)*
* **My Input Variables (The Building Features I Used to Predict):**
    * `PBA` (The building's main use, like an office or retail store)
    * `SQFT` (The total square footage of the building)
    * `YEARCON` (The year the building was constructed)
    * `WKHRS` (How many hours the building typically operates per week)
    * `EMP_TOT` (The total number of employees in the building)
    * `CDD65` / `HDD65` (Climate data: Cooling and Heating Degree Days for context)
    * `EQUIPM` (The main heating equipment type)
    * `ACEQUIPM` (The main cooling equipment type)
    * `LGTINLED` (Whether the building uses LED indoor lighting)
    * ...and many other structural and operational details available in the CBECS dataset.
