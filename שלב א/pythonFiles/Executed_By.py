import csv
import random

# טווח מזהים אמיתיים לפי הנתונים הקיימים
operation_ids = list(range(1, 51))  # יש לנו 50 מבצעים
unit_ids = list(range(1, 101))      # יש לנו 100 יחידות
corps_ids = list(range(1, 11))      # יש לנו 10 חילות

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

        writer.writerow([operation_id, unit_id, corps_id])

print("✅ CSV file 'executed_by.csv' created successfully!")
