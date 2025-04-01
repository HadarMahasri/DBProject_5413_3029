import csv
import random

# מספר רשומות ליצירה
NUM_RECORDS = 400

# יצירת רשומות אקראיות עבור טבלת Requires (קשר בין ציוד למבצע)
data_requires = []
for _ in range(NUM_RECORDS):
    equipment_id = random.randint(1, 100)  # מזהה ציוד קיים מתוך 100
    operation_id = random.randint(1, 50)  # מזהה מבצע קיים מתוך 50
    data_requires.append([equipment_id, operation_id])

# שמירה לקובץ CSV
csv_filename_requires = "requires_data.csv"
with open(csv_filename_requires, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["EquipmentID", "OperationID"])  # כותרות העמודות
    writer.writerows(data_requires)

print(f"✅ Requires data successfully saved to {csv_filename_requires}")
