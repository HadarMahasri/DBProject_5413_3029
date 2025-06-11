-- יצירת פרוצדורה בשם check_logistic_risk_operations
CREATE OR REPLACE PROCEDURE check_logistic_risk_operations()
LANGUAGE plpgsql AS $$
DECLARE
    rec RECORD;         -- משתנה מסוג RECORD – ישמש לאחסון כל שורה שמתקבלת מה-cursor
    ref refcursor;      -- הגדרה של refcursor שיאחסן את תוצאת הפונקציה
BEGIN
    -- קריאה לפונקציה שמחזירה סטטוס לוגיסטי לכל מבצע (ציוד נדרש מול ציוד זמין)
    ref := get_logistic_status_by_operation_upgraded();

    -- התחלת לולאה שמבצעת איטרציה על כל שורת תוצאה מה-cursor
    LOOP
        FETCH ref INTO rec;         -- שליפת שורה אחת מה-cursor אל תוך rec
        EXIT WHEN NOT FOUND;       -- יציאה מהלולאה כשאין יותר תוצאות

        -- בדיקה האם יש בעיה לוגיסטית (מחסור או כיסוי גבולי)
        IF rec.status IN ('מחסור בציוד', 'כיסוי גבולי') THEN
            BEGIN
                -- ניסיון להכניס דוח לוגיסטי חדש לטבלת operational_report
                INSERT INTO operational_report(operationid, date, content)
                SELECT 
                    o.operationid,                       -- מזהה המבצע
                    (
                        o.startdate +                   -- תאריך התחלתי
                        (
                            floor(random() * GREATEST(1, 
                                LEAST(COALESCE(o.enddate, CURRENT_DATE), CURRENT_DATE) - o.startdate + 1)
                            ) * interval '1 day'        -- בחירת תאריך אקראי בטווח המבצע
                        )
                    )::date,
                    -- תוכן הדוח המורכב מסטטוס לוגיסטי ושם המבצע
                    'התראה לוגיסטית: ' || rec.status || ' עבור המבצע ' || rec.operationname
                FROM operation o
                -- התאמת המבצע לפי שם, תוך נטרול רווחים ורישיות
                WHERE TRIM(LOWER(o.operationname)) = TRIM(LOWER(rec.operationname))
                  AND CURRENT_DATE >= o.startdate        -- מבצע חייב להיות בתוקף (כבר התחיל)
                LIMIT 1;                                  -- נכניס רק שורת דוח אחת לכל מבצע

            -- טיפול בשגיאות – אם משהו משתבש (למשל כפילות מפתח, NULL וכו') נציג הודעה
            EXCEPTION
                WHEN OTHERS THEN
                    RAISE NOTICE '⚠️ שגיאה בהכנסת דוח לוגיסטי עבור המבצע %: %', 
                                 rec.operationname, SQLERRM;
            END;
        END IF;
    END LOOP;

    -- סגירת ה-cursor אחרי סיום העבודה
    CLOSE ref;
END;
$$;
