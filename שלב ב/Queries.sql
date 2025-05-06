-- 1. הצגת מבצעים שמשתמשים ביותר ציוד מהממוצע (תת שאילתה)
SELECT o.OperationID, o.OperationName, COUNT(r.EquipmentID) AS EquipmentCount
FROM Operation o
JOIN Requires r ON o.OperationID = r.OperationID
GROUP BY o.OperationID, o.OperationName
HAVING COUNT(r.EquipmentID) > (
    SELECT AVG(equip_count)
    FROM (
        SELECT COUNT(EquipmentID) as equip_count
        FROM Requires
        GROUP BY OperationID
    ) AS subquery
)
ORDER BY EquipmentCount DESC;

-- 2. מפקדים מנוסים שלא מובילים מבצעים כרגע (תת שאילתה)
SELECT c.ID, c.Name, c.Rank, c.ExperienceYears
FROM Commander c
WHERE c.ExperienceYears > 10
AND c.ID NOT IN (
    SELECT ID FROM Operation
    WHERE endDate IS NULL
)
ORDER BY c.ExperienceYears DESC;

-- 3. מבצעים עם יותר משימות מהממוצע (תת שאילתה)
SELECT o.OperationID, o.OperationName, COUNT(t.TaskID) AS TaskCount
FROM Operation o
JOIN Task t ON o.OperationID = t.OperationID
GROUP BY o.OperationID, o.OperationName
HAVING COUNT(t.TaskID) > (
    SELECT AVG(task_count) 
    FROM (
        SELECT COUNT(*) as task_count
        FROM Task
        GROUP BY OperationID
    ) AS avg_tasks
)
ORDER BY TaskCount DESC;

-- 4. הצגת היחידות והחילות שלהן, עם מספר המבצעים שכל יחידה השתתפה בהם
SELECT u.UnitID, u.Name AS UnitName, c.CorpsName, c.Specialization, 
       COUNT(e.OperationID) AS OperationCount
FROM Unit u
JOIN Corps c ON u.CorpsID = c.CorpsID
LEFT JOIN Executed_by e ON u.UnitID = e.UnitID
GROUP BY u.UnitID, u.Name, c.CorpsName, c.Specialization
ORDER BY OperationCount DESC;

-- 5. מציאת המבצעים שנמשכו יותר מ-500 ימים עם פירוט מספר הימים
SELECT o.OperationID, o.OperationName, o.startDate, o.endDate,
       (o.endDate - o.startDate) AS DurationDays
FROM Operation o
WHERE (o.endDate - o.startDate) > 500
ORDER BY DurationDays DESC;

-- 6. הצגת ציוד שנדרש ביותר ממבצע אחד ומה הכמות הכוללת שנדרשה
SELECT e.EquipmentID, e.Name, e.Quantity AS TotalAvailable, 
       COUNT(r.OperationID) AS UsedInOperations,
       SUM(r.RequiredQuantity) AS TotalRequired
FROM Equipment e
JOIN Requires r ON e.EquipmentID = r.EquipmentID
GROUP BY e.EquipmentID, e.Name, e.Quantity
HAVING COUNT(r.OperationID) > 1
ORDER BY UsedInOperations DESC;

-- 7. מציאת המשימות שהתרחשו במהלך חודש פברואר 2023
SELECT t.TaskID, t.Task, t.Date, t.StartTime, t.EndTime, o.OperationName
FROM Task t
JOIN Operation o ON t.OperationID = o.OperationID
WHERE t.Date BETWEEN '2023-02-01' AND '2023-02-28'
ORDER BY t.Date, t.StartTime;

-- 8. סיכום מספר המבצעים לפי חודשים בשנת 2023
SELECT 
    EXTRACT(MONTH FROM startDate) AS Month,
    COUNT(*) AS OperationCount
FROM Operation
WHERE EXTRACT(YEAR FROM startDate) = 2023
GROUP BY EXTRACT(MONTH FROM startDate)
ORDER BY Month;

-- ======= שאילתות UPDATE =======

-- 1. עדכון דרגות של מפקדים עם ניסיון רב
UPDATE Commander
SET Rank = 'General'
WHERE ExperienceYears > 20 AND Rank != 'General';

-- 2. הארכת מבצעים שהסתיימו בפברואר ב-3 ימים
UPDATE Operation
SET endDate = endDate + INTERVAL '3 days'
WHERE EXTRACT(MONTH FROM endDate) = 2 AND EXTRACT(YEAR FROM endDate) = 2023;

-- 3. עדכון התמחות של חילות אוויר
UPDATE Corps
SET Specialization = 'Tactical Navigation'
WHERE CorpsName = 'Air Force' AND (Specialization IS NULL OR Specialization = '');

-- ======= שאילתות DELETE =======

-- 1. מחיקת משימות שהסתיימו לפני 2023
DELETE FROM Task
WHERE Date < '2023-01-01';

-- 2. מחיקת ציוד שלא נמצא בשימוש באף מבצע
DELETE FROM Equipment
WHERE EquipmentID NOT IN (
    SELECT DISTINCT EquipmentID FROM Requires
);

-- 3. מחיקת הקצאות ציוד למבצעים שכבר הסתיימו לפני יותר מחודש
DELETE FROM Requires
USING Operation
WHERE Requires.OperationID = Operation.OperationID
AND Operation.endDate < CURRENT_DATE - INTERVAL '1 month';