import os

# Path to the directory containing case text files
case_dir = "F:\CYRUS\AILA\Object_casedocs"

# Dictionary to store case data
case_data = {}

# Iterate through files
for num in range(1, 3001):
    file_path = os.path.join(case_dir, f"C{num}.txt")
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            case_data[f"C{num}"] = file.read().lower()
        
        # Print progress every 100 cases
        if num % 100 == 0:
            print(f"Loaded {num} cases...")
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

print(f"✅ Successfully loaded {len(case_data)} cases!")
