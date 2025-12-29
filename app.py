import streamlit as st
import pandas as pd

# --- SETTINGS ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1z3GnmXOaouQH6Z0ZG59b8AftTTuL0gc5cgcAKHUqPiY/export?format=xlsx"

doctor_sequence = [
    "Total",
    "DR. PADMANABHA SHENOY",
    "DR. SANJANA JOSEPH",
    "DR. ANUROOPA VIJAYAN",
    "DR. K. NARAYANAN",
    "DR. KAVERI K NALIANDA",
    "DR. ANU SREEKANTH",
    "DR. VISHAL MARWAHA",
    "RANJINI C",
    "DR. PRIYA PRABHAKARAN",
    "Unknown"
]

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Read Google Sheet as Excel
    sheet25 = pd.read_excel(SHEET_URL, sheet_name="Sheet25")
    cokstats = pd.read_excel(SHEET_URL, sheet_name="COKStats")
    return sheet25, cokstats

sheet25, cokstats = load_data()

# --- SIDEBAR ---
selected_doctor = st.sidebar.selectbox("Choose Doctor", doctor_sequence)

# --- FILTER PATIENTS ---
if selected_doctor == "Total":
    doctor_data = sheet25
else:
    doctor_data = sheet25[sheet25["Doctor Name"] == selected_doctor]

st.title(f"Patients - {selected_doctor}")

# --- PATIENT TILES ---
for _, row in doctor_data.iterrows():
    st.markdown(f"""
    <div style="background:#0078D7;color:white;padding:15px;margin:10px;border-radius:8px;">
        <h4>{row['Name']} ({row['OP No']})</h4>
        <p>Phone: {row['Phone No']}</p>
        <p>Type: {row['Type']}</p>
        <p>Confirm Time: {row['Confirm Time']}</p>
        <p>Regn Time: {row['Regn. Time']}</p>
        <p>Service: {row['Service']}</p>
        <p>Specimen Coll.Time: {row['Specimen Coll.Time']}</p>
        <p>Service Result: {row['Service Result']}</p>
        <p>Entry Time: {row['Entry Time']}</p>
        <p>Exit Time: {row['Exit Time']}</p>
    </div>
    """, unsafe_allow_html=True)

# --- PERFORMANCE INDICES ---
st.subheader("General Performance Indices (HH:MM)")

def avg_time(df, col1, col2):
    # Convert to datetime
    t1 = pd.to_datetime(df[col1], errors="coerce")
    t2 = pd.to_datetime(df[col2], errors="coerce")
    diffs = (t1 - t2).dropna().dt.total_seconds()
    if len(diffs) == 0:
        return "00:00"
    avg_secs = diffs.mean()
    mins, secs = divmod(avg_secs, 60)
    return f"{int(mins):02}:{int(secs):02}"

indices = {
    "Average Turnaround (Service Result - Specimen Coll.Time)": ("Service Result", "Specimen Coll.Time"),
    "Average Sample Collection Turnaround (Specimen Coll.Time - Service)": ("Specimen Coll.Time", "Service"),
    "Average Patient Entry (Confirm Time - Regn. Time)": ("Confirm Time", "Regn. Time")
}

for label, (c1, c2) in indices.items():
    st.write(f"**{label}**")
    st.write(f"Total: {avg_time(cokstats, c1, c2)}")
    st.write(f"Last 10 patients: {avg_time(cokstats.tail(10), c1, c2)}")
