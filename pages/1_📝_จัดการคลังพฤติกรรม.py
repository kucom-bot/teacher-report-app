# ไฟล์: pages/1_📝_จัดการคลังพฤติกรรม.py
import streamlit as st
import sqlite3
import pandas as pd

DB_FILE = "school_report.db"

def connect_db():
    return sqlite3.connect(DB_FILE)

st.set_page_config(layout="wide")
st.title("📝 จัดการคลังคำอธิบายพฤติกรรม")
st.info("หน้านี้สำหรับคุณครูเพื่อ เพิ่ม/แก้ไข/ลบ คำอธิบายพฤติกรรมที่จะนำไปใช้ในรายงาน")

conn = connect_db()
cursor = conn.cursor()

# ดึงข้อมูลสมรรถนะทั้งหมดมาให้ครูเลือก
competencies = pd.read_sql_query("SELECT id, name FROM competencies", conn)
comp_dict = pd.Series(competencies.name.values, index=competencies.id).to_dict()

st.header("1. เลือกเพื่อแก้ไข")

# สร้างคอลัมน์เพื่อให้จัดวางสวยงาม
col1, col2 = st.columns(2)

with col1:
    selected_comp_id = st.selectbox("เลือกสมรรถนะที่ต้องการแก้ไข:", options=list(comp_dict.keys()), format_func=lambda x: comp_dict[x])
with col2:
    selected_level = st.selectbox("เลือกระดับที่ต้องการแก้ไข:", options=["เชี่ยวชาญ", "ชำนาญ", "พัฒนา", "เริ่มต้น"])

# ค้นหาคำอธิบายเดิมจากฐานข้อมูล
cursor.execute("SELECT description FROM behavior_bank WHERE competency_id = ? AND level = ?", (selected_comp_id, selected_level))
result = cursor.fetchone()
current_description = result[0] if result else ""

st.header("2. กรอกคำอธิบายใหม่")
new_description = st.text_area("คำอธิบายพฤติกรรม:", value=current_description, height=150)

if st.button("💾 บันทึกการเปลี่ยนแปลง", type="primary"):
    if new_description:
        # ใช้คำสั่ง UPSERT เพื่อ: ถ้ามีข้อมูลอยู่แล้วให้ UPDATE, ถ้ายังไม่มีให้ INSERT
        cursor.execute("""
            INSERT INTO behavior_bank (competency_id, level, description)
            VALUES (?, ?, ?)
            ON CONFLICT(competency_id, level) DO UPDATE SET description=excluded.description
        """, (selected_comp_id, selected_level, new_description))
        conn.commit()
        st.success(f"บันทึกข้อมูลสำหรับ '{comp_dict[selected_comp_id]}' ระดับ '{selected_level}' เรียบร้อยแล้ว!")
    else:
        st.warning("กรุณากรอกคำอธิบายก่อนบันทึก")

conn.close()