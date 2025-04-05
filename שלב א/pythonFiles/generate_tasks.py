import csv
import random
from datetime import datetime, timedelta

# רשימת משימות אפשריות
tasks = [
    "Reconnaissance Mission", "Rescue Operation", "Supply Drop", "Combat Exercise",
    "Surveillance", "Target Elimination", "Defense Setup", "Intel Gathering",
    "Training Drill", "Border Patrol", "Night Raid", "Covert Infiltration",
    "Explosive Disposal", "Air Support", "Cyber Warfare Operation"
]

# יצירת נתונים עבור 400 משימות
with open("tasks_data.csv", mode="w", newline="") as file:
    writer = csv.writer(file)

    # כתיבת כותרות העמודות
    writer.writerow(["Task", "Date", "StartTime", "EndTime", "OperationID"])

    # יצירת 400 רשומות אקראיות
    for _ in range(400):
        task = random.choice(tasks)
        date = (datetime.today() - timedelta(days=random.randint(0, 365))).date()
        start_time = (datetime(2023, 1, 1, random.randint(0, 23), random.randint(0, 59))).time()
        end_time = (datetime(2023, 1, 1, random.randint(0, 23), random.randint(0, 59))).time()
        operation_id = random.randint(1, 50)  # מזהה מבצע אקראי בין 1 ל-50

        # כתיבת השורה לקובץ
        writer.writerow([task, date, start_time, end_time, operation_id])

print("✅ CSV file 'tasks_data.csv' created successfully!")
