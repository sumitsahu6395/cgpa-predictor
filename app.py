import streamlit as st
import joblib
import hashlib
import warnings
import numpy as np
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

# ---------- LOAD MODEL ----------
LR = joblib.load("LINEARMODEL")

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="CGPA Predictor",
    page_icon="🎓",
    layout="centered"
)

# ---------- PASSWORD HASH ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------- LOGIN ----------
def login():
    st.title("🔐 Student Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        users = st.secrets["users"]

        if username in users and users[username] == hash_password(password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid credentials ❌")

# ---------- AUTH ----------
if not st.session_state.logged_in:
    login()
    st.stop()

# ---------- DARK MODE ----------
dark_mode = st.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown("""
        <style>
        body { background-color: #0e1117; color: white; }
        </style>
    """, unsafe_allow_html=True)

# ---------- HEADER ----------
st.title("🎓 CGPA Predictor")
st.write(f"Welcome **{st.session_state.username}** 👋")

# ---------- INPUT ----------
hours = st.number_input("📚 Study Hours", 0.0, 24.0, step=0.5)

# ---------- PREDICT ----------
if st.button("Predict CGPA 🚀"):

    cgpa = LR.predict([[hours]])[0]

    # limit CGPA between 0 and 10
    cgpa = max(0, min(cgpa, 10))

    st.success(f"🎯 Predicted CGPA: {cgpa:.2f}")

    if cgpa >= 9:
        st.balloons()
        st.info("🏆 Excellent!")
    elif cgpa >= 7:
        st.info("👍 Very Good")
    elif cgpa >= 5:
        st.warning("🙂 Can improve")
    else:
        st.error("⚠️ Study more!")

    st.progress(min(int(cgpa * 10), 100))

# ---------- GRAPH ----------
st.subheader("📈 CGPA Trend")

x = np.linspace(0, 24, 50)
y = LR.predict(x.reshape(-1, 1))

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("Study Hours")
ax.set_ylabel("CGPA")

st.pyplot(fig)

# ---------- DASHBOARD ----------
st.subheader("📊 Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Max CGPA", "10")
col2.metric("Recommended Hours", "8+")
col3.metric("Status", "Active")

# ---------- LOGOUT ----------
if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
