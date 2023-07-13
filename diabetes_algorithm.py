import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error


# NOTE: THIS TAKES 10 MINS TO RUN ON MY I7-12700K CPU SO NEED TO FIX LATER
# also model is very inaccurate atm, need to clean data or use diff features

# Load the data
data = pd.read_csv('BRFSS_2021_dataset.csv')

# Define the target variable
target = 'Diabetes'

# Convert target to binary
data[target] = data[target].map({'Yes': 1, 'No': 0})

# Separate the target variable from the rest of the data
y = data[target]
X = data.drop(target, axis=1)

# Encode categorical variables
encoder = OrdinalEncoder()
X_encoded = pd.DataFrame(encoder.fit_transform(X), columns=X.columns)

# Remove instances with missing target values
X_encoded = X_encoded[~np.isnan(y)]
y = y.dropna()

# Split the data into a training set and a test set
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# helper function so we don't have to repeat code
def train_and_evaluate(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    return mse, mae

# Train and evaluate multiple models
results = {}

model = LogisticRegression(random_state=42)
mse, mae = train_and_evaluate(model, X_train_scaled, y_train, X_test_scaled, y_test)
results['Logistic Regression'] = {'MSE': mse, 'MAE': mae}

model = DecisionTreeClassifier(random_state=42)
mse, mae = train_and_evaluate(model, X_train, y_train, X_test, y_test)
results['Decision Tree'] = {'MSE': mse, 'MAE': mae}

model = RandomForestClassifier(random_state=42)
mse, mae = train_and_evaluate(model, X_train, y_train, X_test, y_test)
results['Random Forest'] = {'MSE': mse, 'MAE': mae}

model = SVC(random_state=42)
mse, mae = train_and_evaluate(model, X_train_scaled, y_train, X_test_scaled, y_test)
results['SVM'] = {'MSE': mse, 'MAE': mae}

model = MLPClassifier(random_state=42)
mse, mae = train_and_evaluate(model, X_train_scaled, y_train, X_test_scaled, y_test)
results['ANN'] = {'MSE': mse, 'MAE': mae}

# Display the results
results_df = pd.DataFrame(results).T
print(results_df)
