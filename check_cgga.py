import os
import pandas as pd

# Define the folder path
folder_path = "data/3_external_CGGA198/"

print("--- Listing files in folder ---")
if os.path.exists(folder_path):
    files = os.listdir(folder_path)
    print(f"Found files: {files}\n")
else:
    print(f"Error: Folder '{folder_path}' does not exist!\n")
    files = []

# Try to automatically assign clinical and expression files based on keywords
clinical_path = None
expr_path = None

for f in files:
    if "clinical" in f.lower():
        clinical_path = os.path.join(folder_path, f)
    elif "expr" in f.lower() or "microrna" in f.lower():
        # Make sure it's not a probe file if you happened to download it
        if "probe" not in f.lower():
            expr_path = os.path.join(folder_path, f)

print("--- Loading Datasets ---")
df_clinical = None
df_expr = None

# Load Clinical Data
if clinical_path:
    try:
        # CGGA files are usually tab-separated (\t) or comma-separated
        df_clinical = pd.read_csv(clinical_path, sep=None, engine='python')
        print(f"Successfully loaded Clinical data from: {os.path.basename(clinical_path)}")
    except Exception as e:
        print(f"Error loading Clinical file: {e}")
else:
    print("Could not find a file with 'clinical' in the name.")

# Load Expression Data
if expr_path:
    try:
        df_expr = pd.read_csv(expr_path, sep=None, engine='python', index_col=0)
        print(f"Successfully loaded Expression data from: {os.path.basename(expr_path)}\n")
    except Exception as e:
        print(f"Error loading Expression file: {e}\n")
else:
    print("Could not find a file with 'expr' or 'microRNA' in the name.\n")

# Run analysis only if both files loaded successfully
if df_clinical is not None and df_expr is not None:
    
    # 2. Check miRNA Naming Format
    print("--- Checking miRNA Naming Format ---")
    mirna_names = list(df_expr.index[:5])
    print(f"First 5 miRNA names look like this: {mirna_names}\n")

    # 3. Check ID Alignment
    print("--- Checking ID Alignment ---")
    expr_sample_ids = set(df_expr.columns)
    clinical_sample_ids = set(df_clinical.iloc[:, 0]) 

    matching_ids = expr_sample_ids.intersection(clinical_sample_ids)
    print(f"Samples in Expression file: {len(expr_sample_ids)}")
    print(f"Samples in Clinical file: {len(clinical_sample_ids)}")
    print(f"Successfully matched IDs: {len(matching_ids)}\n")

    # 4. Check Glioblastoma Labels
    print("--- Checking Clinical Columns for GBM ---")
    print("Here are the clinical columns available:")
    print(list(df_clinical.columns))

    possible_columns = ['Histology', 'Grade', 'WHO_Grade', 'histology', 'grade']
    for col in df_clinical.columns:
        if col in possible_columns:
            print(f"\nUnique values found in column '{col}':")
            print(df_clinical[col].value_counts())
else:
    print("❌ Data check skipped because one or both files failed to load.")
    print("Please verify your file names inside data/3_external_CGGA198/")