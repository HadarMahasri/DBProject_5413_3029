DO $$
DECLARE
    ref refcursor;  -- הגדרת מצביע מסוג refcursor שיקבל את תוצאות הפונקציה
    rec RECORD;     -- הגדרת רשומה זמנית לשמירת כל שורה שתישלף בלולאה
BEGIN
    -- שלב 1: קריאה לפונקציה get_corps_patient_summary שמחזירה עומס פצועים לפי חיל ולפי מבצע
    -- התוצאה היא טבלה פתוחה מסוג refcursor
    ref := get_corps_patient_summary();

    -- הצגת כותרת לוגית למסך בזמן הרצה (רק להדגמה למשתמש או לבדיקות)
    RAISE NOTICE '----- עומס רפואי לפי חיל -----';

    -- שלב 1.1: מעבר בלולאה על כל התוצאות שהפונקציה החזירה
    LOOP
        FETCH ref INTO rec;             -- שליפת שורה אחת בכל איטרציה והכנסתה למשתנה rec
        EXIT WHEN NOT FOUND;           -- יציאה מהלולאה כשהסתיימו התוצאות
        RAISE NOTICE 'חיל: %, מספר פצועים: %', rec.corpsname, rec.total_patients;  
        -- הדפסת פרטי כל חיל למעקב
    END LOOP;

    -- סגירת המצביע אחרי שהסתיימה הלולאה
    CLOSE ref;

    -- שלב 2: קריאה לפרוצדורה summarize_medical_load_to_report
    -- הפרוצדורה בודקת אם יש עומס רפואי חריג או בינוני, ואם כן - מוסיפה דוח רפואי לטבלת operational_report
    CALL summarize_medical_load_to_report();
    -- הצגת הודעה לסיום התוכנית
    RAISE NOTICE 'התוכנית הסתיימה בהצלחה.';
END;
$$ LANGUAGE plpgsql;
