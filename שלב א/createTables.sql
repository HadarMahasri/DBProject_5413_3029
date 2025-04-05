-- יצירת טבלת Corps (חיל)
CREATE TABLE Corps (
    CorpsID SERIAL PRIMARY KEY,
    CorpsName VARCHAR(30) NOT NULL,
    Specialization VARCHAR(50) -- תחום ההתמחות של החיל
);

-- יצירת טבלת Commander (מפקד)
CREATE TABLE Commander (
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(30) NOT NULL,
    Rank VARCHAR(50) NOT NULL,
    ExperienceYears INT NOT NULL
);

-- יצירת טבלת Operation (מבצע)
CREATE TABLE Operation (
    OperationID SERIAL PRIMARY KEY,
    OperationName VARCHAR(30) NOT NULL,
    Objective TEXT,
    Location VARCHAR(30),
    startDate DATE,
    endDate DATE,
    ID INT,
    FOREIGN KEY (ID) REFERENCES Commander(ID)
);

-- יצירת טבלת Operational_Report (דו"ח מבצעי)
CREATE TABLE Operational_Report (
    ReportID SERIAL PRIMARY KEY,
    OperationID INT NOT NULL,
    Date DATE NOT NULL,
    Content TEXT,
    FOREIGN KEY (OperationID) REFERENCES Operation(OperationID)
);

-- יצירת טבלת Unit (יחידה)
CREATE TABLE Unit (
    UnitID SERIAL PRIMARY KEY,
    CorpsID INT NOT NULL,
    Name VARCHAR(30) NOT NULL,
    NumOfSoldiers INT NOT NULL,
    FOREIGN KEY (CorpsID) REFERENCES Corps(CorpsID)
);

-- יצירת טבלת Equipment (ציוד)
CREATE TABLE Equipment (
    EquipmentID SERIAL PRIMARY KEY,
    Name VARCHAR(30) NOT NULL,
    Quantity INT NOT NULL
);

-- יצירת טבלת Task (משימה)
CREATE TABLE Task (
    TaskID SERIAL PRIMARY KEY,
    Task VARCHAR(255) NOT NULL,
    Date DATE,
    StartTime TIME,
    EndTime TIME,
    OperationID INT NOT NULL,
    FOREIGN KEY (OperationID) REFERENCES Operation(OperationID)
);

-- יצירת טבלת הקשר Executed_by (בוצע על ידי - קשר בין מבצע ליחידה)
CREATE TABLE Executed_by (
    OperationID INT,
    UnitID INT,
    CorpsID INT,
    PRIMARY KEY (OperationID, UnitID),
    FOREIGN KEY (OperationID) REFERENCES Operation(OperationID),
    FOREIGN KEY (UnitID) REFERENCES Unit(UnitID),
    FOREIGN KEY (CorpsID) REFERENCES Corps(CorpsID)
);

-- יצירת טבלת הקשר Requires (דורש - קשר בין מבצע לציוד)
CREATE TABLE Requires (
    EquipmentID INT,
    OperationID INT,
    RequiredQuantity INT, -- כמה ציוד דרוש למבצע הזה
    PRIMARY KEY (EquipmentID, OperationID),
    FOREIGN KEY (EquipmentID) REFERENCES Equipment(EquipmentID),
    FOREIGN KEY (OperationID) REFERENCES Operation(OperationID)
);
