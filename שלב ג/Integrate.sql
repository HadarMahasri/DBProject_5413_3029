/*
 * אינטגרציה מלאה של מערכת מידע רפואי ומערכת מידע צבאית
 * שמירה על שמות העמודות המקוריים: commander_id, paramedic_id, patient_id
 * 
 * טווחי מזהים:
 * - מפקדים: 1,000,000 + מזהה מקורי
 * - פרמדיקים: 2,000,000 + מזהה מקורי
 * - מטופלים: 3,000,000 + מזהה מקורי
 */



-- ====== חלק 1: יצירת טבלת Soldier ======
CREATE TABLE IF NOT EXISTS Soldier (
    soldier_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    PRIMARY KEY (soldier_id)
);

-- ====== חלק 2: עדכון טבלת Commander (שמירה על commander_id) ======
-- הסרת המפתח הזר מ-Operation
ALTER TABLE Operation DROP CONSTRAINT IF EXISTS operation_id_fkey;

-- הסרת המפתח הראשי מ-Commander
ALTER TABLE Commander DROP CONSTRAINT IF EXISTS commander_pkey;

-- הוספת המפקדים לטבלת Soldier
INSERT INTO Soldier (soldier_id, name)
SELECT id + 1000000, Name
FROM Commander;

-- עדכון המזהים בטבלת Commander
UPDATE Commander SET id = id + 1000000;

-- הוספת מפתח ראשי מחדש
ALTER TABLE Commander ADD CONSTRAINT commander_pkey PRIMARY KEY (id);

-- עדכון המזהים בטבלת Operation
UPDATE Operation SET ID = ID + 1000000;

-- הוספת המפתח הזר מחדש
ALTER TABLE Operation ADD CONSTRAINT fk_operation_commander
    FOREIGN KEY (ID) REFERENCES Commander(id);

-- קישור Commander ל-Soldier
ALTER TABLE Commander ADD CONSTRAINT fk_commander_soldier
    FOREIGN KEY (id) REFERENCES Soldier(soldier_id);

-- ====== חלק 3: עדכון טבלת Paramedic (שמירה על paramedic_id) ======
-- הסרת המפתח הזר מ-Treatment
ALTER TABLE Treatment DROP CONSTRAINT IF EXISTS treatment_paramedic_id_fkey;

-- הסרת המפתח הראשי מ-Paramedic
ALTER TABLE Paramedic DROP CONSTRAINT IF EXISTS paramedic_pkey;

-- הוספת הפרמדיקים לטבלת Soldier
INSERT INTO Soldier (soldier_id, name)
SELECT paramedic_id + 2000000, paramedic_name
FROM Paramedic;

-- עדכון המזהים בטבלת Paramedic
UPDATE Paramedic SET paramedic_id = paramedic_id + 2000000;

-- הוספת מפתח ראשי מחדש
ALTER TABLE Paramedic ADD CONSTRAINT paramedic_pkey PRIMARY KEY (paramedic_id);

-- עדכון המזהים בטבלת Treatment
UPDATE Treatment SET paramedic_id = paramedic_id + 2000000;

-- הוספת המפתח הזר מחדש
ALTER TABLE Treatment ADD CONSTRAINT fk_treatment_paramedic
    FOREIGN KEY (paramedic_id) REFERENCES Paramedic(paramedic_id);

-- קישור Paramedic ל-Soldier
ALTER TABLE Paramedic ADD CONSTRAINT fk_paramedic_soldier
    FOREIGN KEY (paramedic_id) REFERENCES Soldier(soldier_id);

-- ====== חלק 4: עדכון טבלת Patient (שמירה על patient_id) ======
-- הסרת המפתח הזר מ-receives_treatment
ALTER TABLE receives_treatment DROP CONSTRAINT IF EXISTS receives_treatment_patient_id_fkey;

-- הסרת המפתח הראשי מ-Patient
ALTER TABLE Patient DROP CONSTRAINT IF EXISTS patient_pkey;

-- הוספת המטופלים לטבלת Soldier (רק חיילים)
INSERT INTO Soldier (soldier_id, name)
SELECT patient_id + 3000000, patient_name
FROM Patient


-- עדכון המזהים בטבלת Patient
UPDATE Patient SET patient_id = patient_id + 3000000;

-- הוספת מפתח ראשי מחדש
ALTER TABLE Patient ADD CONSTRAINT patient_pkey PRIMARY KEY (patient_id);

-- עדכון המזהים בטבלת receives_treatment
UPDATE receives_treatment SET patient_id = patient_id + 3000000;

-- הוספת המפתח הזר מחדש
ALTER TABLE receives_treatment ADD CONSTRAINT fk_receives_treatment_patient
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id);

-- קישור Patient ל-Soldier (רק חיילים)
ALTER TABLE Patient ADD CONSTRAINT fk_patient_soldier
    FOREIGN KEY (patient_id) REFERENCES Soldier(soldier_id)
   

-- ====== חלק 5: מיזוג טבלאות ציוד עם מפתח מורכב ======
-- הסרת מפתחות זרים שמצביעים לטבלת Equipment
ALTER TABLE uses DROP CONSTRAINT IF EXISTS uses_equipment_id_fkey;
ALTER TABLE Requires DROP CONSTRAINT IF EXISTS requires_equipmentid_fkey;

-- הסרת המפתח הראשי הקיים מטבלת Equipment
ALTER TABLE Equipment DROP CONSTRAINT IF EXISTS equipment_pkey;

-- הוספת עמודת סוג ציוד לטבלת Equipment
ALTER TABLE Equipment ADD COLUMN IF NOT EXISTS equipment_type VARCHAR(20) DEFAULT 'Military';

-- הוספת מפתח ראשי מורכב לטבלת Equipment
ALTER TABLE Equipment ADD CONSTRAINT equipment_pkey PRIMARY KEY (EquipmentID, equipment_type);

-- הכנסת ציוד רפואי לטבלת הציוד המאוחדת (ללא שינוי במזהים)
INSERT INTO Equipment (EquipmentID, Name, Quantity, equipment_type)
SELECT equipment_id, equipment_name, quantity_, 'Medical'
FROM Medical_equipment;

-- עדכון טבלת uses
-- הוספת עמודת equipment_type לטבלת uses
ALTER TABLE uses ADD COLUMN IF NOT EXISTS equipment_type VARCHAR(20) DEFAULT 'Military';

-- עדכון ערכי equipment_type לציוד רפואי
UPDATE uses SET equipment_type = 'Medical'
WHERE equipment_id IN (SELECT equipment_id FROM Medical_equipment);

-- הוספת המפתח הזר החדש לטבלת uses
ALTER TABLE uses ADD CONSTRAINT uses_equipment_fkey
    FOREIGN KEY (equipment_id, equipment_type) REFERENCES Equipment(EquipmentID, equipment_type);

-- עדכון טבלת Requires
-- הוספת עמודת equipment_type לטבלת Requires
ALTER TABLE Requires ADD COLUMN IF NOT EXISTS equipment_type VARCHAR(20) DEFAULT 'Military';

-- הוספת המפתח הזר החדש לטבלת Requires
ALTER TABLE Requires ADD CONSTRAINT requires_equipment_fkey
    FOREIGN KEY (EquipmentID, equipment_type) REFERENCES Equipment(EquipmentID, equipment_type);

-- מחיקת טבלת Medical_equipment שכבר לא נדרשת
DROP TABLE IF EXISTS Medical_equipment;

-- ====== חלק 6: קישור בין אירועים רפואיים למבצעים ======
-- הוספת עמודת operation_id לטבלת Medical_event (אם עדיין לא קיימת)
ALTER TABLE Medical_event ADD COLUMN IF NOT EXISTS operation_id INT;

-- עדכון הקשרים לפי תאריכים
UPDATE Medical_event
SET operation_id = Operation.OperationID
FROM Operation
WHERE Medical_event.event_date BETWEEN Operation.startDate AND Operation.endDate
  AND Medical_event.operation_id IS NULL;

-- הוספת אילוץ מפתח זר
ALTER TABLE Medical_event ADD CONSTRAINT fk_medical_event_operation
    FOREIGN KEY (operation_id) REFERENCES Operation(OperationID);

-- ====== חלק 7: הוספת אילוצים לשמירה על שלמות נתונים ======

-- הגבלות על סוג הציוד
ALTER TABLE Equipment DROP CONSTRAINT IF EXISTS chk_equipment_type;
ALTER TABLE Equipment ADD CONSTRAINT chk_equipment_type
    CHECK (equipment_type IN ('Military', 'Medical'));


