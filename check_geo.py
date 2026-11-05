import os
import pandas as pd
from io import StringIO

def parse_robust_geo_matrix(file_path):
    """Parses a GEO matrix by dynamically filtering out lines starting with '!'"""
    try:
        valid_lines = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                # Keep lines that DO NOT start with an exclamation mark metadata tag
                if not line.startswith("!") and line.strip():
                    valid_lines.append(line)
        
        # If we found no structural lines, return None
        if not valid_lines:
            print(f"❌ File appears empty or entirely metadata headers.")
            return None
            
        # Parse the cleaned lines directly into a DataFrame
        # The first non-metadata line contains our sample headers (ID_REF, GSMxxxx, ...)
        cleaned_data = "".join(valid_lines)
        df = pd.read_csv(StringIO(cleaned_data), sep="\t", index_col=0)
        
        return df
    except Exception as e:
        print(f"❌ Error parsing {os.path.basename(file_path)}: {e}")
        return None

def find_txt_files(folder_path):
    """Finds all .txt files in the target directory"""
    paths = []
    if os.path.exists(folder_path):
        for f in os.listdir(folder_path):
            if f.endswith(".txt"):
                paths.append(os.path.join(folder_path, f))
    return paths

# Map out your folder paths
folders = {
    "GSE122488 (Training)": "data/1_training_GSE122488/",
    "GSE184472 (Validation)": "data/2_validation_GSE184472/",
    "GSE90603 (Biological)": "data/4_biological_GSE90603/",
}

print("=== STARTING ROBUST GEO SANITY CHECK ===\n")

for label, folder in folders.items():
    print(f"--- Checking {label} ---")
    discovered_files = find_txt_files(folder)

    if discovered_files:
        for path in discovered_files:
            print(f"Found file: {os.path.basename(path)}")
            df = parse_robust_geo_matrix(path)
            if df is not None:
                print(f"✅ Successfully loaded matrix!")
                print(f"   Shape (miRNAs x Samples): {df.shape}")
                print(f"   First 5 miRNA names: {list(df.index[:5])}\n")
    else:
        print(f"❌ No .txt files discovered in folder: {folder}\n")