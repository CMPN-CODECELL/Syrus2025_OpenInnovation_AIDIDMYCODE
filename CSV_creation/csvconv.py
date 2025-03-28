import os
import pandas as pd

# Paths
tokenized_folder = "F:\\tokenized_cases"
csv_output_path = "F:\\newdata\\tokenized_data.csv"

# Prepare data storage
data = []

# Read tokenized files and save as CSV
for filename in os.listdir(tokenized_folder):
    if filename.endswith(".txt"):
        file_path = os.path.join(tokenized_folder, filename)
        
        with open(file_path, "r", encoding="utf-8") as file:
            tokenized_text = file.read().strip()  # Read and clean text
        
        data.append({"Filename": filename, "Tokenized_Text": tokenized_text})

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv(csv_output_path, index=False)

print(f"✅ CSV saved successfully at: {csv_output_path}")
