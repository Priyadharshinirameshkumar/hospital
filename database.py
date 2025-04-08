import sqlite3

# Connect to SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

# Drop existing tables (optional if you want to reset)
# cursor.execute("DROP TABLE IF EXISTS appointments")
# cursor.execute("DROP TABLE IF EXISTS patients")
# cursor.execute("DROP TABLE IF EXISTS doctors")

# Create Patients Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    diagnosis TEXT,
    emergency_contact TEXT,
    insurance_provider TEXT,
    insurance_number TEXT
)
""")

# Create Doctors Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialization TEXT,
    experience INTEGER
)
""")

# Create Appointments Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    appointment_date TEXT,
    status TEXT DEFAULT 'Scheduled',
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
)
""")

conn.commit()
conn.close()
print("✅ Database setup completed successfully.")
