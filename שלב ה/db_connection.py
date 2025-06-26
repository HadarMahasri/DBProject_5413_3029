# db_connection.py - Updated for Single Window System
import psycopg2
from tkinter import messagebox

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        
        # הגדרות חיבור - בדיוק כמו בקובץ העובד
        self.db_config = {
            "dbname": "Integration",
            "user": "myuser",
            "password": "mypassword",
            "host": "localhost",
            "port": "5432"
        }
    
    def connect(self):
        """Connect to PostgreSQL database - רק התחברות לבסיס הנתונים הקיים"""
        try:
            print("מנסה להתחבר לבסיס נתונים...")
            self.connection = psycopg2.connect(**self.db_config)
            print("✅ חיבור בוצע בהצלחה!")
            
            # בדיקה שהחיבור עובד
            cur = self.connection.cursor()
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"גרסת PostgreSQL: {version[0]}")
            cur.close()
            
            return True
            
        except Exception as e:
            print(f"❌ שגיאה בחיבור: {str(e)}")
            # הסרת messagebox מכאן כי זה יכול לגרום לבעיות בחלון יחיד
            return False
    
    def disconnect(self):
        """Disconnect from database"""
        if self.connection:
            try:
                self.connection.close()
                print("❌ החיבור לבסיס הנתונים נסגר")
            except Exception as e:
                print(f"שגיאה בסגירת החיבור: {str(e)}")
    
    def is_connected(self):
        """בדיקה אם החיבור פעיל"""
        try:
            if self.connection and not self.connection.closed:
                # בדיקה מהירה של החיבור
                cur = self.connection.cursor()
                cur.execute("SELECT 1;")
                cur.fetchone()
                cur.close()
                return True
            return False
        except:
            return False
    
    def execute_query(self, query, params=None):
        """Execute SQL query with better error handling"""
        try:
            # וידוא שהחיבור פעיל
            if not self.is_connected():
                if not self.connect():
                    raise Exception("לא ניתן להתחבר לבסיס הנתונים")
            
            cur = self.connection.cursor()
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
                        
            if query.strip().upper().startswith('SELECT'):
                result = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                cur.close()
                return result, columns
            else:
                self.connection.commit()
                affected_rows = cur.rowcount
                cur.close()
                return affected_rows, None
                
        except Exception as e:
            if hasattr(self, 'connection') and self.connection:
                self.connection.rollback()
            print(f"❌ שגיאה בביצוע שאילתה: {str(e)}")
            raise e
    
    def get_table_data(self, table_name, limit=None):
        """Get data from specific table"""
        try:
            query = f"SELECT * FROM {table_name}" if limit is None else f"SELECT * FROM {table_name} LIMIT {limit}"
            return self.execute_query(query)
        except Exception as e:
            print(f"❌ שגיאה בטעינת נתונים מטבלת {table_name}: {str(e)}")
            raise e
        
    def insert_record(self, table_name, fields, values):
        """Insert new record with better validation"""
        try:
            # סינון ערכים ריקים
            filtered_fields = []
            filtered_values = []
            
            for field, value in zip(fields, values):
                if value is not None and str(value).strip():
                    filtered_fields.append(field)
                    filtered_values.append(value)
            
            if not filtered_fields:
                raise Exception("לא ניתן להוסיף רשומה ללא נתונים")
            
            placeholders = ', '.join(['%s'] * len(filtered_values))
            field_names = ', '.join(filtered_fields)
            query = f"INSERT INTO {table_name} ({field_names}) VALUES ({placeholders})"
            
            return self.execute_query(query, filtered_values)
            
        except Exception as e:
            print(f"❌ שגיאה בהוספת רשומה לטבלת {table_name}: {str(e)}")
            raise e
    
    def update_record(self, table, primary_key, pk_value, fields, values):
        set_clause = ', '.join([f"{field} = %s" for field in fields])
        query = f"UPDATE {table} SET {set_clause} WHERE {primary_key} = %s"
        params = values + [pk_value]
        return self.execute_query(query, params)
    
    def update_record_composite(self, table_name, pk_fields, pk_values, update_fields, update_values):
        try:
            set_clause = ", ".join([f"{field} = %s" for field in update_fields])
            where_clause = " AND ".join([f"{field} = %s" for field in pk_fields])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
            values = update_values + pk_values
            return self.execute_query(query, values)
        except Exception as e:
            print(f"שגיאה בעדכון רשומה עם מפתח מורכב: {e}")
            raise e

    
    def check_related_records(self, table_name, primary_key, pk_value):
        """בודק אילו רשומות קשורות קיימות - מחזיר רק אם יש תלויות"""
        try:
            cur = self.connection.cursor()
            related_records = {}
            
            if table_name == "equipment":
                # בדיקה בטבלת requires
                try:
                    cur.execute("SELECT COUNT(*) FROM requires WHERE equipmentId = %s", (pk_value,))
                    requires_count = cur.fetchone()[0]
                    if requires_count > 0:
                        related_records["requires"] = requires_count
                except Exception as e:
                    print(f"⚠️ לא ניתן לבדוק טבלת requires: {e}")
                
                # בדיקה בטבלת uses
                try:
                    cur.execute("SELECT COUNT(*) FROM uses WHERE equipment_id = %s", (pk_value,))
                    uses_count = cur.fetchone()[0]
                    if uses_count > 0:
                        related_records["uses"] = uses_count
                except Exception as e:
                    print(f"⚠️ לא ניתן לבדוק טבלת uses: {e}")
            
            elif table_name == "medical_event":
                # בדיקה אם יש קשרים לאירועים רפואיים
                try:
                    cur.execute("SELECT COUNT(*) FROM uses WHERE treatment_id IN (SELECT treatment_id FROM treatment WHERE event_id = %s)", (pk_value,))
                    uses_count = cur.fetchone()[0]
                    if uses_count > 0:
                        related_records["uses"] = uses_count
                except Exception as e:
                    print(f"⚠️ לא ניתן לבדוק קשרים רפואיים: {e}")
            
            cur.close()
            return related_records
            
        except Exception as e:
            print(f"❌ שגיאה בבדיקת תלויות: {e}")
            return {}
    
    def delete_record_safe(self, table_name, primary_key, pk_value):
        """מחיקה בטוחה - רק אם אין תלויות"""
        try:
            # בדיקת תלויות לפני מחיקה
            related_records = self.check_related_records(table_name, primary_key, pk_value)
            
            if related_records:
                # יש תלויות - לא ניתן למחוק
                deps_text = f"❌ לא ניתן למחוק את הרשומה {pk_value}\n\n"
                deps_text += "נמצאו תלויות בטבלאות הבאות:\n"
                
                for table, count in related_records.items():
                    deps_text += f"• {table}: {count} רשומות\n"
                
                deps_text += "\n💡 מחק קודם את הרשומות התלויות ואז נסה שוב."
                
                # החזרת מידע על התלויות במקום הצגת messagebox
                return 0, "יש תלויות"
            
            # אין תלויות - ניתן למחוק
            cur = self.connection.cursor()
            query = f"DELETE FROM {table_name} WHERE {primary_key} = %s"
            cur.execute(query, (pk_value,))
            
            rows_affected = cur.rowcount
            self.connection.commit()
            cur.close()
            
            if rows_affected > 0:
                print(f"✅ נמחקה הרשומה {pk_value} מטבלת {table_name}")
            
            return rows_affected, None
            
        except Exception as e:
            if hasattr(self, 'connection') and self.connection:
                self.connection.rollback()
            print(f"❌ שגיאה במחיקה: {e}")
            raise e
    
    def delete_record(self, table_name, primary_key, pk_value):
        """מחיקה רגילה - ללא בדיקת תלויות (לטבלאות שאין להן תלויות)"""
        try:
            cur = self.connection.cursor()
            query = f"DELETE FROM {table_name} WHERE {primary_key} = %s"
            cur.execute(query, (pk_value,))
            
            rows_affected = cur.rowcount
            self.connection.commit()
            cur.close()
            
            return rows_affected, None
            
        except Exception as e:
            if hasattr(self, 'connection') and self.connection:
                self.connection.rollback()
            print(f"❌ שגיאה במחיקה: {e}")
            raise e
    
    def search_records(self, table_name, conditions, values):
        """Search records with conditions"""
        try:
            where_clause = ' AND '.join(conditions)
            query = f"SELECT * FROM {table_name} WHERE {where_clause}"
            return self.execute_query(query, values)
        except Exception as e:
            print(f"❌ שגיאה בחיפוש בטבלת {table_name}: {str(e)}")
            raise e
    
    def get_table_info(self, table_name):
        """קבלת מידע על טבלה - עמודות וסוגי נתונים"""
        try:
            query = """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = %s
            ORDER BY ordinal_position;
            """
            return self.execute_query(query, (table_name,))
        except Exception as e:
            print(f"❌ שגיאה בקבלת מידע על טבלת {table_name}: {str(e)}")
            raise e
    
    def test_connection(self):
        """בדיקת חיבור מפורטת"""
        try:
            if self.connect():
                # בדיקת גישה לטבלאות
                test_queries = [
                    "SELECT COUNT(*) FROM equipment;",
                    "SELECT COUNT(*) FROM medical_event;",
                    "SELECT COUNT(*) FROM requires;",
                    "SELECT COUNT(*) FROM uses;"
                ]
                
                results = {}
                for query in test_queries:
                    try:
                        table_name = query.split("FROM ")[1].split(";")[0].strip()
                        result, _ = self.execute_query(query)
                        results[table_name] = result[0][0] if result else 0
                    except Exception as e:
                        results[table_name] = f"שגיאה: {str(e)}"
                
                self.disconnect()
                return True, results
            else:
                return False, "לא ניתן להתחבר לבסיס הנתונים"
                
        except Exception as e:
            return False, f"שגיאה בבדיקת החיבור: {str(e)}"
  