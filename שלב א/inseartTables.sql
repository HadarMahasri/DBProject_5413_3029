-- הכנסת נתונים לטבלת Corps (חיל) עם Specialization
INSERT INTO Corps (CorpsName, Specialization) VALUES ('חיל האוויר', 'לוחמה אווירית');
INSERT INTO Corps (CorpsName, Specialization) VALUES ('חיל הים', 'לוחמה ימית');
INSERT INTO Corps (CorpsName, Specialization) VALUES ('חיל רגלים', 'לוחמה קרקעית');

-- הכנסת נתונים לטבלת Commander (מפקד)
INSERT INTO Commander (Name, Rank, ExperienceYears) VALUES ('אבי כהן', 'אלוף', 20);
INSERT INTO Commander (Name, Rank, ExperienceYears) VALUES ('שרה לוי', 'אלוף משנה', 15);
INSERT INTO Commander (Name, Rank, ExperienceYears) VALUES ('דוד ישראלי', 'תת אלוף', 18);

-- הכנסת נתונים לטבלת Operation (מבצע)
INSERT INTO Operation (OperationName, Objective, Location, startDate, endDate, ID) 
VALUES ('מבצע חומת מגן', 'הגנה על הגבול הצפוני', 'צפון', '2023-01-15', '2023-01-20', 1);
INSERT INTO Operation (OperationName, Objective, Location, startDate, endDate, ID) 
VALUES ('מבצע עמוד ענן', 'הגנה אווירית', 'דרום', '2023-02-10', '2023-02-15', 2);
INSERT INTO Operation (OperationName, Objective, Location, startDate, endDate, ID) 
VALUES ('מבצע צוק איתן', 'מבצע ימי', 'מערב', '2023-03-05', '2023-03-12', 3);

-- הכנסת נתונים לטבלת Operational_Report (דו"ח מבצעי)
INSERT INTO Operational_Report (OperationID, Date, Content) 
VALUES (1, '2023-01-21', 'המבצע הושלם בהצלחה, הושגו כל היעדים');
INSERT INTO Operational_Report (OperationID, Date, Content) 
VALUES (2, '2023-02-16', 'המבצע הושלם באופן חלקי, חלק מהיעדים הושגו');
INSERT INTO Operational_Report (OperationID, Date, Content) 
VALUES (3, '2023-03-13', 'המבצע הושלם בהצלחה, עם מספר קשיים');

-- הכנסת נתונים לטבלת Unit (יחידה)
INSERT INTO Unit (CorpsID, Name, NumOfSoldiers) VALUES (1, 'טייסת 123', 50);
INSERT INTO Unit (CorpsID, Name, NumOfSoldiers) VALUES (2, 'שייטת 13', 75);
INSERT INTO Unit (CorpsID, Name, NumOfSoldiers) VALUES (3, 'גדוד 890', 120);

-- הכנסת נתונים לטבלת Equipment (ציוד)
INSERT INTO Equipment (Name, Quantity) VALUES ('מטוס F-15', 10);
INSERT INTO Equipment (Name, Quantity) VALUES ('ספינת טילים', 5);
INSERT INTO Equipment (Name, Quantity) VALUES ('נגמש', 20);

-- הכנסת נתונים לטבלת Task (משימה)
INSERT INTO Task (Task, Date, StartTime, EndTime, OperationID) 
VALUES ('סיור אווירי', '2023-01-16', '08:00', '10:00', 1);
INSERT INTO Task (Task, Date, StartTime, EndTime, OperationID) 
VALUES ('תקיפה אווירית', '2023-02-11', '06:30', '08:00', 2);
INSERT INTO Task (Task, Date, StartTime, EndTime, OperationID) 
VALUES ('סיור ימי', '2023-03-06', '07:15', '11:30', 3);

-- הכנסת נתונים לטבלת הקשר Executed_by (בוצע על ידי)
INSERT INTO Executed_by (OperationID, UnitID, CorpsID) VALUES (1, 1, 1);
INSERT INTO Executed_by (OperationID, UnitID, CorpsID) VALUES (2, 1, 1);
INSERT INTO Executed_by (OperationID, UnitID, CorpsID) VALUES (3, 2, 2);

-- הכנסת נתונים לטבלת הקשר Requires (דורש) עם RequiredQuantity
INSERT INTO Requires (EquipmentID, OperationID, RequiredQuantity) VALUES (1, 1, 2); -- 2 מטוסים
INSERT INTO Requires (EquipmentID, OperationID, RequiredQuantity) VALUES (2, 3, 1); -- 1 ספינת טילים
INSERT INTO Requires (EquipmentID, OperationID, RequiredQuantity) VALUES (3, 2, 3); -- 3 נגמשים
