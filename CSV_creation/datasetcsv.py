import os
import pandas as pd
import chardet  # Install with: pip install chardet

# Define paths
input_folder = "F:\\tokenized"  # Folder with tokenized files
output_csv = "F:\\dataset\\tokenized_data.csv"  # Output CSV file

# Ensure output folder exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# Prepare data storage
data = []

# Function to detect encoding
def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read(100000))  # Read first 100KB
    return result["encoding"]

# Read tokenized files
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        file_path = os.path.join(input_folder, filename)
        
        # Detect encoding
        encoding = detect_encoding(file_path)

        with open(file_path, "r", encoding=encoding, errors="replace") as file:
            tokens = file.read().strip().split()  # Read and split tokens

        # Append filename and tokenized text as a row
        data.append([filename, " ".join(tokens)])

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Filename", "Tokenized_Text"])

# Save to CSV
df.to_csv(output_csv, index=False, encoding="utf-8")

print(f"✅ Tokenized data saved to CSV: {output_csv}")
