import os
os.system("pip install --upgrade pip")
os.system("pip install scikit-learn==1.4.2 pandas numpy joblib Pillow")

import subprocess
import sys
import streamlit as st

try:
    import sklearn
    st.write(f"Scikit-learn version: {sklearn.__version__}")
except ImportError as e:
    st.error("Scikit-learn is not installed.")
    st.write(str(e))

# List all installed packages
try:
    installed_packages = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
    st.text(installed_packages.decode("utf-8"))
except Exception as e:
    st.error("Failed to list installed packages.")
    st.write(str(e))




from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


import pandas as pd
import numpy as np
df = pd.read_csv("heart.csv")

X = df.drop("output", axis=1)
y = df["output"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Instantiate and fit the model
clf = SVC(kernel='linear', C=1, random_state=42).fit(X_train, y_train)

# Predict the values
y_pred = clf.predict(X_test)


import joblib
import streamlit as st
import numpy as np
joblib.dump(clf, 'heart_attack_model.pkl')
# Load the trained model
from PIL import Image
# Load the trained model
model = joblib.load('heart_attack_model.pkl')

# Set up the Streamlit page configuration
st.set_page_config(
    page_title="Heart Attack Predictor ",
    page_icon="❤️",
    layout="centered"
)

# Title of the web app
image = Image.open("banner.png")
resized_image = image.resize((800, 400))  # Specify the desired width and height

# Display the resized image in Streamlit
st.image(resized_image, use_column_width=True)
st.title("Heart Attack Predictor ")
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

# Display the input data in a more readable format
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

# Prepare input data by making sure everything is numeric
input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

# Predict button with better styling
if st.button("Predict", key="predict_button"):
    # Check if the input data is in the correct format and predict
    prediction = model.predict(input_data)

    # Display result in an engaging way
    if prediction[0] == 1:
        st.image("alert.png", width=100)
        st.markdown("<h3 style='color: red;'>The patient is likely to have a heart attack. Please consult a doctor immediately.</h3>", unsafe_allow_html=True)
    else:
        st.image("C:/Users/Praveen/Downloads/sucess.png", width=100)
        st.markdown("<h3 style='color: green;'>The patient is unlikely to have a heart attack. Keep monitoring health regularly.</h3>", unsafe_allow_html=True)

# Additional info section
st.markdown("""
    ---  
    ### About the Model
    The model uses various features such as age, cholesterol levels, chest pain type, and others to predict the likelihood of a heart attack. It was trained on a dataset of heart disease patients and uses a **Support Vector Classifier (SVC)** with a linear kernel for accurate predictions.

    **Disclaimer:** This app is not a substitute for professional medical advice. Always consult a healthcare provider for a proper diagnosis and treatment plan.
""")

# Footer section with contact information
st.markdown("""
    <footer style="text-align: center; padding: 20px; background-color: #2a9d8f; color: white;">
        <p>Developed by <strong>Praveen kumar</strong> | Contact: <a href="mailto:praveengavalapally@gmail.com" style="color: white;">youremail@example.com</a></p>
    </footer>
""", unsafe_allow_html=True)


