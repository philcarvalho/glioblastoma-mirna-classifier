import pandas as pd
import os

folder = "data/4_biological_GSE90603/"

print("--- Peeking at GPL Annotation File ---")
try:
    # Find the annotation file (the text file that is NOT the series matrix)
    anno_file = None
    for f in os.listdir(folder):
        if f.endswith(".txt") and "series_matrix" not in f:
            anno_file = os.path.join(folder, f)
            break
            
    if not anno_file:
        print("❌ Could not find the annotation file. Make sure it is an unzipped .txt file!")
    else:
        print(f"Found annotation file: {os.path.basename(anno_file)}")
        
        # Read the file. GEO annotation tables sometimes start with comment lines (#)
        df_anno = pd.read_csv(anno_file, sep="\t", comment="#", low_memory=False)
        
        print(f"✅ Successfully loaded!")
        print(f"Shape: {df_anno.shape}")
        
        # Print all the column names so we can find the miRNA names
        print("\nAvailable Columns:")
        print(list(df_anno.columns))
        
        # Peek at the first row to see what the data looks like
        print("\nFirst Row of Data:")
        print(df_anno.iloc[0].to_dict())

except Exception as e:
    print(f"❌ Error: {e}")