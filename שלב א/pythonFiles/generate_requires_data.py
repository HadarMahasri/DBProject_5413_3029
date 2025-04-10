import csv
import random

# מספר רשומות ליצירה
NUM_RECORDS = 400

# יצירת רשומות אקראיות עבור טבלת Requires (קשר בין ציוד למבצע)
data_requires = []
for _ in range(NUM_RECORDS):
    equipment_id = random.randint(1, 100)       # מזהה ציוד
    operation_id = random.randint(1, 50)        # מזהה מבצע
    required_quantity = random.randint(1, 10)   # כמות נדרשת
    data_requires.append([equipment_id, operation_id, required_quantity])

# שמירה לקובץ CSV
csv_filename_requires = "requires_data.csv"
with open(csv_filename_requires, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["EquipmentID", "OperationID", "RequiredQuantity"])  # כותרות העמודות
    writer.writerows(data_requires)

print(f"✅ Requires data with quantity successfully saved to {csv_filename_requires}")
