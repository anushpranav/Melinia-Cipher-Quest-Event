import pandas as pd
import numpy as np
import random
#null adder code
def add_random_nulls(input_csv_path, output_csv_path, num_rows, protected_columns, null_percentage):
    """
    Add random null values to a CSV dataset while protecting specified columns.
    
    Parameters:
    input_csv_path (str): Path to the input CSV file
    output_csv_path (str): Path to save the output CSV file
    num_rows (int): Number of rows to include from the dataset
    protected_columns (list): List of column names that should not contain null values
    null_percentage (float): Percentage of cells to replace with null values (default: 5%)
    
    Returns:
    None
    """
    # Read the CSV file
    df = pd.read_csv(input_csv_path)
    
    # Select only the first num_rows rows
    if num_rows < len(df):
        df = df.iloc[:num_rows]
    else:
        print(f"Warning: Requested {num_rows} rows but dataset only has {len(df)} rows.")
        num_rows = len(df)
    
    # Verify protected columns exist in the dataset
    for col in protected_columns:
        if col not in df.columns:
            print(f"Warning: Protected column '{col}' not found in the dataset.")
    
    # Get columns that can have null values
    eligible_columns = [col for col in df.columns if col not in protected_columns]
    
    if not eligible_columns:
        print("Error: No eligible columns for adding null values after excluding protected columns.")
        return
    
    # Calculate total eligible cells
    total_eligible_cells = num_rows * len(eligible_columns)
    
    # Calculate how many cells to convert to null
    num_nulls = int(total_eligible_cells * null_percentage)
    
    # Generate random indices for null values
    nulls_added = 0
    while nulls_added < num_nulls:
        row_idx = random.randint(0, num_rows - 1)
        col_name = random.choice(eligible_columns)
        
        # Skip if already null
        if pd.isna(df.loc[row_idx, col_name]):
            continue
            
        # Add null value
        df.loc[row_idx, col_name] = np.nan
        nulls_added += 1
    
    # Save the modified dataset
    df.to_csv(output_csv_path, index=False)
    
    # Print summary
    print(f"Created new CSV file with {num_rows} rows and {nulls_added} null values.")
    print(f"Protected columns that remained intact: {', '.join(protected_columns)}")
    print(f"Output saved to: {output_csv_path}")

# Example usage
if __name__ == "__main__":
    # Update these paths and parameters as needed
    input_csv_path = "temp.csv"  # Replace with your input file path
    output_csv_path = "output_data_with_nulls.csv"
    rows_to_include = 20000
    
    # Columns that should not contain null values
    protected_columns = ['ID', 'CNTYFIPS', 'Ori', 'Solved']
    
    null_percentage = 0.10
    
    add_random_nulls(
        input_csv_path=input_csv_path,
        output_csv_path=output_csv_path,
        num_rows=rows_to_include,
        protected_columns=protected_columns,
        null_percentage=null_percentage
    )