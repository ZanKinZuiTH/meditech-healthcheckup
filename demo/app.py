import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from database import Database, Gender, AppointmentType, AppointmentStatus
import random

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="MediTech Demo",
    page_icon="��",
    layout="wide",
    initial_sidebar_state="expanded"
)

# สร้าง session state
if 'use_real_db' not in st.session_state:
    st.session_state.use_real_db = False
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'font_size' not in st.session_state:
    st.session_state.font_size = 16

# เชื่อมต่อฐานข้อมูล
@st.cache_resource
def get_database():
    return Database(use_real_db=st.session_state.use_real_db)

db = get_database()

# Sidebar
with st.sidebar:
    st.title("🏥 MediTech")
    
    # การตั้งค่า
    st.header("⚙️ การตั้งค่า")
    db_mode = st.selectbox(
        "โหมดการเชื่อมต่อฐานข้อมูล",
        ["Demo Mode", "Production Mode"],
        index=0
    )
    
    st.session_state.dark_mode = st.toggle("โหมดกลางคืน", st.session_state.dark_mode)
    st.session_state.font_size = st.slider("ขนาดตัวอักษร", 12, 24, st.session_state.font_size)
    
    # เมนูหลัก
    st.header("📋 เมนูหลัก")
    demo_section = st.radio(
        "เลือกส่วนที่ต้องการสาธิต",
        ["Dashboard", "AI Diagnosis", "Patient Management", "Appointments", "Reports"]
    )

# ปรับโหมดการเชื่อมต่อฐานข้อมูล
if db_mode == "Production Mode" and not st.session_state.use_real_db:
    st.session_state.use_real_db = True
    st.experimental_rerun()
elif db_mode == "Demo Mode" and st.session_state.use_real_db:
    st.session_state.use_real_db = False
    st.experimental_rerun()

# แสดงเนื้อหาตามเมนูที่เลือก
if demo_section == "Dashboard":
    st.header("📊 Dashboard")
    
    # สถิติสำคัญ
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("ผู้ป่วยทั้งหมด", "1,234", "+12")
    with col2:
        st.metric("นัดหมายวันนี้", "45", "+5")
    with col3:
        st.metric("รอดำเนินการ", "12", "-3")
    with col4:
        st.metric("รายได้เดือนนี้", "฿123,456", "+15.2%")
    
    # กราฟและสถิติ
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("จำนวนผู้ป่วยรายเดือน")
        monthly_data = pd.DataFrame({
            "เดือน": pd.date_range(start="2024-01-01", periods=6, freq="M"),
            "จำนวน": [120, 150, 140, 160, 180, 200]
        })
        fig = px.line(monthly_data, x="เดือน", y="จำนวน")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("สัดส่วนประเภทการตรวจ")
        exam_data = pd.DataFrame({
            "ประเภท": ["ตรวจทั่วไป", "ตรวจเฉพาะทาง", "ติดตามผล", "ฉุกเฉิน"],
            "จำนวน": [45, 25, 20, 10]
        })
        fig = px.pie(exam_data, values="จำนวน", names="ประเภท")
        st.plotly_chart(fig, use_container_width=True)
    
    # ตารางนัดหมายวันนี้
    st.subheader("📅 นัดหมายวันนี้")
    appointments = db.get_appointments(datetime.now().date())
    if appointments:
        appointments_df = pd.DataFrame([
            {
                "เวลา": "10:00",
                "ผู้ป่วย": "นายสมชาย ใจดี",
                "ประเภท": a.type.value,
                "สถานะ": a.status.value
            }
            for a in appointments
        ])
        st.dataframe(appointments_df, use_container_width=True)
    else:
        st.info("ไม่มีนัดหมายวันนี้")

elif demo_section == "AI Diagnosis":
    st.title("🤖 AI Diagnosis System")
    
    # แบ่งหน้าจอเป็น 2 ส่วน
    input_col, result_col = st.columns([1, 1])
    
    with input_col:
        st.subheader("กรอกข้อมูลอาการ")
        
        # ฟอร์มกรอกข้อมูล
        symptoms = st.text_area(
            "อาการที่พบ",
            placeholder="กรอกอาการที่พบ แยกแต่ละอาการด้วยเครื่องหมาย ,",
            help="เช่น: ไข้, ปวดหัว, ไอ"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("อายุ", 0, 150, 25)
        with col2:
            gender = st.selectbox("เพศ", ["ชาย", "หญิง", "อื่นๆ"])
        
        duration = st.slider("ระยะเวลาที่มีอาการ (วัน)", 0, 30, 1)
        
        medical_history = st.text_area(
            "ประวัติการรักษาที่เกี่ยวข้อง (ถ้ามี)",
            placeholder="ระบุประวัติการรักษาที่เกี่ยวข้อง"
        )
        
        if st.button("วินิจฉัย", type="primary"):
            with result_col:
                st.subheader("ผลการวินิจฉัยเบื้องต้น")
                
                # จำลองการประมวลผล
                with st.spinner("กำลังวิเคราะห์..."):
                    st.progress(100)
                    
                    # ตัวอย่างผลการวินิจฉัย
                    st.write("### โรคที่เป็นไปได้:")
                    conditions = [
                        "ไข้หวัดทั่วไป (Common Cold)",
                        "ไข้หวัดใหญ่ (Influenza)",
                        "ภูมิแพ้ (Allergic Rhinitis)"
                    ]
                    for c in conditions:
                        st.write(f"- {c}")
                    
                    st.write("### ระดับความเชื่อมั่น:")
                    st.progress(85)
                    st.write("85%")
                    
                    st.write("### คำแนะนำ:")
                    st.info("""
                    1. ควรพักผ่อนให้เพียงพอ
                    2. ดื่มน้ำมากๆ
                    3. หากอาการไม่ดีขึ้นภายใน 3 วัน ควรพบแพทย์
                    """)
                    
                    # แสดงคำเตือนถ้าพบสัญญาณอันตราย
                    if "หายใจลำบาก" in symptoms:
                        st.error("""
                        ⚠️ พบสัญญาณอันตราย:
                        อาการหายใจลำบากเป็นสัญญาณอันตราย ควรพบแพทย์โดยด่วน
                        """)
    
    # คำเตือนด้านล่าง
    st.warning("""
    ⚠️ คำเตือน: ระบบนี้ให้การวินิจฉัยเบื้องต้นเท่านั้น ไม่สามารถใช้แทนการตรวจวินิจฉัยโดยแพทย์ได้
    หากมีอาการรุนแรงหรือเป็นมากขึ้น กรุณาพบแพทย์โดยด่วน
    """)

elif demo_section == "Patient Management":
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

elif demo_section == "Appointments":
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

elif demo_section == "Reports":
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