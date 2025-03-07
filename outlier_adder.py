import pandas as pd
import numpy as np
import os
import random

def add_outliers_to_crime_data(input_file, output_file, outlier_percentage=0.05):
    """
    Add outliers to the crime dataset to reduce ML model accuracy.
    
    Parameters:
    - input_file: Path to the input CSV file
    - output_file: Path to save the output CSV file with outliers
    - outlier_percentage: Percentage of data points to convert to outliers (default: 5%)
    
    Returns:
    - DataFrame with added outliers
    """
    print(f"Loading crime dataset from {input_file}")
    # Load the dataset with proper quoting to handle complex fields
    df = pd.read_csv(input_file, quotechar='"', escapechar='\\')
    
    # Make a copy to avoid modifying the original DataFrame
    df_outliers = df.copy()
    
    # Calculate number of outliers to add
    n_rows = len(df)
    n_outliers = int(n_rows * outlier_percentage)
    print(f"Planning to add outliers to {n_outliers} rows out of {n_rows}")
    
    # Fields we can modify to create outliers
    numerical_fields = ['VicAge', 'OffAge']
    categorical_fields = ['VicSex', 'OffSex', 'VicRace', 'OffRace', 'Weapon', 'Relationship']
    
    # Track modifications for reporting
    modifications = {field: 0 for field in numerical_fields + categorical_fields}
    
    # 1. Add age outliers (extreme ages)
    outlier_indices = np.random.choice(df.index, size=n_outliers, replace=False)
    
    for idx in outlier_indices:
        # Select which field to modify
        field_to_modify = random.choice(numerical_fields + categorical_fields)
        
        if field_to_modify in numerical_fields:
            # Handle numerical fields - create extreme ages
            if field_to_modify == 'VicAge' or field_to_modify == 'OffAge':
                # Generate an extreme age (either very young or very old)
                if random.random() < 0.5:
                    # Very old (90-120 years)
                    outlier_value = random.randint(90, 120)
                else:
                    # Inappropriately young for crime data (8-12 years)
                    outlier_value = random.randint(8, 12)
                
                # Apply the outlier
                df_outliers.at[idx, field_to_modify] = outlier_value
                modifications[field_to_modify] += 1
        
        else:
            # Handle categorical fields - swap to unusual combinations
            if field_to_modify in ['VicSex', 'OffSex']:
                # Randomly assign unusual gender code
                unusual_sex = random.choice(['Unknown', 'Other'])
                df_outliers.at[idx, field_to_modify] = unusual_sex
                modifications[field_to_modify] += 1
            
            elif field_to_modify in ['VicRace', 'OffRace']:
                # Assign unusual race category
                unusual_race = random.choice(['Multi-racial', 'Pacific Islander', 'Other'])
                df_outliers.at[idx, field_to_modify] = unusual_race
                modifications[field_to_modify] += 1
            
            elif field_to_modify == 'Weapon':
                # Assign unusual weapon
                unusual_weapons = ['Poison', 'Explosives', 'Narcotics', 'Drowning', 'Advanced technology']
                df_outliers.at[idx, field_to_modify] = random.choice(unusual_weapons)
                modifications[field_to_modify] += 1
            
            elif field_to_modify == 'Relationship':
                # Assign unusual relationship
                unusual_relations = ['Unknown complex relationship', 'Multiple relationships', 'Time-traveler']
                df_outliers.at[idx, field_to_modify] = random.choice(unusual_relations)
                modifications[field_to_modify] += 1
    
    # 2. Create some unusually high VicCount and OffCount values
    high_count_indices = np.random.choice(df.index, size=int(n_outliers/4), replace=False)
    for idx in high_count_indices:
        # Very high victim or offender counts
        high_count = random.randint(10, 50)
        field = random.choice(['VicCount', 'OffCount'])
        df_outliers.at[idx, field] = high_count
        
        # Track this modification
        if field not in modifications:
            modifications[field] = 0
        modifications[field] += 1
    
    # 3. Change Years to create anachronistic entries
    year_outlier_indices = np.random.choice(df.index, size=int(n_outliers/4), replace=False)
    for idx in year_outlier_indices:
        # Either future years or very old years
        if random.random() < 0.5:
            future_year = random.randint(2025, 2050)
            df_outliers.at[idx, 'Year'] = future_year
        else:
            past_year = random.randint(1800, 1900)
            df_outliers.at[idx, 'Year'] = past_year
            
        # Track this modification
        if 'Year' not in modifications:
            modifications['Year'] = 0
        modifications['Year'] += 1
    
    # Save the modified DataFrame to new CSV
    df_outliers.to_csv(output_file, index=False, quoting=1)
    print(f"Dataset with outliers saved to {output_file}")
    
    # Report modifications
    print("\nOutlier modifications summary:")
    for field, count in modifications.items():
        print(f"- {field}: {count} outliers added")
    
    return df_outliers

# Example usage
if __name__ == "__main__":
    # Define input and output files
    input_file = "temp2.csv"  # Replace with your actual file
    output_file = "crime_dataset_with_outliers.csv"
    
    # Add outliers (adjust percentage as needed)
    modified_df = add_outliers_to_crime_data(
        input_file,
        output_file,
        outlier_percentage=0.2
    )
    
    # Display sample of modified data
    print("\nSample of data with outliers:")
    print(modified_df.sample(5))