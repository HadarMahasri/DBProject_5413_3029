import csv
import random
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/Operations Branch"

# יצירת מנוע SQLAlchemy
engine = create_engine(DATABASE_URL)

# טווח מזהים אמיתיים לפי הנתונים הקיימים
operation_ids = list(range(1, 401))
equipment_ids = list(range(1, 401))

# רשימה לשמירת הנתונים
requires_data = []

# העלאת הנתונים לבסיס הנתונים
try:
    # בדיקת חיבור לבסיס הנתונים
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.scalar()
        print(f"PostgreSQL Version: {version}")
        print("✅ התחברות למסד הנתונים הצליחה!")

        # ניקוי טבלה קיימת (אופציונלי - הסר אם אתה רוצה להוסיף לנתונים קיימים)
        connection.execute(text("TRUNCATE TABLE requires CASCADE"))
        connection.commit()
        print("✅ טבלת Requires נוקתה בהצלחה")

        # הכנסת הנתונים בקבוצות של 50
        batch_size = 50
        for i in range(0, len(requires_data), batch_size):
            batch = requires_data[i:i + batch_size]

            # הכנסת האצווה לבסיס הנתונים
            stmt = text("""
                INSERT INTO requires (equipmentid, operationid, requiredquantity)
                VALUES (:equip_id, :op_id, :req_qty)
            """)

            connection.execute(stmt, batch)
            connection.commit()
            print(f"✅ הוכנסו {min(i + batch_size, len(requires_data))} רשומות Requires...")

        print(f"✅ סה\"כ הוכנסו בהצלחה {len(requires_data)} רשומות לטבלת Requires!")

except Exception as e:
    print(f"❌ שגיאה בחיבור למסד הנתונים או בהכנסת הנתונים: {e}")