import streamlit as st
st.image("C:/Users/Praveen/Downloads/WhatsApp Image 2024-11-20 at 22.24.51_e184d04c-fotor-2024112022354.png",width=300)

st.title(" Guess the Chinni ")

st.sidebar.title("Fill the data")
st.sidebar.caption( " This is a small webinterface created to know how often u know chinni ")
st.sidebar.text_input("Enter your name")

st.sidebar.text_input( " Your bond with Chinni")


st.radio(" Pick Chinni Gender" , ["Male","Female"])

st.caption (" Lets know how much do you know Chinni ")

st.selectbox("Pick Chinni's Favourite Person" , [ "Nishitha" , " Praveen " , " Viswateja"])

st.multiselect(" Choose Chinni's fav food ", [" Chicken " , " Fork " , " Mutton "])

st.select_slider(" Rate Chinni", ["Bad" , " Good" , " Excellent"])

st.date_input(" Guess Chinni's Birthday")

st.text_area( "what do you like in Chinni")

st.file_uploader(" Drop your photo with Chinni ")

st.color_picker(" Guess Chinni's Fav colour")

st.sidebar.radio(" How you related to Chinni ", ["Friend" , " BestFriend ", " Enemy "])

st.checkbox("I agree that Information given is written whole heartedly")

st.text("Rate my work")


st.button("submit")