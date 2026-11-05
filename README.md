\--- Listing files in folder ---

Found files: \['CGGA.microRNA\_array\_198\_clinical.20200506.txt', 'CGGA.microRNA\_array\_198\_gene\_level.20200506.txt']



\--- Loading Datasets ---

Successfully loaded Clinical data from: CGGA.microRNA\_array\_198\_clinical.20200506.txt

Successfully loaded Expression data from: CGGA.microRNA\_array\_198\_gene\_level.20200506.txt



\--- Checking miRNA Naming Format ---

First 5 miRNA names look like this: \['hsa-miR-199a-3p,hsa-miR-199b-3p', 'hsa-miR-320d,hsa-miR-320b,hsa-miR-320a,hsa-miR-320c', 'hsa-miR-502-3p,hsa-miR-500#', 'hsa-miR-516a-3p,hsa-miR-516b#', 'hsa-miR-517a,hsa-miR-517b']



\--- Checking ID Alignment ---

Samples in Expression file: 198

Samples in Clinical file: 198

Successfully matched IDs: 198



\--- Checking Clinical Columns for GBM ---

Here are the clinical columns available:

\['CGGA\_ID', 'PRS\_type', 'Histology', 'Grade', 'Gender', 'Age', 'OS', 'Censor (alive=0; dead=1)', 'Radio\_status (treated=1;un-treated=0)', 'Chemo\_status (TMZ treated=1;un-treated=0)', 'IDH\_mutation\_status', '1p19q\_codeletion\_status', 'MGMTp\_methylation\_status']



Unique values found in column 'Histology':

Histology

GBM     81

A       45

AA      23

O       13

AO      12

sGBM     6

AOA      5

rAA      5

rGBM     4

rAO      2

rA       1

OA       1

Name: count, dtype: int64



Unique values found in column 'Grade':

Grade

WHO IV     91

WHO II     60

WHO III    47

Name: count, dtype: int64

