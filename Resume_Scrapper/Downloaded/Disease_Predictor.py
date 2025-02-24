"""
This is a test model
Used Logistic Regression on a self made dataset
"""

import numpy as np

data = {
    'fever': [1, 0, 1, 1, 0, 1, 1], #for the seven samples 1 represents  fever and 0 represents no fever
    'cough': [1, 0, 0, 1, 0, 1, 0],
    'headache': [0, 1, 1, 0, 1, 1, 0],
    'sore_throat': [1, 0, 1, 1, 0, 1, 1],
    'fatigue': [1, 0, 1, 1, 0, 0, 1],
    'muscle_pain': [1, 1, 1, 0, 0, 1, 0],
    'loss_of_taste': [1, 0, 1, 1, 0, 0, 1],
    'shortness_of_breath': [0, 1, 1, 0, 0, 1, 1],#same till here
    'Flu': [1, 0, 0, 1, 0, 1, 0], #this also works the same, takes samples saying if the patient has the disease or not 
    'Tumor': [0, 1, 1, 0, 0, 1, 0], #Each col here is one person's data. So if that person has certain symptoms with indications of a disease. The probability of have the disease increases.
    'Lead to Cancer': [1, 0, 1, 1, 0, 0, 1],  
    'Jaundice': [0, 0, 1, 0, 1, 0, 1]
}


symptoms = list(data.keys())[:-4]#takes keys from start to last 5th key.
diseases = list(data.keys())[-4:]#takes keys from last 4th to last.
X = np.array([data[symptom] for symptom in symptoms]).T
y_dict = {disease: np.array(data[disease]) for disease in diseases}

# Add intercept term to X
X = np.hstack((np.ones((X.shape[0], 1)), X))

# Sigmoid function for logistic regression
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# Logistic Regression Model
class LogisticRegression:
    def __init__(self, lr=0.1, n_iter=1000):
        self.lr = lr
        self.n_iter = n_iter

    def fit(self, X, y):
        self.theta = np.zeros(X.shape[1])
        for _ in range(self.n_iter):
            z = np.dot(X, self.theta)
            predictions = sigmoid(z)
            gradient = np.dot(X.T, (predictions - y)) / y.size
            self.theta -= self.lr * gradient

    def predict_proba(self, X):
        return sigmoid(np.dot(X, self.theta))

# Train models for each disease in a loop
models = {}
for disease, y in y_dict.items():
    model = LogisticRegression(lr=0.1, n_iter=1000)
    model.fit(X, y)
    models[disease] = model

# User input for symptoms
symptom_input = {}
user_data = [1]  # Intercept term

print("Please answer 'yes' or 'no' for the following symptoms:")

for symptom in symptoms:
    answer = input(f"Do you have {symptom}? ").strip().lower()
    symptom_input[symptom] = 1 if answer == "yes" else 0
    user_data.append(symptom_input[symptom])

# Convert user_data to numpy array
user_data = np.array(user_data).reshape(1, -1)

# Show symptoms the user has
present_symptoms = [symptom for symptom, value in symptom_input.items() if value == 1]
if present_symptoms:
    print("\nYou have the following symptoms:", ", ".join(present_symptoms))
else:
    print("\nYou have no symptoms listed.")

# Make predictions for each disease and store probabilities
disease_probabilities = {disease: model.predict_proba(user_data)[0] for disease, model in models.items()}

# Display prediction results
print("\nDisease Prediction Probabilities:")
for disease, prob in disease_probabilities.items():
    print(f"{disease}: {(prob)*100:.2f}%")

# Determine the most likely disease and threshold diseases
most_likely_disease = max(disease_probabilities, key=disease_probabilities.get)
most_likely_prob = disease_probabilities[most_likely_disease]
high_risk_diseases = {disease: prob for disease, prob in disease_probabilities.items() if prob > 0.8}

# Print the results
print(f"\nMost Likely Disease Based on Symptoms: {most_likely_disease} (Probability: {(most_likely_prob)*100:.2f}%)")

if high_risk_diseases:
    print("\nDiseases with a High Likelihood:")
    for disease, prob in high_risk_diseases.items():
        print(f"- {disease} with a probability of {(prob)*100:.2f}%")
else:
    print("\nNo diseases have a high likelihood based on your symptoms.")
