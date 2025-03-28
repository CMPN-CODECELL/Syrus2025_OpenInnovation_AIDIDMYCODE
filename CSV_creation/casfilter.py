import os

# Directory where your case files are stored
case_dir = "F:\CYRUS\AILA\Object_casedocs"

# Directory to save filtered cases
filtered_cases_folder = "F:\\cyrusliute\\final\\finally\\filtered_cases"

# Keywords to filter relevant cases
keywords = ["false allegation", "wrongful conviction", "malicious prosecution", "false complaint"]

# Path to save the list of case numbers
case_numbers_path = "F:\\cyrusliute\\final\\finally\\caseno.txt"

# Ensure the filtered cases directory exists
os.makedirs(filtered_cases_folder, exist_ok=True)

# Open the case numbers file
with open(case_numbers_path, "w", encoding="utf-8") as case_file:
    for num in range(1, 3001):  # Processing C1 to C3000
        file_path = os.path.join(case_dir, f"C{num}.txt")
        
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                case_text = file.read().strip()  # Read and remove extra spaces
                
                # Check if any keyword is present in the case text
                if any(keyword in case_text.lower() for keyword in keywords):
                    # Define the output path for this specific case
                    filtered_case_path = os.path.join(filtered_cases_folder, f"C{num}_filtered.txt")

                    # Save the filtered case
                    with open(filtered_case_path, "w", encoding="utf-8") as filtered_file:
                        filtered_file.write(f"========== CASE C{num} ==========\n")
                        filtered_file.write(case_text)
                        filtered_file.write("\n" + "="*40 + "\n")

                    # Save only the case number
                    case_file.write(f"C{num}\n")

                    print(f"✅ Matched & Saved: {filtered_case_path}")
        
        except FileNotFoundError:
            print(f"⚠️ Warning: {file_path} not found. Skipping...")

print(f"\n✅ Filtering complete! Filtered cases saved in '{filtered_cases_folder}' and case numbers in '{case_numbers_path}'")
