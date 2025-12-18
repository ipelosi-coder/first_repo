#!/usr/bin/env python

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import VarianceThreshold
from lazypredict.Supervised import LazyRegressor

filename = "acetylcholinesterase_06_bioactivity_data_3class_pIC50_pubchem_fp.csv"
url = "https://github.com/dataprofessor/data/raw/master/acetylcholinesterase_06_bioactivity_data_3class_pIC50_pubchem_fp.csv"

if not os.path.exists(filename):
    os.system(f"wget {url}")

df = pd.read_csv(filename)

X = df.drop('pIC50', axis=1)
Y = df['pIC50']

selection = VarianceThreshold(threshold=(0.8 * (1 - 0.8)))
X = selection.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

clf = LazyRegressor(verbose=0, ignore_warnings=True)
models_train, predictions_train = clf.fit(
    X_train, X_train, Y_train, Y_train
)

models_test, predictions_test = clf.fit(
    X_train, X_test, Y_train, Y_test
)

print("=== Training set results ===")
print(predictions_train)

print("\n=== Test set results ===")
print(predictions_test)
