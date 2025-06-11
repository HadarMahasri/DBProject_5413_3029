DO $$
DECLARE
    ref refcursor;  -- הגדרת משתנה refcursor שישמש לקבלת תוצאות מהפונקציה
    rec RECORD;     -- הגדרת רשומה זמנית שתקבל כל שורה מה-cursor בלולאה
BEGIN
    -- שלב 1: קריאה לפונקציה get_logistic_status_by_operation
    -- הפונקציה מחזירה refcursor עם מידע על מצב הציוד הלוגיסטי של כל מבצע (שם מבצע, מפקד, ציוד נדרש וכמות בפועל)
    ref := get_logistic_status_by_operation();

    -- הודעה לוגית שמודיעה למשתמש שהנתונים שהתקבלו מהפונקציה יוצגו כעת
    RAISE NOTICE '----- סטטוס לוגיסטי לפי מבצע -----';

    -- שלב 1.1: לולאה שרצה על כל רשומות ה-cursor שהוחזר מהפונקציה
    LOOP
        FETCH ref INTO rec;            -- שליפת שורה אחת מה-cursor לכל איטרציה
        EXIT WHEN NOT FOUND;          -- יציאה מהלולאה כאשר הסתיימו כל הרשומות
        RAISE NOTICE 'מבצע: %, סטטוס: %', rec.operationname, rec.status;
        -- הצגת שם המבצע והסטטוס הלוגיסטי שלו (מחסור בציוד / כיסוי תקין וכו')
    END LOOP;

    -- סגירת ה-cursor בסיום הלולאה
    CLOSE ref;

    -- שלב 2: קריאה לפרוצדורה check_logistic_risk_operations
    -- הפרוצדורה מבצעת את הבדיקה אם יש מחסור או כיסוי גבולי,
    -- ואם כן – מוסיפה רשומה של התראה לוגיסטית לטבלת operational_report.
    CALL check_logistic_risk_operations();

    -- הודעת סיום להרצה מוצלחת של התוכנית
    RAISE NOTICE 'התוכנית הסתיימה בהצלחה.';
END;
$$ LANGUAGE plpgsql;
