# Cipher Quest: The Data Mystery

This repository contains code and data utilities for working with crime datasets, focusing on data wrangling, feature engineering, and machine learning model building. The tools and scripts here are designed to help with dataset preparation, feature selection, and model evaluation.

---

## 🧩 Code & Notebook Explanations

### Data Preparation Scripts

- **`dataset_creator.py`**: Provides a GUI for selecting features and generating custom datasets. Useful for creating datasets with required and optional features.
- **`dada_shuffler.py`**: Randomly shuffles the rows of a CSV file to anonymize or randomize the data order.
- **`noise_adder.py`**: Generates synthetic homicide records with realistic but noisy values for various features, simulating real-world data imperfections.
- **`null adder.py`**: Adds random null values to a dataset, with the ability to protect certain columns from being nullified. Useful for testing missing data handling.
- **`outlier_adder.py`**: Injects outliers into numerical and categorical fields to challenge model robustness.
- **`outlier_detector.py`**: Detects outliers in numeric columns using the Interquartile Range (IQR) method and prints them for review.

### Notebooks

- **`homicide-feature-selection-notebook.ipynb`**: Analyzes the homicide dataset to identify the 15 most important features using various feature selection techniques.
- **`ml-model-all-features.ipynb`**: Implements and compares multiple machine learning models using all available features in the dataset.
- **`ml-model-excluding-top-features.ipynb`**: Similar to the above, but excludes the top 15 features to test model performance with less informative data.

### Data & Feature Documentation

- **`features.txt`**: Detailed documentation of all features in the dataset, including their types and descriptions. Essential for understanding the data columns and their meanings.
- **`top15_feature_importance.png`**: Visualization of the most important features as determined by feature selection analysis.

### Datasets

- **`Shuffled Datasets/`**: Contains shuffled versions of the main datasets and test data for model evaluation.
    - `Crime Data Prototype-2 (shuffled).csv`: Shuffled main dataset.
    - `Testing Data 20k.csv`: Test dataset for model evaluation.
- **`Normal Datasets/`**: Contains the original and variant datasets, including:
    - `Crime Data Prototype-1 (with homicide).csv`: Original dataset with homicide data.
    - `Crime Data Prototype-2 (without homicide).csv`: Dataset variant without homicide data.
    - `Crime Data Prototype-3 (120k).csv`: Larger dataset variant.
- **`Round -1 Dataset/`**: Contains the dataset used for the first round.
    - `Round-1 Data.csv`: Dataset for initial analysis or modeling.

---

## 📊 Feature List (from `features.txt`)

- **Identifiers & Admin:** ID, CNTYFIPS, Ori, State, Agency, Agentype, Source
- **Case Details:** Solved, Year, Month, Incident, ActionType
- **Crime Classification:** Homicide, Situation
- **Victim Details:** VicAge, VicSex, VicRace, VicEthnic
- **Offender Details:** OffAge, OffSex, OffRace, OffEthnic
- **Weapon Used:** Weapon
- **Relationship:** Relationship
- **Circumstances:** Circumstance, Subcircum
- **Counts:** VicCount, OffCount
- **Miscellaneous:** FileDate, MSA

See the full `features.txt` for detailed descriptions.

---

