import os
import re
import torch
from transformers import AutoTokenizer

# Load Legal-BERT tokenizer
tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")

# Path to the folder containing filtered case files
filtered_cases_folder = "F:\\cyrusliute\\final\\finally\\filtered_cases"
output_folder = "F:\\tokenized"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Get a list of all text files in the filtered_cases folder
filtered_files = [f for f in os.listdir(filtered_cases_folder) if f.endswith(".txt")]

# Check if files exist
if not filtered_files:
    print("❌ No filtered case files found!")
    exit()

# Preprocessing function
def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = text.lower().strip()  # Convert to lowercase
    return text

# Process, tokenize, and save each case file
for filename in filtered_files:
    input_path = os.path.join(filtered_cases_folder, filename)
    output_path = os.path.join(output_folder, f"tok_{filename}")  # Save as tok_C1.txt, tok_C2.txt, etc.

    with open(input_path, "r", encoding="utf-8") as f:
        case_text = f.read()
    
    processed_text = preprocess_text(case_text)
    tokenized = tokenizer(processed_text, padding="max_length", truncation=True, return_tensors="pt")

    # Save tokenized data
    torch.save(tokenized, output_path)

    print(f"✅ Tokenized & Saved: {output_path}")

print(f"🎯 {len(filtered_files)} cases tokenized and saved successfully!")
