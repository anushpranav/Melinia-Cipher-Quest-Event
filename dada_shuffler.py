import csv
import random

# Define input and output file paths here
INPUT_CSV_PATH = "temp3.csv"  # Replace with your actual input file path
OUTPUT_CSV_PATH = "shuffled_output.csv"  # Name for your shuffled output file

def shuffle_csv(input_file, output_file):
    """
    Reads a CSV file, randomly shuffles all rows, and writes the shuffled data to a new CSV file.
    
    Args:
        input_file (str): Path to the input CSV file
        output_file (str): Path to save the shuffled output CSV file
    """
    # Read all rows from the input CSV file
    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Save the header row
        rows = list(reader)    # Read all data rows
    
    # Shuffle the rows randomly
    random.shuffle(rows)
    
    # Write the shuffled data to the output file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)  # Write the header row first
        writer.writerows(rows)   # Write all shuffled data rows
    
    print(f"Shuffled {len(rows)} rows from '{input_file}' to '{output_file}'")

# Set a random seed for reproducible results (optional)
# random.seed(42)

# Execute the shuffling function
if __name__ == "__main__":
    shuffle_csv(INPUT_CSV_PATH, OUTPUT_CSV_PATH)
    print(f"Shuffling complete! Shuffled data saved to {OUTPUT_CSV_PATH}")