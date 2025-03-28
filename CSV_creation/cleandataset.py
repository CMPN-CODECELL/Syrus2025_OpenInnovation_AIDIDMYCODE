import pandas as pd
import re

# Load the CSV
df = pd.read_csv("F:\\newdata\\tokenized_data.csv")

# Function to clean the text
def clean_text(text):
    text = re.sub(r"=+", "", text)  # Remove "=" symbols
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    return text.strip()

# Apply cleaning function
df["Tokenized_Text"] = df["Tokenized_Text"].apply(clean_text)

# Save the cleaned data
df.to_csv("F:\\newdata\\cleaned_tokenized_data.csv", index=False)

print("✅ Cleaned data saved successfully!")
