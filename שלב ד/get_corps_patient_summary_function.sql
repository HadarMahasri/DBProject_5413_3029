--  פונקציה המחזירה עומס פצועים לפי חיל ומבצע, כולל אחוז מסך כל הפצועים ורמת העומס
CREATE OR REPLACE FUNCTION get_corps_patient_summary()
RETURNS refcursor AS $$
DECLARE
    ref refcursor;  -- הגדרת משתנה מסוג רפרנס לקורסור
BEGIN
    -- פתיחת קורסור שמחזיר סיכום פצועים לפי חיל ומבצע
    OPEN ref FOR
    SELECT
        c.corpsname,  -- שם החיל
        o.operationname,  -- שם המבצע
        COUNT(p.patient_id) AS total_patients,  -- סך הפצועים בחיל עבור מבצע מסוים

        -- חישוב אחוז הפצועים מתוך כלל הפצועים בכל המערכת
        ROUND(100.0 * COUNT(p.patient_id) / NULLIF((SELECT COUNT(*) FROM patient), 0), 2) AS percent_of_total,

        -- קביעת דרגת עומס רפואי על סמך מספר הפצועים
        CASE 
            WHEN COUNT(p.patient_id) > 10 THEN 'עומס חריג'
            WHEN COUNT(p.patient_id) > 5 THEN 'עומס בינוני'
            ELSE 'עומס נמוך'
        END AS load_level

    -- חיבורים ליצירת הקשר בין חיל → יחידה → מבצע → אירוע רפואי → פצוע
    FROM corps c
    JOIN unit u ON c.corpsid = u.corpsid                     -- חיל ↔ יחידה
    JOIN executed_by e ON u.unitid = e.unitid               -- יחידה ↔ מבצע
    JOIN operation o ON o.operationid = e.operationid       -- קבלת שם המבצע
    LEFT JOIN medical_event me ON me.operation_id = o.operationid  -- מבצע ↔ אירוע רפואי
    LEFT JOIN patient p ON p.event_id = me.event_id         -- אירוע רפואי ↔ פצוע

    -- קיבוץ לפי שם חיל ושם מבצע
    GROUP BY c.corpsname, o.operationname;

    RETURN ref; -- החזרת הקורסור
END;
$$ LANGUAGE plpgsql;
