
import streamlit as st
import psycopg2
import datetime
from psycopg2.extras import Json

st.set_page_config(page_title="Mwanza Irrigation Data Tool", layout="centered")

st.title("🌿 Mwanza Irrigation Data Collection & Monitoring Tool")

# Database connection using Streamlit secrets
def get_connection():
    return psycopg2.connect(
        host=st.secrets["db_host"],
        database=st.secrets["db_name"],
        user=st.secrets["db_user"],
        password=st.secrets["db_password"],
        port=st.secrets["db_port"]
    )

# Form UI
with st.form("irrigation_form"):
    st.subheader("🔍 Basic Information")
    epa = st.text_input("EPA Name")
    section = st.text_input("Section")
    visit_date = st.date_input("Date of Visit", datetime.date.today())
    scheme_name = st.text_input("Irrigation Scheme Name")
    gps_e = st.text_input("GPS Easting")
    gps_n = st.text_input("GPS Northing")
    project_name = st.text_input("Project Name")
    financial_year = st.text_input("Financial Year")
    quarter = st.selectbox("Quarter", ["Q1", "Q2", "Q3", "Q4"])
    month = st.text_input("Month")

    st.subheader("👥 Beneficiaries")
    male = st.number_input("Male", min_value=0, step=1)
    female = st.number_input("Female", min_value=0, step=1)
    total = male + female

    st.subheader("📏 Irrigation Area")
    potential = st.number_input("Potential Area (Ha)", step=0.1)
    developed = st.number_input("Developed Area (Ha)", step=0.1)
    actual = st.number_input("Actual Area under Irrigation (Ha)", step=0.1)
    newly = st.number_input("Newly Developed Area (Ha)", step=0.1)

    st.subheader("💧 Water Sources")
    water_sources = st.multiselect("Select Water Sources", ["Dam", "Stream", "Shallow Well", "Deep Well", "Borehole"])

    st.subheader("🚜 Irrigation Systems Used")
    systems = st.multiselect("Select Irrigation Systems", ["Watering cans/buckets", "Motorized pumps", "Solar Pumps", "River diversion", "Treadle Pumps"])

    st.subheader("🌾 Cropping Area")
    area_1 = st.number_input("Area under 1 Cropping Cycle (Ha)", step=0.1)
    area_2 = st.number_input("Area under 2 Cropping Cycles (Ha)", step=0.1)
    area_3 = st.number_input("Area under 3 Cropping Cycles (Ha)", step=0.1)
    area_4 = st.number_input("Area under 4 Cropping Cycles (Ha)", step=0.1)

    st.subheader("⚠️ Challenges & Solutions")
    challenges = st.text_area("Challenges")
    solutions = st.text_area("Proposed Solutions")

    submitted = st.form_submit_button("Submit Entry")

    if submitted:
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO irrigation_data (
                    epa_name, section, visit_date, scheme_name,
                    gps_easting, gps_northing, project_name,
                    financial_year, quarter, month,
                    male_beneficiaries, female_beneficiaries, total_beneficiaries,
                    potential_area_ha, developed_area_ha, actual_area_ha, new_developed_ha,
                    water_sources, irrigation_systems,
                    area_1_cycle, area_2_cycle, area_3_cycle, area_4_cycle,
                    challenges, solutions
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                epa, section, visit_date, scheme_name, gps_e, gps_n,
                project_name, financial_year, quarter, month,
                male, female, total,
                potential, developed, actual, newly,
                water_sources, systems,
                area_1, area_2, area_3, area_4,
                challenges, solutions
            ))
            conn.commit()
            cur.close()
            conn.close()
            st.success("✅ Data submitted successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
