--  פונקציה שמחזירה סטטוס כיסוי ציוד לוגיסטי לכל מבצע, כולל שמו של המפקד, הכמות הדרושה, הכמות הקיימת, אחוז כיסוי, וסטטוס מילולי
CREATE OR REPLACE FUNCTION get_logistic_status_by_operation()
RETURNS refcursor AS $$
DECLARE
    ref refcursor;  -- הגדרת משתנה מסוג refcursor שיחזיר את תוצאת השאילתה
BEGIN
    -- פתיחת הקורסור על שאילתה שמבצעת בדיקת סטטוס לוגיסטי לכל מבצע
    OPEN ref FOR
    SELECT
        o.operationname,              -- שם המבצע
        c.name AS commander_name,     -- שם המפקד האחראי על המבצע
        r.requiredquantity,           -- כמות הציוד שנדרש
        e.quantity,                   -- כמות הציוד הקיים בפועל

        -- חישוב אחוז הכיסוי: כמות קיימת מתוך נדרש
        ROUND(100.0 * e.quantity / NULLIF(r.requiredquantity, 0), 2) AS coverage_percent,

        -- קביעת סטטוס לוגיסטי לפי הכיסוי בפועל לעומת הדרוש
        CASE
            WHEN e.quantity >= r.requiredquantity THEN 'כיסוי תקין'         -- כיסוי מלא
            WHEN e.quantity >= r.requiredquantity * 0.7 THEN 'כיסוי גבולי'  -- מעל 70% מהדרוש
            WHEN e.quantity IS NULL THEN 'אין ציוד'                         -- לא הוגדרה כמות קיימת
            ELSE 'מחסור בציוד'                                              -- כמות נמוכה מ-70%
        END AS status

    -- חיבורים בין טבלאות: מבצע → דרישות ציוד → ציוד בפועל
    FROM operation o
    LEFT JOIN commander c ON c.id = o.id                       -- חיבור המפקד לפי מזהה (בהנחה שקיים קשר כזה)
    LEFT JOIN requires r ON r.operationid = o.operationid      -- דרישות ציוד לפי מבצע
    LEFT JOIN equipment e ON                                   -- ציוד בפועל
        e.equipmentid = r.equipmentid AND                      -- לפי מזהה ציוד
        e.equipment_type = r.equipment_type;                   -- וגם לפי סוג ציוד (כדי להבחין בין סוגים דומים)

    RETURN ref; -- החזרת הקורסור
END;
$$ LANGUAGE plpgsql;
