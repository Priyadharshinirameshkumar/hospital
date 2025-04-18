import streamlit as st
import sqlite3
import pandas as pd


# Set Streamlit page config
st.set_page_config(page_title="Hospital Cloud System", layout="wide")

# Function to set background from image URL
def set_bg_url(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .stSidebar {{
            background-color: rgba(255, 255, 255, 0.85);
        }}
        .stDataFrame, .stButton, .stSelectbox, .stTextInput, .stSlider, .stDateInput {{
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 10px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ✅ Set a working background image
set_bg_url("https://bsmedia.business-standard.com/_media/bs/img/article/2024-05/27/full/1716791846-1251.jpg")

# Title
st.title("🏥 Cloud-Based Hospital Management System")

# Connect to SQLite
conn = sqlite3.connect("hospital.db", check_same_thread=False)
cursor = conn.cursor()

# Sidebar Navigation
menu = ["Patients", "Doctors", "Appointments", "Reports"]
choice = st.sidebar.radio("Navigate", menu)

# PATIENTS
if choice == "Patients":
    st.header("🧑‍🤝‍🧑 Add New Patient")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
        age = st.number_input("Age", 0, 120)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        diagnosis = st.text_input("Diagnosis")
    with col2:
        emergency_contact = st.text_input("Emergency Contact")
        insurance_provider = st.text_input("Insurance Provider (Optional)")
        insurance_number = st.text_input("Insurance Number (Optional)")

    if st.button("➕ Add Patient"):
        cursor.execute("""
            INSERT INTO patients (name, age, gender, diagnosis, emergency_contact, insurance_provider, insurance_number) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, age, gender, diagnosis, emergency_contact, insurance_provider, insurance_number))
        conn.commit()
        st.success("✅ Patient added successfully!")

    st.subheader("📋 Existing Patients")
    df = pd.read_sql("SELECT * FROM patients", conn)
    st.dataframe(df, use_container_width=True)

# DOCTORS
elif choice == "Doctors":
    st.header("👨‍⚕️ Register Doctor")
    col1, col2 = st.columns(2)
    with col1:
        doctor_name = st.text_input("Doctor Name")
        specialization = st.text_input("Specialization")
    with col2:
        experience = st.slider("Experience (Years)", 0, 40, 5)

    if st.button("➕ Add Doctor"):
        cursor.execute("""
            INSERT INTO doctors (name, specialization, experience) 
            VALUES (?, ?, ?)
        """, (doctor_name, specialization, experience))
        conn.commit()
        st.success("✅ Doctor added!")

    st.subheader("📋 Registered Doctors")
    df = pd.read_sql("SELECT * FROM doctors", conn)
    st.dataframe(df, use_container_width=True)

# APPOINTMENTS
elif choice == "Appointments":
    st.header("📅 Schedule Appointment")

    patients = cursor.execute("SELECT id, name FROM patients").fetchall()
    doctors = cursor.execute("SELECT id, name FROM doctors").fetchall()

    patient_dict = {name: pid for pid, name in patients}
    doctor_dict = {name: did for did, name in doctors}

    patient_selected = st.selectbox("Select Patient", list(patient_dict.keys()))
    doctor_selected = st.selectbox("Select Doctor", list(doctor_dict.keys()))
    appointment_date = st.date_input("Appointment Date")

    if st.button("📌 Schedule"):
        cursor.execute("""
            INSERT INTO appointments (patient_id, doctor_id, appointment_date) 
            VALUES (?, ?, ?)
        """, (patient_dict[patient_selected], doctor_dict[doctor_selected], str(appointment_date)))
        conn.commit()
        st.success(f"✅ Appointment booked with Dr. {doctor_selected} on {appointment_date}")

    st.subheader("📋 Appointment Records")
    query = """
        SELECT a.id, p.name AS Patient, d.name AS Doctor, a.appointment_date
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df, use_container_width=True)

# REPORTS
elif choice == "Reports":
    st.header("📊 System Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Patients", cursor.execute("SELECT COUNT(*) FROM patients").fetchone()[0])
    col2.metric("Total Doctors", cursor.execute("SELECT COUNT(*) FROM doctors").fetchone()[0])
    col3.metric("Appointments", cursor.execute("SELECT COUNT(*) FROM appointments").fetchone()[0])

    st.info("🔐 Data stored securely using SQLite.")

# Close connection
conn.close()



