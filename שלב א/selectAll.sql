-- קובץ selectAll.sql להצגת כל הנתונים מכל הטבלאות במערכת מבצעים צבאית

-- הצגת נתוני טבלת החיל
SELECT * FROM Corps;

-- הצגת נתוני טבלת המפקדים
SELECT * FROM Commander;

-- הצגת נתוני טבלת המבצעים
SELECT * FROM Operation;

-- הצגת נתוני טבלת הדוחות המבצעיים
SELECT * FROM Operational_Report;

-- הצגת נתוני טבלת היחידות
SELECT * FROM Unit;

-- הצגת נתוני טבלת הציוד
SELECT * FROM Equipment;

-- הצגת נתוני טבלת המשימות
SELECT * FROM Task;

-- הצגת נתוני טבלת היחס בין מבצעים ליחידות
SELECT * FROM Executed_by;

-- הצגת נתוני טבלת היחס בין מבצעים לציוד
SELECT * FROM Requires;