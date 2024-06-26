# -*- coding: utf-8 -*-
"""CREDIT CARD FRAUD DETECTION"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, precision_score, recall_score, f1_score, accuracy_score

# Load the dataset
data = pd.read_csv("/content/creditcard.csv")

# Normalize the 'Amount' column
scaler = StandardScaler()
data['Amount'] = scaler.fit_transform(data[['Amount']])

# Drop the 'Time' column
data.drop(columns=['Time'], inplace=True)

# Check for and handle missing values in the target variable *before* separating features and target
if data['Class'].isnull().values.any():
    print("Warning: Target variable contains missing values. Handling them by dropping the corresponding rows.")
    data = data.dropna(subset=['Class']) # Drop rows in the entire dataset where 'Class' is missing

# Separate features and target *after* handling missing values
X = data.drop(columns=['Class'])
y = data['Class']

# Apply SMOTE to balance the classes
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.3, random_state=42)

# Train the model
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1-Score:", f1_score(y_test, y_pred))

# Detailed classification report
print(classification_report(y_test, y_pred))
