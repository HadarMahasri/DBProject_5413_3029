import csv
import random
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/Operations Branch"

# יצירת מנוע SQLAlchemy
engine = create_engine(DATABASE_URL)

# טווח מזהים אמיתיים לפי הנתונים הקיימים
operation_ids = list(range(1, 401))
unit_ids = list(range(1, 401))
corps_ids = list(range(1, 401))

# רשימה לשמירת הנתונים
executed_by_data = []

# יצירת קובץ CSV
with open("executed_by.csv", mode="w", newline="") as file:
    writer = csv.writer(file)

    # כתיבת כותרות העמודות
    writer.writerow(["OperationID", "UnitID", "CorpsID"])

    # יצירת 400 רשומות תקינות
    for _ in range(400):
        operation_id = random.choice(operation_ids)
        unit_id = random.choice(unit_ids)
        corps_id = random.choice(corps_ids)

        # כתיבה לקובץ CSV
        writer.writerow([operation_id, unit_id, corps_id])

        # שמירת הנתונים גם לרשימה לצורך הכנסה לבסיס הנתונים
        executed_by_data.append({
            "op_id": operation_id,
            "unit_id": unit_id,
            "corps_id": corps_id
        })

print("✅ קובץ CSV 'executed_by.csv' נוצר בהצלחה!")

# העלאת הנתונים לבסיס הנתונים
try:
    # בדיקת חיבור לבסיס הנתונים
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.scalar()
        print(f"PostgreSQL Version: {version}")
        print("✅ התחברות למסד הנתונים הצליחה!")

        # ניקוי טבלה קיימת (אופציונלי - הסר אם אתה רוצה להוסיף לנתונים קיימים)
        connection.execute(text("TRUNCATE TABLE executed_by CASCADE"))
        connection.commit()
        print("✅ טבלת Executed_by נוקתה בהצלחה")

        # הכנסת הנתונים בקבוצות של 50
        batch_size = 50
        for i in range(0, len(executed_by_data), batch_size):
            batch = executed_by_data[i:i + batch_size]

            # הכנסת האצווה לבסיס הנתונים
            stmt = text("""
                INSERT INTO executed_by (operationid, unitid, corpsid)
                VALUES (:op_id, :unit_id, :corps_id)
            """)

            connection.execute(stmt, batch)
            connection.commit()
            print(f"✅ הוכנסו {min(i + batch_size, len(executed_by_data))} רשומות Executed_by...")

        print(f"✅ סה\"כ הוכנסו בהצלחה {len(executed_by_data)} רשומות לטבלת Executed_by!")

except Exception as e:
    print(f"❌ שגיאה בחיבור למסד הנתונים או בהכנסת הנתונים: {e}")