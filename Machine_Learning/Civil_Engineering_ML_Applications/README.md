# Compilation of Machine Learning Projects for CIVL 4100R 🔍

### Context
This repository contains three machine learning projects undertaken as part of the **HKUST CIVL 4100R: Practical Machine Learning for Smart Infrastructure Systems** course. Each project applies advanced data analysis and machine learning techniques to solve domain-specific problems.

---

## Tools Used 🛠️
- **Programming Language**: Python
- **Libraries**: NumPy, Pandas, Scikit-learn, PyTorch, Matplotlib, Seaborn, TensorFlow
- **Visualization Tools**: Jupyter Notebook, Matplotlib, Seaborn

---

## Key Findings 💡
1. **User Thermal Preference Prediction:** Logistic regression models provided interpretable insights during EDA, while Random Forest slightly improved predictive accuracy.
2. **Binary Crack Detection:** Data augmentation significantly improved model performance, while overly aggressive regularization hindered accuracy.
3. **Electricity Demand Forecasting:** XGBoost demonstrated the highest accuracy, showcasing the strength of feature-based predictions.

---

## The 3 Key Takeaways 📊
1. Data preprocessing and feature engineering significantly impact model performance.
2. Hyperparameter tuning and model evaluation are critical steps to achieving high accuracy and robustness.
3. Combining domain knowledge with machine learning enhances problem-solving capabilities.

---

## Table of Contents

### Projects:
1. [User Thermal Preference Prediction](#1-user-thermal-preference-prediction)
2. [Binary Crack Detection Using ResNet-50](#2-binary-crack-detection-using-resnet-50)
3. [Electricity Demand Forecasting for Los Angeles](#3-electricity-demand-forecasting-for-los-angeles)

---

## Project Descriptions 🌐

### **1. User Thermal Preference Prediction**
This project predicts building occupants' thermal preferences to enhance indoor environmental comfort and energy efficiency. A major focus was on **Exploratory Data Analysis (EDA)** to understand relationships within the data and identify key factors influencing thermal comfort. The dataset includes features such as age, gender, season, air temperature, and relative humidity.

**Key Tasks:**
- **Exploratory Data Analysis (EDA):**
  - Visualized relationships between features and thermal preferences.
  - Discovered that air temperature had the most significant impact on thermal preference.
- **Model Development:**
  - Logistic Regression: Used for interpretable classification of preferences into "cooler," "warmer," or "no change."
  - Random Forest: Outperformed logistic regression in terms of accuracy.
- **Feature Importance Analysis:** Highlighted air temperature and gender as key factors influencing thermal preferences.

---

### **2. Binary Crack Detection Using ResNet-50**
This project utilizes a ResNet-50 model to classify images of concrete surfaces as "cracked" or "not cracked."

**Key Tasks:**
- **Data Augmentation:** Applied strategies like random flips, rotations, and transformations to improve model robustness.
- **Model Training:**
  - Used PyTorch to fine-tune a pre-trained ResNet-50 model.
  - Implemented hyperparameter tuning for learning rates and regularization parameters.
- **Evaluation and Insights:**
  - Compared the effects of different learning rates and epochs on model accuracy.
  - Explored the impact of augmentation strategies and regularization in mitigating overfitting.

---

### **3. Electricity Demand Forecasting for Los Angeles**
This project forecasts electricity demand in Los Angeles for the week ahead using historical data on electricity usage, temperature, and temporal features.

**Key Tasks:**
- **Exploratory Data Analysis (EDA):**
  - Investigated correlations between electricity demand, temperature, and temporal variables (weekends, holidays).
  - Noted a U-shaped relationship between demand and temperature.
- **Feature Engineering:**
  - Categorical variables were one-hot encoded.
  - Created a "season" feature to capture climatic trends.
- **Model Development and Comparison:**
  - **LSTM (Long Short-Term Memory Networks):** Captured temporal patterns.
  - **Prophet:** Time series forecasting.
  - **XGBoost:** Gradient boosting for feature-driven prediction.
- **Model Evaluation:** Compared performance using RMSE and CVRMSE.

---

### Author 👨‍🔬
- **Selim SHERIF**
