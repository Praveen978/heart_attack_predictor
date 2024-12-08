from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import pandas as pd
import numpy as np
df = pd.read_csv("C:/Users/Praveen/Downloads/heart.csv")

X = df.drop("output", axis=1)
y = df["output"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Instantiate and fit the model
clf = SVC(kernel='linear', C=1, random_state=42).fit(X_train, y_train)

# Predict the values
y_pred = clf.predict(X_test)

# Print the accuracy
#print("The test accuracy score of SVM is ", accuracy_score(y_test, y_pred))

import joblib
import streamlit as st
# Save the trained model
joblib.dump(clf, 'heart_attack_model.pkl')

# Load the trained model
model = joblib.load('heart_attack_model.pkl')

# Title of the web app
st.title("Heart Attack Prediction App")

# Input fields for user data
st.sidebar.header("Enter Patient Details")
age = st.sidebar.slider("Age", 20, 100, 50)
sex = st.sidebar.selectbox("Sex (1=Male, 0=Female)", [1, 0])
cp = st.sidebar.slider("Chest Pain Type (0-3)", 0, 3, 1)
trestbps = st.sidebar.slider("Resting Blood Pressure (mm Hg)", 80, 200, 120)
chol = st.sidebar.slider("Cholesterol Level (mg/dL)", 100, 600, 200)
fbs = st.sidebar.selectbox("Fasting Blood Sugar > 120 mg/dL (1=True, 0=False)", [1, 0])
restecg = st.sidebar.slider("Resting ECG Results (0-2)", 0, 2, 1)
thalach = st.sidebar.slider("Maximum Heart Rate Achieved", 50, 220, 150)
exang = st.sidebar.selectbox("Exercise-Induced Angina (1=Yes, 0=No)", [1, 0])
oldpeak = st.sidebar.slider("ST Depression Induced by Exercise", 0.0, 5.0, 1.0)
slope = st.sidebar.slider("Slope of ST Segment (0-2)", 0, 2, 1)
ca = st.sidebar.slider("Number of Major Vessels (0-4)", 0, 4, 0)
thal = st.sidebar.slider("Thalassemia (0-3)", 0, 3, 2)

# Predict button
if st.button("Predict"):
    # Prepare the input array for prediction
    input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
    prediction = model.predict(input_data)

    # Display result
    if prediction[0] == 1:
        st.success("The patient is likely to have a heart attack. Please consult a doctor immediately.")
    else:
        st.success("The patient is unlikely to have a heart attack. Keep monitoring health regularly.")


