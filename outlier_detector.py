import pandas as pd

# Load dataset
df = pd.read_csv('Crime Data Prototype-1.csv')

# Select numeric columns
numeric_cols = ['VicAge', 'OffAge', 'OffCount', 'VicCount']

# Convert to numeric and handle errors
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert, setting non-numeric as NaN

# Drop NaN values to avoid issues
df_clean = df.dropna(subset=numeric_cols)

# Function to detect outliers using IQR
def detect_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data[column] < lower_bound) | (data[column] > upper_bound)]

# Check outliers for each numeric column
for col in numeric_cols:
    outliers = detect_outliers_iqr(df_clean, col)
    print(f"Outliers in {col}:\n", outliers)
