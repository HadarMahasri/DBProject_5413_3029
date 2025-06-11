CREATE OR REPLACE PROCEDURE summarize_medical_load_to_report()
LANGUAGE plpgsql AS $$
DECLARE
    rec RECORD;         -- משתנה שיחזיק כל שורה מה-cursor
    ref refcursor;      -- הגדרת refcursor לקריאת תוצאות מהפונקציה
BEGIN
    -- קריאה לפונקציה שמחזירה סיכום פצועים לפי חיל ומבצע
    ref := get_corps_patient_summary();

    LOOP
        FETCH ref INTO rec;         -- שליפת שורה אחת מה-cursor אל תוך rec
        EXIT WHEN NOT FOUND;       -- עצירה כשה-cursor נגמר

        -- בדיקה אם העומס גבוה מספיק ליצירת דוח
        IF rec.load_level IN ('עומס בינוני', 'עומס חריג') THEN
            BEGIN
                INSERT INTO operational_report(operationid, date, content)
                SELECT o.operationid,
                       -- בחירת תאריך אקראי בטווח [startdate, enddate]
                       (o.startdate + (
                           floor(random() * GREATEST(1, LEAST(COALESCE(o.enddate, CURRENT_DATE), CURRENT_DATE) - o.startdate + 1))
                           * interval '1 day'
                       ))::date,
                       -- ניסוח טקסט הדוח
                       'עומס רפואי ב-' || rec.corpsname || ' עבור המבצע ' || rec.operationname ||
                       ' - דרגת עומס: ' || rec.load_level
                FROM operation o
                WHERE TRIM(LOWER(o.operationname)) = TRIM(LOWER(rec.operationname))
                  AND CURRENT_DATE >= o.startdate
                LIMIT 1;
            EXCEPTION
                WHEN OTHERS THEN
                    RAISE NOTICE '⚠️ שגיאה בהכנסת דוח רפואי עבור המבצע %: %', rec.operationname, SQLERRM;
            END;
        END IF;
    END LOOP;
    CLOSE ref;
END;
$$;
