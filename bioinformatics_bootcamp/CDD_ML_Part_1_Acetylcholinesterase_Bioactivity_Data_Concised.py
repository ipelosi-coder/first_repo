#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Bioinformatics Project - CDD Part 1
# Cleaned Python script for Storm

import pandas as pd
from chembl_webresource_client.new_client import new_client
import subprocess  # optional, for shell commands

# ----------------------
# Search for Target protein
# ----------------------
target = new_client.target
target_query = target.search('acetylcholinesterase')
targets = pd.DataFrame.from_dict(target_query)
print(targets)

# ----------------------
# Select target and retrieve bioactivity data
# ----------------------
selected_target = targets.target_chembl_id[0]
print(f"Selected target: {selected_target}")

activity = new_client.activity
res = activity.filter(target_chembl_id=selected_target).filter(standard_type="IC50")
df = pd.DataFrame.from_dict(res)
print(df.head())

# Save raw data
df.to_csv('acetylcholinesterase_01_bioactivity_data_raw.csv', index=False)
print("Saved raw data to 'acetylcholinesterase_01_bioactivity_data_raw.csv'")

# ----------------------
# Handle missing data
# ----------------------
df2 = df[df.standard_value.notna()]
df2 = df2[df.canonical_smiles.notna()]
df2_nr = df2.drop_duplicates(['canonical_smiles'])
print(f"Number of unique molecules: {len(df2_nr.canonical_smiles.unique())}")

# ----------------------
# Data pre-processing
# ----------------------
selection = ['molecule_chembl_id','canonical_smiles','standard_value']
df3 = df2_nr[selection]
df3.to_csv('acetylcholinesterase_02_bioactivity_data_preprocessed.csv', index=False)
print("Saved preprocessed data to 'acetylcholinesterase_02_bioactivity_data_preprocessed.csv'")

# ----------------------
# Label compounds as active, intermediate, inactive
# ----------------------
df4 = pd.read_csv('acetylcholinesterase_02_bioactivity_data_preprocessed.csv')
bioactivity_threshold = []
for i in df4.standard_value:
    if float(i) >= 10000:
        bioactivity_threshold.append("inactive")
    elif float(i) <= 1000:
        bioactivity_threshold.append("active")
    else:
        bioactivity_threshold.append("intermediate")

bioactivity_class = pd.Series(bioactivity_threshold, name='class')
df5 = pd.concat([df4, bioactivity_class], axis=1)
print(df5.head())

df5.to_csv('acetylcholinesterase_03_bioactivity_data_curated.csv', index=False)
print("Saved curated data to 'acetylcholinesterase_03_bioactivity_data_curated.csv'")

# ----------------------
# Optional: Zip CSV files using subprocess
# ----------------------
subprocess.run(['zip', 'acetylcholinesterase.zip', '*.csv'])
subprocess.run(['ls', '-l'])
