import os
import torch
import chardet

# Define paths
tokenized_folder = "F:\\cyrtoken"  # Folder with tokenized cases
dataset_folder = "F:\\dataset"  # Folder to save processed dataset

# Ensure output folder exists
os.makedirs(dataset_folder, exist_ok=True)

# Function to detect file encoding
def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        raw_data = f.read(10000)  # Read first 10KB to detect encoding
        result = chardet.detect(raw_data)
        return result["encoding"]

# Process each tokenized file
for filename in os.listdir(tokenized_folder):
    if filename.endswith(".txt"):
        input_path = os.path.join(tokenized_folder, filename)
        output_path = os.path.join(dataset_folder, f"dataset_{filename}")

        # Detect encoding
        encoding = detect_encoding(input_path)

        # Read file with detected encoding
        with open(input_path, "r", encoding=encoding, errors="ignore") as file:
            tokens = file.read().strip().split()  # Read and split tokens

        # Convert tokens into PyTorch tensor
        token_tensor = torch.tensor([int(token) for token in tokens if token.isdigit()])

        # Save processed dataset
        torch.save(token_tensor, output_path)
        print(f"✅ Processed & Saved: {output_path}")

print(f"🎯 All tokenized cases have been successfully processed and saved!")
