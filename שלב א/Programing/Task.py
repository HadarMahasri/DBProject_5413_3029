import csv
import random
from datetime import datetime, timedelta, time
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/Operations Branch"

# יצירת מנוע SQLAlchemy
engine = create_engine(DATABASE_URL)

# טווח מזהים אמיתיים לפי הנתונים הקיימים
operation_ids = list(range(1, 401))

# רשימת סוגי משימות
task_types = [
    "סיור שטח", "איסוף מודיעין", "פינוי שטח", "אבטחת אזור",
    "חיפוש מטרות", "הקמת מחסום", "פעילות יזומה", "סריקת מבנים",
    "ליווי שיירה", "חילוץ והצלה", "אבטחת אישיות", "פשיטה",
    "מארב", "לחימה בשטח בנוי", "פינוי אוכלוסייה", "אבטחת גבול",
    "סיוע הומניטרי", "תצפית", "פינוי פצועים", "אבטחת אירוע"
]

# רשימה לשמירת הנתונים
task_data = []

# יצירת תאריכים בטווח 2023-01-01 עד 2023-12-31
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = (end_date - start_date).days

# יצירת קובץ CSV
with open("task.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # כתיבת כותרות העמודות
    writer.writerow(["TaskID", "Task", "Date", "StartTime", "EndTime", "OperationID"])

    # יצירת 400 רשומות תקינות
    for i in range(1, 401):
        # יצירת תאריך אקראי
        random_days = random.randint(0, date_range)
        task_date = start_date + timedelta(days=random_days)

        # יצירת זמני התחלה וסיום אקראיים
        start_hour = random.randint(6, 20)
        start_minute = random.randint(0, 59)
        start_time_obj = time(start_hour, start_minute)

        # משך משימה בין שעה ל-8 שעות
        task_duration = random.randint(1, 8)
        end_hour = min(start_hour + task_duration, 23)
        end_minute = random.randint(0, 59)
        end_time_obj = time(end_hour, end_minute)

        # בחירת מבצע אקראי
        operation_id = random.choice(operation_ids)

        # יצירת שם משימה
        task_type = random.choice(task_types)
        task_suffix = f"באזור {random.choice(['צפון', 'דרום', 'מרכז', 'מזרח', 'מערב'])}"
        task_name = f"{task_type} {task_suffix}"

        # כתיבה לקובץ CSV
        writer.writerow([
            i,  # TaskID
            task_name,
            task_date.strftime("%Y-%m-%d"),
            start_time_obj.strftime("%H:%M:%S"),
            end_time_obj.strftime("%H:%M:%S"),
            operation_id
        ])

        # שמירת הנתונים גם לרשימה לצורך הכנסה לבסיס הנתונים
        task_data.append({
            "task_id": i,
            "task": task_name,
            "date": task_date,
            "start_time": start_time_obj,
            "end_time": end_time_obj,
            "op_id": operation_id
        })

print("✅ קובץ CSV 'task.csv' נוצר בהצלחה!")

# העלאת הנתונים לבסיס הנתונים
try:
    # בדיקת חיבור לבסיס הנתונים
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.scalar()
        print(f"PostgreSQL Version: {version}")
        print("✅ התחברות למסד הנתונים הצליחה!")

        # ניקוי טבלה קיימת (אופציונלי - הסר אם אתה רוצה להוסיף לנתונים קיימים)
        connection.execute(text("TRUNCATE TABLE task CASCADE"))
        connection.commit()
        print("✅ טבלת Task נוקתה בהצלחה")

        # הכנסת הנתונים בקבוצות של 50
        batch_size = 50
        for i in range(0, len(task_data), batch_size):
            batch = task_data[i:i + batch_size]

            # הכנסת האצווה לבסיס הנתונים
            stmt = text("""
                INSERT INTO task (taskid, task, date, starttime, endtime, operationid)
                VALUES (:task_id, :task, :date, :start_time, :end_time, :op_id)
            """)

            connection.execute(stmt, batch)
            connection.commit()
            print(f"✅ הוכנסו {min(i + batch_size, len(task_data))} רשומות Task...")

        print(f"✅ סה\"כ הוכנסו בהצלחה {len(task_data)} רשומות לטבלת Task!")

except Exception as e:
    print(f"❌ שגיאה בחיבור למסד הנתונים או בהכנסת הנתונים: {e}")