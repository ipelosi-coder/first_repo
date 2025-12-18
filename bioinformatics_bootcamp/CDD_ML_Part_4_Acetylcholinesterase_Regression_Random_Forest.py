import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import VarianceThreshold

# Download CSV if not present
filename = 'acetylcholinesterase_06_bioactivity_data_3class_pIC50_pubchem_fp.csv'
url = "https://github.com/dataprofessor/data/raw/master/acetylcholinesterase_06_bioactivity_data_3class_pIC50_pubchem_fp.csv"
if not os.path.exists(filename):
    os.system(f"wget {url}")

# Load dataset
df = pd.read_csv(filename)

# Prepare input/output
X = df.drop('pIC50', axis=1)
Y = df.pIC50

# Remove low-variance features
selection = VarianceThreshold(threshold=(.8 * (1 - .8)))
X = selection.fit_transform(X)

# Split data 80/20
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Train Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, Y_train)
r2 = model.score(X_test, Y_test)
print("R2 score:", r2)

# Predict
Y_pred = model.predict(X_test)

# Plot Experimental vs Predicted pIC50
sns.set(color_codes=True)
sns.set_style("white")
ax = sns.regplot(x=Y_test, y=Y_pred, scatter_kws={'alpha':0.4})
ax.set_xlabel('Experimental pIC50', fontsize='large', fontweight='bold')
ax.set_ylabel('Predicted pIC50', fontsize='large', fontweight='bold')
ax.set_xlim(0, 12)
ax.set_ylim(0, 12)
ax.figure.set_size_inches(5, 5)
plt.show()
