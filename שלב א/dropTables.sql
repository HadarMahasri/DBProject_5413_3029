-- קובץ dropTables.sql למחיקת כל הטבלאות במערכת מבצעים צבאית
-- הטבלאות נמחקות בסדר הפוך מסדר היצירה שלהן כדי לטפל במפתחות זרים

-- מחיקת טבלאות היחס (טבלאות רבות-לרבות) תחילה
DROP TABLE IF EXISTS Requires;
DROP TABLE IF EXISTS Executed_by;

-- מחיקת טבלאות עם מפתחות זרים המצביעים לטבלאות אחרות
DROP TABLE IF EXISTS Task;
DROP TABLE IF EXISTS Equipment;
DROP TABLE IF EXISTS Unit;
DROP TABLE IF EXISTS Operational_Report;
DROP TABLE IF EXISTS Operation;

-- לבסוף, מחיקת טבלאות הבסיס
DROP TABLE IF EXISTS Commander;
DROP TABLE IF EXISTS Corps;