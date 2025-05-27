

-- ======================== מבט 1: האגף הרפואי ========================
-- שם המבט: Active_Paramedics
-- תיאור: מציג פרמדיקים פעילים עם סטטיסטיקות מקיפות על הטיפולים שהם נותנים
-- טבלות בסיס: Paramedic, Treatment
-- מטרת השימוש: ניתוח ביצועי פרמדיקים, זיהוי צרכי הכשרה, ותכנון כוח אדם

CREATE OR REPLACE VIEW Active_Paramedics AS
SELECT 
    -- מידע בסיסי על הפרמדיק
    p.paramedic_id,                                           -- מזהה ייחודי של הפרמדיק
    p.paramedic_name,                                         -- שם מלא של הפרמדיק
    p.experience,                                             -- שנות ניסיון (מספר שלם)
    
    -- מדדי פעילות וביצועים
    COUNT(t.treatment_id) AS total_treatments,                -- סך כל הטיפולים שנתן הפרמדיק
    ROUND(AVG(t.treatment_duration), 1) AS avg_treatment_time, -- זמן ממוצע בדקות לטיפול (עוגל לעשירית)
    MAX(t.date) AS last_treatment_date,                       -- תאריך הטיפול האחרון שנתן
    COUNT(DISTINCT t.treatment_type) AS different_treatment_types -- מספר סוגי הטיפולים השונים שמבצע
    
FROM Paramedic p
LEFT JOIN Treatment t ON p.paramedic_id = t.paramedic_id      -- LEFT JOIN כדי לכלול גם פרמדיקים שלא נתנו טיפולים
GROUP BY p.paramedic_id, p.paramedic_name, p.experience;     -- קיבוץ לפי מזהה הפרמדיק כדי לחשב סטטיסטיקות

-- ======================== שאילתות ניתוח על מבט הפרמדיקים ========================

-- שאילתה 1: זיהוי הפרמדיקים הכי פעילים במערכת
-- מטרה עסקית: לזהות את הפרמדיקים המובילים כדי להכיר בתרומתם ולהשתמש בהם כמנטורים
-- פרמטרי מדידה: כמות טיפולים, ניסיון, זמן טיפול ממוצע, מגוון טיפולים

SELECT 
    paramedic_name,                    -- שם הפרמדיק לתצוגה
    experience,                        -- שנות ניסיון (חשוב לקורלציה עם פעילות)
    total_treatments,                  -- מספר הטיפולים (מדד עיקרי לפעילות)
    avg_treatment_time,                -- זמן ממוצע (מדד ליעילות)
    different_treatment_types          -- מגוון טיפולים (מדד לרב-תחומיות)
FROM Active_Paramedics
WHERE total_treatments > 0             -- סינון: רק פרמדיקים שנתנו לפחות טיפול אחד
ORDER BY total_treatments DESC,        -- מיון ראשי: לפי כמות טיפולים (יורד)
         experience DESC               -- מיון משני: לפי ניסיון (יורד)
LIMIT 10;                             -- הצגת 10 המובילים

-- שאילתה 2: זיהוי פרמדיקים הזקוקים לתמיכה או הכשרה
-- מטרה עסקית: לזהות פרמדיקים שצריכים התערבות - הכשרה, ליווי או סקירת ביצועים
-- קריטריונים: חוסר פעילות, חדשים במקצוע, זמן טיפול גבוה

SELECT 
    paramedic_name,                    -- שם הפרמדיק
    experience,                        -- שנות ניסיון (קריטריון לזיהוי חדשים)
    total_treatments,                  -- מספר טיפולים (קריטריון לפעילות)
    
    -- לוגיקת סיווג והמלצות טיפול
    CASE 
        WHEN total_treatments = 0 THEN 'לא פעיל - צריך הכשרה'                    -- לא נתן טיפולים כלל
        WHEN experience < 5 AND total_treatments < 3 THEN 'חדש - צריך ליווי'     -- פרמדיק חדש עם מעט טיפולים
        WHEN avg_treatment_time > 60 THEN 'זמן טיפול גבוה - צריך סקירה'         -- טיפולים ארוכים מידי
        ELSE 'תקין'                                                           -- מצב תקין
    END AS status_recommendation       -- המלצת פעולה מבוססת קריטריונים
    
FROM Active_Paramedics
WHERE (total_treatments = 0            -- סינון: פרמדיקים שלא פעילים
       OR experience < 5               -- או פרמדיקים חדשים (פחות מ-5 שנות ניסיון)
       OR avg_treatment_time > 60)     -- או פרמדיקים עם זמן טיפול גבוה (מעל 60 דקות)
ORDER BY experience ASC,              -- מיון ראשי: פרמדיקים חדשים קודם
         total_treatments ASC          -- מיון משני: פחות פעילים קודם
LIMIT 10;                             -- הצגת 10 המקרים הדחופים ביותר

-- ======================== מבט 2: האגף הצבאי ========================
-- שם המבט: Units_In_Operations  
-- תיאור: מציג קשרים בין יחידות צבאיות למבצעים שבהם השתתפו
-- טבלות בסיס: Operation, Unit, Corps, Executed_by (טבלת קשר)
-- מטרת השימוש: ניתוח עומס יחידות, תכנון מבצעים עתידיים, זיהוי יחידות קריטיות

CREATE OR REPLACE VIEW Units_In_Operations AS
SELECT 
    -- מידע על המבצע
    o.OperationID,                     -- מזהה ייחודי של המבצע
    o.OperationName,                   -- שם המבצע
    o.Location,                        -- מיקום ביצוע המבצע
    o.startDate,                       -- תאריך תחילת המבצע
    o.endDate,                         -- תאריך סיום המבצע
    
    -- מידע על היחידה
    u.UnitID,                          -- מזהה ייחודי של היחידה
    u.Name AS unit_name,               -- שם היחידה
    u.NumOfSoldiers,                   -- מספר החיילים ביחידה
    
    -- מידע על החיל
    corps.CorpsName,                   -- שם החיל (חיל רגלים, שריון, וכו')
    corps.Specialization               -- התמחות החיל
    
FROM Operation o
JOIN Executed_by eb ON o.OperationID = eb.OperationID    -- קישור מבצעים ליחידות דרך טבלת הקשר
JOIN Unit u ON eb.UnitID = u.UnitID                      -- קישור ליחידות
JOIN Corps corps ON u.CorpsID = corps.CorpsID;          -- קישור לחילות

-- ======================== שאילתות ניתוח על מבט היחידות ========================

-- שאילתה 1: זיהוי היחידות הכי פעילות במבצעים
-- מטרה עסקית: לזהות יחידות עם עומס גבוה למעקב ותכנון מנוחה/חילוף
-- מדדי מדידה: מספר מבצעים, גודל יחידה

SELECT 
    unit_name,                         -- שם היחידה
    CorpsName,                         -- החיל שהיחידה שייכת אליו
    NumOfSoldiers,                     -- גודל היחידה (רלוונטי לעומס)
    COUNT(*) AS operations_participated -- מספר המבצעים שהיחידה השתתפה בהם
FROM Units_In_Operations
GROUP BY UnitID, unit_name, CorpsName, NumOfSoldiers     -- קיבוץ לפי יחידה (כל השדות הלא-מקובצים)
ORDER BY operations_participated DESC,                   -- מיון ראשי: לפי מספר מבצעים (יורד)
         NumOfSoldiers DESC                              -- מיון משני: יחידות גדולות קודם
LIMIT 10;                                               -- הצגת 10 היחידות הפעילות ביותר

-- שאילתה 2: ניתוח ביקוש לחילות שונים
-- מטרה עסקית: לזהות איזה חילות הכי נדרשים כדי לתכנן הכשרות ותגבורת
-- מדדי מדידה: מספר מבצעים שונים, השתתפויות כוללות, מספר חיילים שנפרסו

SELECT 
    CorpsName,                                    -- שם החיל
    Specialization,                               -- התמחות החיל
    COUNT(DISTINCT OperationID) AS different_operations,      -- מספר מבצעים שונים (מדד לגיוון)
    COUNT(*) AS total_unit_participations,                    -- סך השתתפויות יחידות (מדד לעומס כולל)
    SUM(NumOfSoldiers) AS total_soldiers_deployed             -- סך החיילים שנפרסו (מדד לעומס אנושי)
FROM Units_In_Operations
GROUP BY CorpsName, Specialization                -- קיבוץ לפי חיל והתמחות
ORDER BY different_operations DESC,               -- מיון ראשי: חילות המשתתפים במגוון מבצעים
         total_soldiers_deployed DESC             -- מיון משני: חילות עם פריסה רחבה
LIMIT 10;                                        -- הצגת 10 החילות הנדרשים ביותר

