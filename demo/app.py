import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from database import Database, Gender, AppointmentType, AppointmentStatus

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="MediTech Demo",
    page_icon="🏥",
    layout="wide"
)

# เชื่อมต่อฐานข้อมูล
@st.cache_resource
def get_database():
    # ตรวจสอบการใช้งานฐานข้อมูลจริงจาก session state
    use_real_db = st.session_state.get('use_real_db', False)
    return Database(use_real_db=use_real_db)

# สร้างหรือโหลด session state
if 'use_real_db' not in st.session_state:
    st.session_state.use_real_db = False

# หน้าหลัก
st.title("🏥 MediTech HealthCheckup System")
st.subheader("ระบบตรวจสุขภาพและบันทึกข้อมูลทางการแพทย์")

# เลือกโหมดการเชื่อมต่อฐานข้อมูล
db_mode = st.sidebar.radio(
    "โหมดการเชื่อมต่อฐานข้อมูล",
    ["ใช้ข้อมูลตัวอย่าง", "เชื่อมต่อฐานข้อมูลจริง"]
)

if db_mode == "เชื่อมต่อฐานข้อมูลจริง" and not st.session_state.use_real_db:
    st.session_state.use_real_db = True
    st.experimental_rerun()
elif db_mode == "ใช้ข้อมูลตัวอย่าง" and st.session_state.use_real_db:
    st.session_state.use_real_db = False
    st.experimental_rerun()

# เชื่อมต่อฐานข้อมูล
db = get_database()

# เมนูด้านข้าง
menu = st.sidebar.selectbox(
    "เลือกส่วนที่ต้องการสาธิต",
    ["การจัดการผู้ป่วย", "ระบบนัดหมาย", "การบันทึกผลตรวจ", "การออกรายงาน"]
)

# แสดงเนื้อหาตามเมนูที่เลือก
if menu == "การจัดการผู้ป่วย":
    st.header("👤 การจัดการข้อมูลผู้ป่วย")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("ค้นหาผู้ป่วย")
        search = st.text_input("ค้นหาด้วยรหัสหรือชื่อ")
        patients = db.get_patients(search)
        if patients:
            patients_df = pd.DataFrame([
                {
                    "รหัส": p.id,
                    "ชื่อ": p.name,
                    "อายุ": p.age,
                    "เพศ": p.gender.value,
                    "โรคประจำตัว": p.conditions
                }
                for p in patients
            ])
            st.dataframe(patients_df)
        else:
            st.info("ไม่พบข้อมูลผู้ป่วย")
    
    with col2:
        st.subheader("เพิ่ม/แก้ไขข้อมูล")
        patient_id = st.text_input("รหัสผู้ป่วย", "P0000")
        name = st.text_input("ชื่อ-นามสกุล")
        age = st.number_input("อายุ", 0, 120, 25)
        gender = st.selectbox("เพศ", ["ชาย", "หญิง"])
        conditions = st.multiselect(
            "โรคประจำตัว",
            ["ความดัน", "เบาหวาน", "ไขมัน", "หัวใจ"]
        )
        
        if st.button("บันทึก"):
            try:
                db.add_patient(
                    id=patient_id,
                    name=name,
                    age=age,
                    gender=gender,
                    conditions=", ".join(conditions)
                )
                st.success("บันทึกข้อมูลสำเร็จ")
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {str(e)}")

elif menu == "ระบบนัดหมาย":
    st.header("📅 ระบบนัดหมาย")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("ตารางนัดหมาย")
        appointments = db.get_appointments()
        if appointments:
            appointments_df = pd.DataFrame([
                {
                    "วันที่": a.date,
                    "รหัสคนไข้": a.patient_id,
                    "ประเภท": a.type.value,
                    "สถานะ": a.status.value
                }
                for a in appointments
            ])
            st.dataframe(appointments_df)
        else:
            st.info("ไม่พบข้อมูลการนัดหมาย")
    
    with col2:
        st.subheader("จองคิวตรวจ")
        appointment_date = st.date_input("วันที่นัดหมาย")
        patients = db.get_patients()
        patient_options = {p.name: p.id for p in patients}
        patient_name = st.selectbox("เลือกผู้ป่วย", list(patient_options.keys()))
        appointment_type = st.selectbox(
            "ประเภทการตรวจ",
            ["ตรวจทั่วไป", "ตรวจเฉพาะทาง", "ติดตามผล", "ฉุกเฉิน"]
        )
        
        if st.button("จองคิว"):
            try:
                db.add_appointment(
                    date=appointment_date,
                    patient_id=patient_options[patient_name],
                    type=appointment_type
                )
                st.success("จองคิวสำเร็จ")
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {str(e)}")

elif menu == "การบันทึกผลตรวจ":
    st.header("🔬 การบันทึกผลตรวจ")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("บันทึกผลตรวจ")
        patients = db.get_patients()
        patient_options = {p.name: p.id for p in patients}
        patient_name = st.selectbox("เลือกผู้ป่วย", list(patient_options.keys()))
        pressure = st.number_input("ความดันโลหิต", 90, 200, 120)
        sugar = st.number_input("ระดับน้ำตาล", 70, 200, 100)
        cholesterol = st.number_input("คอเลสเตอรอล", 100, 300, 200)
        
        if st.button("บันทึกผล"):
            try:
                db.add_health_record(
                    patient_id=patient_options[patient_name],
                    date=datetime.now().date(),
                    blood_pressure=pressure,
                    blood_sugar=sugar,
                    cholesterol=cholesterol
                )
                st.success("บันทึกผลตรวจสำเร็จ")
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {str(e)}")
    
    with col2:
        st.subheader("กราฟติดตามผล")
        if patient_name:
            records = db.get_health_records(patient_options[patient_name])
            if records:
                records_df = pd.DataFrame([
                    {
                        "วันที่": r.date,
                        "ความดัน": r.blood_pressure,
                        "น้ำตาล": r.blood_sugar,
                        "คอเลสเตอรอล": r.cholesterol
                    }
                    for r in records
                ])
                
                metric = st.selectbox(
                    "เลือกค่าที่ต้องการดู",
                    ["ความดัน", "น้ำตาล", "คอเลสเตอรอล"]
                )
                
                fig = px.line(
                    records_df,
                    x="วันที่",
                    y=metric,
                    title=f"การติดตามค่า{metric}"
                )
                st.plotly_chart(fig)
            else:
                st.info("ไม่พบข้อมูลผลตรวจ")

else:  # การออกรายงาน
    st.header("📊 การออกรายงาน")
    
    tab1, tab2, tab3 = st.tabs(["สถิติผู้ป่วย", "สถิติการนัดหมาย", "สถิติผลตรวจ"])
    
    with tab1:
        patients = db.get_patients()
        if patients:
            patients_df = pd.DataFrame([
                {
                    "เพศ": p.gender.value,
                    "โรคประจำตัว": p.conditions
                }
                for p in patients
            ])
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("จำนวนผู้ป่วยตามเพศ")
                fig = px.pie(
                    patients_df,
                    names="เพศ",
                    title="สัดส่วนผู้ป่วยตามเพศ"
                )
                st.plotly_chart(fig)
            
            with col2:
                st.subheader("จำนวนผู้ป่วยตามโรค")
                disease_counts = pd.Series([
                    disease.strip()
                    for conditions in patients_df["โรคประจำตัว"]
                    for disease in conditions.split(",")
                    if disease.strip()
                ]).value_counts()
                
                fig = px.bar(
                    disease_counts,
                    title="จำนวนผู้ป่วยตามโรคประจำตัว"
                )
                st.plotly_chart(fig)
        else:
            st.info("ไม่พบข้อมูลผู้ป่วย")
    
    with tab2:
        appointments = db.get_appointments()
        if appointments:
            appointments_df = pd.DataFrame([
                {
                    "ประเภท": a.type.value,
                    "สถานะ": a.status.value
                }
                for a in appointments
            ])
            
            st.subheader("สถิติการนัดหมาย")
            fig = px.histogram(
                appointments_df,
                x="ประเภท",
                color="สถานะ",
                title="จำนวนการนัดหมายตามประเภทและสถานะ"
            )
            st.plotly_chart(fig)
        else:
            st.info("ไม่พบข้อมูลการนัดหมาย")
    
    with tab3:
        records = db.get_health_records()
        if records:
            records_df = pd.DataFrame([
                {
                    "วันที่": r.date,
                    "ความดัน": r.blood_pressure,
                    "น้ำตาล": r.blood_sugar,
                    "คอเลสเตอรอล": r.cholesterol
                }
                for r in records
            ])
            
            st.subheader("แนวโน้มผลตรวจ")
            fig = px.line(
                records_df,
                x="วันที่",
                y=["ความดัน", "น้ำตาล", "คอเลสเตอรอล"],
                title="แนวโน้มค่าสุขภาพโดยรวม"
            )
            st.plotly_chart(fig)
        else:
            st.info("ไม่พบข้อมูลผลตรวจ")

# แสดงสถานะระบบ
st.sidebar.markdown("---")
st.sidebar.subheader("สถานะระบบ")
col1, col2, col3 = st.sidebar.columns(3)

patients = db.get_patients()
appointments = db.get_appointments()
pending_appointments = [a for a in appointments if a.status == AppointmentStatus.PENDING]

col1.metric("ผู้ป่วยทั้งหมด", len(patients))
col2.metric(
    "นัดหมายวันนี้",
    len([a for a in appointments if a.date == datetime.now().date()])
)
col3.metric("รอดำเนินการ", len(pending_appointments)) 