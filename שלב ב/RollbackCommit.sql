-- RollbackCommit.sql
-- קובץ המדגים שימוש בפקודות COMMIT ו-ROLLBACK לניהול עסקאות

-- ===== דוגמה 1: הוספת מבצע חדש וביצוע COMMIT =====

-- התחלת העסקה
BEGIN;

-- הצגת מצב לפני הכנסת הנתונים
SELECT * FROM Operation WHERE OperationID = 500;

-- הוספת מבצע חדש
INSERT INTO Operation (OperationID, OperationName, startDate, endDate, Location, ID)
VALUES (500, 'מבצע דוגמה', CURRENT_DATE, NULL, 'צפון', 1);

-- הצגת מצב אחרי הכנסת הנתונים אך לפני ה-COMMIT
SELECT * FROM Operation WHERE OperationID = 500;

-- ביצוע COMMIT לשמירת השינויים
COMMIT;

-- הצגת מצב אחרי ה-COMMIT
SELECT * FROM Operation WHERE OperationID = 500;

-- ===== דוגמה 2: עדכון נתונים וביצוע ROLLBACK =====

-- התחלת העסקה
BEGIN;

-- הצגת מצב לפני העדכון
SELECT * FROM Unit WHERE UnitID = 1;

-- עדכון מספר החיילים ביחידה
UPDATE Unit SET NumOfSoldiers = 999 WHERE UnitID = 1;

-- הצגת מצב אחרי העדכון אך לפני ה-ROLLBACK
SELECT * FROM Unit WHERE UnitID = 1;

-- ביצוע ROLLBACK לביטול השינויים
ROLLBACK;

-- הצגת מצב אחרי ה-ROLLBACK (חזרה למצב המקורי)
SELECT * FROM Unit WHERE UnitID = 1;

-- ===== דוגמה 3: מספר עדכונים עם SAVEPOINT =====

-- התחלת העסקה
BEGIN;

-- ביצוע עדכון ראשון
UPDATE Commander SET Rank = 'Major' WHERE ID = 1;

-- יצירת נקודת שמירה
SAVEPOINT update_rank;

-- ביצוע עדכון שני
UPDATE Commander SET Name = 'גיא לוי' WHERE ID = 1;

-- הצגת מצב אחרי שני העדכונים
SELECT * FROM Commander WHERE ID = 1;

-- חזרה לנקודת השמירה (ביטול רק העדכון השני)
ROLLBACK TO update_rank;

-- הצגת מצב אחרי חזרה לנקודת השמירה (רק העדכון הראשון נשמר)
SELECT * FROM Commander WHERE ID = 1;

-- ביצוע COMMIT לשמירת השינויים שנותרו
COMMIT;

-- הצגת מצב סופי
SELECT * FROM Commander WHERE ID = 1;