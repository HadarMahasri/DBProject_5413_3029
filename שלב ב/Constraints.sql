
-- ===== אילוצי NOT NULL =====

-- בדיקת אילוץ NOT NULL על OperationName בטבלת Operation
-- הפעלת האילוץ:
ALTER TABLE Operation ALTER COLUMN OperationName SET NOT NULL;

-- ניסיון להכניס שורה עם ערך NULL בשדה OperationName (יגרום לשגיאה)
INSERT INTO Operation (OperationID, OperationName, startDate, endDate, Location, ID)
VALUES (501, NULL, CURRENT_DATE, NULL, 'דרום', 1);

-- ===== אילוצי CHECK =====

-- יצירת אילוץ CHECK - תאריך סיום המבצע חייב להיות אחרי תאריך ההתחלה
ALTER TABLE Operation ADD CONSTRAINT check_operation_dates 
CHECK (endDate IS NULL OR endDate >= startDate);

-- ניסיון להכניס שורה עם תאריך סיום לפני תאריך התחלה (יגרום לשגיאה)
INSERT INTO Operation (OperationID, OperationName, startDate, endDate, Location, ID)
VALUES (504, 'מבצע שגוי', '2023-05-15', '2023-05-01', 'מרכז', 1);


-- יצירת אילוץ CHECK - דרגת המפקד חייבת להיות אחת מהדרגות המאושרות
ALTER TABLE Commander ADD CONSTRAINT cmd_rnk_check
CHECK (Rank IN ('Captain', 'Major', 'Corporal', 'Private', 'Lieutenant', 'General', 'Sergeant'));


-- ניסיון להכניס שורה עם דרגה שאינה ברשימה (יגרום לשגיאה)
INSERT INTO Commander (ID, Name, Rank, ExperienceYears)
VALUES (501, 'משה כהן', 'Admiral', 10);

-- ===== אילוצי DEFAULT =====

-- יצירת אילוץ DEFAULT - כמות ציוד נדרשת ברירת מחדל ל-500
ALTER TABLE Requires ALTER COLUMN RequiredQuantity SET DEFAULT 500;

-- הכנסת שורה ללא ציון כמות - תוכנס כמות ברירת המחדל (500)
INSERT INTO Requires (EquipmentID, OperationID)
VALUES (1, 1);

-- בדיקה שהכמות הוכנסה כברירת מחדל (צריך להיות 500)
SELECT * FROM Requires WHERE EquipmentID = 1 AND OperationID = 1;


