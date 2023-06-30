import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def predict_disease(symptoms):
        # Create a new dataframe with the same columns as the symptom matrix
        user_symptoms = pd.DataFrame(columns=symptom_matrix.columns)

        # Add the user's symptoms to the dataframe
        for symptom in symptoms:
            if symptom in user_symptoms.columns:
                user_symptoms.loc[0, symptom] = \
                symptom_severity.loc[symptom_severity['Symptom'] == symptom, 'weight'].values[0]
            else:
                print(f'Warning: Symptom {symptom} not recognized')
        user_symptoms.fillna(0, inplace=True)
        # Make a prediction
        probabilities = clf.predict_proba(user_symptoms)

        # clf.classes_ gives you the list of classes in the order they appear in probabilities
        classes = clf.classes_

        # Create a dictionary that maps each class (disease) to its corresponding probability
        disease_probability = dict(zip(classes, probabilities[0]))

        # Filter the dictionary to show only diseases with 50% probability or higher
        high_probability_diseases = {disease: prob for disease, prob in disease_probability.items() if prob >= 0.1}

        return high_probability_diseases
# Load the data
symptom_severity = pd.read_csv('Symptom-severity.csv')
dataset = pd.read_csv('dataset.csv')
# Preprocess the data
dataset.fillna('', inplace=True)
symptom_severity.fillna(0, inplace=True)
# Add an extra level to the columns
# Create a binary matrix for the symptoms
# Create a binary matrix for the symptoms
symptom_matrix = pd.get_dummies(dataset.iloc[:, 1:].stack().reset_index(level=1, drop=True))
symptom_matrix = symptom_matrix.groupby(level=0).sum()


# Incorporate the weights of the symptoms
for symptom in symptom_severity['Symptom']:
    if symptom in symptom_matrix.columns:
        symptom_matrix[symptom] *= symptom_severity.loc[symptom_severity['Symptom'] == symptom, 'weight'].values[0]

# Display the first few rows of the symptom matrix
symptom_matrix.head()

symptom_matrix.columns = symptom_matrix.columns.str.strip()
# Split the data into training and testing sets
X = symptom_matrix

y = dataset['Disease']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
clf = RandomForestClassifier(n_estimators=5, max_depth=18,random_state=42)
clf.fit(X_train, y_train)

# Make predictions on the test set
y_pred = clf.predict(X_test)

# Calculate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print(accuracy)
print(predict_disease(['itching', 'nodal_skin_eruptions','shivering','chills']))