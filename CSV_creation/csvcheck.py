import os

# Define paths
input_folder = r"F:\cyrusliute\final\finally\filtered_cases"
output_folder = r"F:\PREPRO"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Process each file
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        with open(input_path, "r", encoding="utf-8", errors="ignore") as file:
            text = file.read()

        # Basic text cleanup (Remove extra spaces, special characters, etc.)
        cleaned_text = " ".join(text.split())

        # Save preprocessed text
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(cleaned_text)

        print(f"✅ Preprocessed & Saved: {output_path}")
