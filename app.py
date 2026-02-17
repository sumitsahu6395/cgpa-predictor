import streamlit as st
import joblib
import json
import os
import warnings
import matplotlib.pyplot as plt
import numpy as np

warnings.filterwarnings("ignore")

# Load model
LR = joblib.load("D:/LR/LINEARMODEL")

st.set_page_config(page_title="CGPA Predictor", page_icon="🎓", layout="centered")

USERS_FILE = "users.json"

# ---------- USER DATA FUNCTIONS ---------- #

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# ---------- SESSION STATE ---------- #

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------- REGISTER PAGE ---------- #

def register():
    st.subheader("📝 Register")

    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")

    if st.button("Register"):
        users = load_users()

        if new_user in users:
            st.error("User already exists")
        else:
            users[new_user] = new_pass
            save_users(users)
            st.success("Registration successful! You can login now.")

# ---------- LOGIN PAGE ---------- #

def login():
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()

        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---------- AUTH SECTION ---------- #

if not st.session_state.logged_in:
    choice = st.radio("Select Option", ["Login", "Register"])

    if choice == "Login":
        login()
    else:
        register()

    st.stop()

# ---------- DARK MODE ---------- #

dark_mode = st.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown("""
        <style>
        body { background-color: #0e1117; color: white; }
        </style>
    """, unsafe_allow_html=True)

# ---------- APP HEADER ---------- #

st.title("🎓 Student CGPA Predictor")
st.write(f"Welcome, **{st.session_state.username}** 👋")

# ---------- INPUT ---------- #

hours = st.number_input("📚 Study Hours", 0.0, 24.0, step=0.5)

# ---------- PREDICT ---------- #

if st.button("Predict CGPA 🚀"):

    cgpa = LR.predict([[hours]])[0]

    # ✅ Limit CGPA between 0 and 10
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

# ---------- GRAPH ---------- #

st.subheader("📈 CGPA Trend")

x = np.linspace(0, 24, 50)
y = LR.predict(x.reshape(-1,1))

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("Study Hours")
ax.set_ylabel("CGPA")

st.pyplot(fig)

# ---------- DASHBOARD ---------- #

st.subheader("📊 Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Max CGPA", "10")
col2.metric("Recommended Hours", "8+")
col3.metric("Status", "Active")

# ---------- LOGOUT ---------- #

if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
