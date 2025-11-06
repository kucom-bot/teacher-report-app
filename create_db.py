# ไฟล์: create_db.py
import sqlite3
from faker import Faker

# --- ส่วนของการตั้งค่า ---
DB_FILE = "school_report.db"
COMPETENCIES = [
    "ความสามารถด้านการสื่อสาร",
    "ความสามารถด้านการคิด",
    "ความสามารถด้านการแก้ปัญหา",
    "ความสามารถด้านการใช้ทักษะชีวิต",
    "ความสามารถด้านการใช้เทคโนโลยี",
    "ความสามารถด้านความร่วมมือ",
    "ความสามารถด้านการสร้างสรรค์",
    "ความสามารถด้านสุขภาวะ"
]
BEHAVIOR_BANK_DATA = {
    # ตัวอย่างแค่ 2 สมรรถนะก่อนนะครับ สามารถเพิ่มเติมได้ตามรูปแบบนี้
    1: { # ID ของสมรรถนะข้อที่ 1
        "เชี่ยวชาญ": "สื่อสารสองภาษาได้อย่างคล่องแคล่ว นำเสนอข้อมูลซับซ้อนได้น่าสนใจ",
        "ชำนาญ": "เลือกใช้ภาษาและวิธีการสื่อสารได้เหมาะสมกับบุคคลและสถานการณ์",
        "พัฒนา": "สามารถสื่อสาร ถ่ายทอดความคิด ความรู้สึกของตนเองได้",
        "เริ่มต้น": "รับสารและส่งสารด้วยภาษาไทยเบื้องต้นได้",
    },
    2: { # ID ของสมรรถนะข้อที่ 2
        "เชี่ยวชาญ": "คิดวิเคราะห์ สังเคราะห์ และประเมินข้อมูลเพื่อตัดสินใจแก้ปัญหาที่ซับซ้อนได้",
        "ชำนาญ": "สามารถจำแนก แยกแยะ เปรียบเทียบข้อมูล และให้เหตุผลได้",
        "พัฒนา": "สามารถสรุปใจความสำคัญจากเรื่องที่ฟังและอ่านได้",
        "เริ่มต้น": "บอกหรือเล่าเรื่องราวจากสิ่งที่พบเห็นได้",
    }
}

# --- ส่วนของการสร้างฐานข้อมูล ---
def create_database():
    print("กำลังสร้างฐานข้อมูล...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 1. ตารางนักเรียน
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL
    )''')

    # 2. ตารางสมรรถนะ 8 ข้อ
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS competencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )''')

    # 3. ตารางคลังพฤติกรรม
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS behavior_bank (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        competency_id INTEGER,
        level TEXT NOT NULL,
        description TEXT NOT NULL,
        FOREIGN KEY (competency_id) REFERENCES competencies (id),
        UNIQUE (competency_id, level) -- <--- เพิ่มบรรทัดนี้
    )''')

    # 4. ตารางเก็บคะแนนดิบ (สำคัญมาก!)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        competency_id INTEGER,
        raw_score INTEGER NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (competency_id) REFERENCES competencies (id)
    )''')

    print("สร้างตารางสำเร็จ!")
    conn.commit()
    conn.close()

# --- ส่วนของการใส่ข้อมูลตัวอย่าง ---
def populate_data():
    print("กำลังเพิ่มข้อมูลตัวอย่าง...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    fake = Faker('th_TH') # สร้างข้อมูลชื่อภาษาไทย

    # เพิ่มสมรรถนะ 8 ข้อ
    if cursor.execute("SELECT COUNT(*) FROM competencies").fetchone()[0] == 0:
        for c in COMPETENCIES:
            cursor.execute("INSERT INTO competencies (name) VALUES (?)", (c,))
        print("- เพิ่มข้อมูลสมรรถนะ 8 ข้อแล้ว")

    # เพิ่มคลังพฤติกรรม
    if cursor.execute("SELECT COUNT(*) FROM behavior_bank").fetchone()[0] == 0:
        for comp_id, levels in BEHAVIOR_BANK_DATA.items():
            for level, desc in levels.items():
                cursor.execute("INSERT INTO behavior_bank (competency_id, level, description) VALUES (?, ?, ?)",
                             (comp_id, level, desc))
        print("- เพิ่มข้อมูลคลังพฤติกรรมแล้ว")

    # เพิ่มรายชื่อนักเรียนตัวอย่าง 20 คน
    if cursor.execute("SELECT COUNT(*) FROM students").fetchone()[0] == 0:
        for i in range(20):
            student_id = f"66{i+1:03d}"
            full_name = fake.name()
            cursor.execute("INSERT INTO students (student_id, full_name) VALUES (?, ?)", (student_id, full_name))
        print("- เพิ่มข้อมูลนักเรียนตัวอย่าง 20 คนแล้ว")

    conn.commit()
    conn.close()
    print("เพิ่มข้อมูลตัวอย่างสำเร็จ!")

# --- สั่งให้โปรแกรมทำงาน ---
if __name__ == "__main__":
    create_database()
    populate_data()
    print(f"\nฐานข้อมูล '{DB_FILE}' พร้อมใช้งานแล้ว!")