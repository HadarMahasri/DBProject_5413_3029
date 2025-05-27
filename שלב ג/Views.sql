/*
 * מבטים פשוטים ומשמעותיים לאגפים הרפואי והצבאי
 * כל מבט משלב מספר טבלאות ומספק מידע בעל ערך מעשי
 */

-- ======================== מבט 1: האגף הרפואי ========================
-- "מבט פרמדיקים פעילים" - מציג פרמדיקים עם הטיפולים שהם נתנו

CREATE OR REPLACE VIEW Active_Paramedics AS
SELECT 
    p.paramedic_id,
    p.paramedic_name,
    p.experience,
    -- ספירת כמות הטיפולים שנתן הפרמדיק
    COUNT(t.treatment_id) AS total_treatments,
    -- ממוצע זמן הטיפול
    ROUND(AVG(t.treatment_duration), 1) AS avg_treatment_time,
    -- התאריך של הטיפול האחרון
    MAX(t.date) AS last_treatment_date,
    -- סוגי הטיפולים השונים שנתן
    COUNT(DISTINCT t.treatment_type) AS different_treatment_types
FROM Paramedic p
LEFT JOIN Treatment t ON p.paramedic_id = t.paramedic_id
GROUP BY p.paramedic_id, p.paramedic_name, p.experience;

-- ======================== שאילתות על מבט הפרמדיקים ========================

-- שאילתה 1: מיהם הפרמדיקים הכי פעילים?
-- שאלה מעשית: איזה פרמדיקים נותנים הכי הרבה טיפולים?
SELECT 
    paramedic_name,
    experience,
    total_treatments,
    avg_treatment_time,
    different_treatment_types
FROM Active_Paramedics
WHERE total_treatments > 0  -- רק פרמדיקים שנתנו טיפולים
ORDER BY total_treatments DESC, experience DESC
LIMIT 10;

-- שאילתה 2: איזה פרמדיקים צריכים עזרה או הכשרה?
-- שאלה מעשית: מי הפרמדיקים החדשים או הפחות פעילים שצריכים תמיכה?
SELECT 
    paramedic_name,
    experience,
    total_treatments,
    CASE 
        WHEN total_treatments = 0 THEN 'לא פעיל - צריך הכשרה'
        WHEN experience < 5 AND total_treatments < 3 THEN 'חדש - צריך ליווי'
        WHEN avg_treatment_time > 60 THEN 'זמן טיפול גבוה - צריך סקירה'
        ELSE 'תקין'
    END AS status_recommendation
FROM Active_Paramedics
WHERE (total_treatments = 0 OR experience < 5 OR avg_treatment_time > 60)
ORDER BY experience ASC, total_treatments ASC
Limit 10;


-- ======================== מבט 2: האגף הצבאי ========================
-- "מבט יחידות ומבצעים" - מציג איזה יחידות השתתפו באילו מבצעים

CREATE OR REPLACE VIEW Units_In_Operations AS
SELECT 
    o.OperationID,
    o.OperationName,
    o.Location,
    o.startDate,
    o.endDate,
    u.UnitID,
    u.Name AS unit_name,
    u.NumOfSoldiers,
    corps.CorpsName,
    corps.Specialization
FROM Operation o
JOIN Executed_by eb ON o.OperationID = eb.OperationID
JOIN Unit u ON eb.UnitID = u.UnitID
JOIN Corps corps ON u.CorpsID = corps.CorpsID;

-- ======================== שאילתות על מבט היחידות ========================

-- שאילתה 1: איזה יחידות הכי פעילות?
-- שאלה פשוטה: אילו יחידות השתתפו בהכי הרבה מבצעים?
SELECT 
    unit_name,
    CorpsName,
    NumOfSoldiers,
    COUNT(*) AS operations_participated
FROM Units_In_Operations
GROUP BY UnitID, unit_name, CorpsName, NumOfSoldiers
ORDER BY operations_participated DESC, NumOfSoldiers DESC
LIMIT 10;

-- שאילתה 2: איזה חילות הכי נדרשים?
-- שאלה פשוטה: איזה סוגי חילות הכי הרבה פעמים נקראים למבצעים?
SELECT 
    CorpsName,
    Specialization,
    COUNT(DISTINCT OperationID) AS different_operations,
    COUNT(*) AS total_unit_participations,
    SUM(NumOfSoldiers) AS total_soldiers_deployed
FROM Units_In_Operations
GROUP BY CorpsName, Specialization
ORDER BY different_operations DESC, total_soldiers_deployed DESC
LIMIT 10;