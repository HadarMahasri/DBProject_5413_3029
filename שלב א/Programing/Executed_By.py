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