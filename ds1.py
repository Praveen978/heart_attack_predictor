import streamlit as st
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import joblib
from PIL import Image

# Set up the Streamlit page configuration
st.set_page_config(
    page_title="Heart Attack Predictor",
    page_icon="❤️",
    layout="centered"
)

# Load and prepare the dataset
df = pd.read_csv("heart.csv")

# Features and target variable
X = df.drop("output", axis=1)
y = df["output"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Instantiate and fit the model
clf = SVC(kernel='linear', C=1, random_state=42)
clf.fit(X_train, y_train)

# Save the trained model to a file
joblib.dump(clf, 'heart_attack_model.pkl')

# Load the trained model
model = joblib.load('heart_attack_model.pkl')

# Display banner image
image = Image.open("banner.png")
resized_image = image.resize((800, 400))  # Resize to desired width and height
st.image(resized_image, use_column_width=True)

# Title and app introduction
st.title("Heart Attack Predictor")
st.markdown("""
    **Welcome to the Heart Attack Prediction App!**  
    This app predicts whether a patient is likely to have a heart attack based on various health indicators.  
    Enter the patient's details below and hit "Predict" to get a result.
""")

# Sidebar for user input
st.sidebar.header("Enter Patient Details")

# Input fields for user data
age = st.sidebar.number_input("Age", min_value=20, max_value=100, value=50, step=1)
sex = st.sidebar.selectbox("Sex (1=Male, 0=Female)", [1, 0])

# Chest Pain Type with descriptive labels
cp_options = {
    0: "Typical Angina",
    1: "Atypical Angina",
    2: "Non-Anginal Pain",
    3: "Asymptomatic"
}
cp = st.sidebar.selectbox(
    "Chest Pain Type",
    options=list(cp_options.keys()),
    format_func=lambda x: f"{x} - {cp_options[x]}"
)

# Other user inputs
st.sidebar.image("hypertension.png", use_column_width=False, width=100, caption="ECG Monitoring")
trestbps = st.sidebar.slider("Resting Blood Pressure (mm Hg)", 80, 200, 120)
chol = st.sidebar.slider("Cholesterol Level (mg/dL)", 100, 600, 200)
fbs = st.sidebar.selectbox("Fasting Blood Sugar > 120 mg/dL (1=True, 0=False)", [1, 0])
st.sidebar.image("ecg.png", use_column_width=False, width=100, caption="ECG Monitoring")
restecg = st.sidebar.slider("Resting ECG Results (0-2)", 0, 2, 1)
thalach = st.sidebar.slider("Maximum Heart Rate Achieved", 50, 220, 150)
exang = st.sidebar.selectbox("Exercise-Induced Angina (1=Yes, 0=No)", [1, 0])
oldpeak = st.sidebar.slider("ST Depression Induced by Exercise", 0.0, 5.0, 1.0)
slope = st.sidebar.slider("Slope of ST Segment (0-2)", 0, 2, 1)
ca = st.sidebar.slider("Number of Major Vessels (0-4)", 0, 4, 0)
thal = st.sidebar.slider("Thalassemia (0-3)", 0, 3, 2)

# Display the entered data summary
st.subheader("Patient's Data Summary:")
st.write(f"Age: {age}")
st.write(f"Sex: {'Male' if sex == 1 else 'Female'}")
st.write(f"Chest Pain Type: {cp}")
st.write(f"Resting Blood Pressure: {trestbps} mm Hg")
st.write(f"Cholesterol Level: {chol} mg/dL")
st.write(f"Fasting Blood Sugar > 120 mg/dL: {'Yes' if fbs == 1 else 'No'}")
st.write(f"Resting ECG Results: {restecg}")
st.write(f"Maximum Heart Rate Achieved: {thalach} bpm")
st.write(f"Exercise-Induced Angina: {'Yes' if exang == 1 else 'No'}")
st.write(f"ST Depression Induced by Exercise: {oldpeak}")
st.write(f"Slope of ST Segment: {slope}")
st.write(f"Number of Major Vessels: {ca}")
st.write(f"Thalassemia: {thal}")

# Prepare the input data for prediction
input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

# Predict button and prediction logic
if st.button("Predict", key="predict_button"):
    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.image("alert.png", width=100)
        st.markdown("<h3 style='color: red;'>The patient is likely to have a heart attack. Please consult a doctor immediately.</h3>", unsafe_allow_html=True)
    else:
        st.image("success.png", width=100)
        st.markdown("<h3 style='color: green;'>The patient is unlikely to have a heart attack. Keep monitoring health regularly.</h3>", unsafe_allow_html=True)

# Additional information about the model
st.markdown("""
    ---  
    ### About the Model
    The model uses various features such as age, cholesterol levels, chest pain type, and others to predict the likelihood of a heart attack. It was trained on a dataset of heart disease patients and uses a **Support Vector Classifier (SVC)** with a linear kernel for accurate predictions.

    **Disclaimer:** This app is not a substitute for professional medical advice. Always consult a healthcare provider for a proper diagnosis and treatment plan.
""")


