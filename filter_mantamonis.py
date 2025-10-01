import pandas as pd

# Load the Excel file
df = pd.read_excel("Mantamonis_bacterial_contamination_analysis.xlsx")

# Filter to only the two desired columns
filtered = df[['contig ID', 'Seq Coverage']]

# Sort by Seq Coverage descending
filtered = filtered.sort_values(by='Seq Coverage', ascending=False)

# Save to your first_repo folder
output_path = 
"/Users/isabellapelosi/Documents/Bioinformatics/first_repo/filtered_mantamonis.csv"
filtered.to_csv(output_path, index=False)

print(f"✅ Filtered dataset saved to: {output_path}")

