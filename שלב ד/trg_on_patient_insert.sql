CREATE OR REPLACE FUNCTION trg_check_medical_load()
RETURNS TRIGGER AS $$
BEGIN
    CALL check_medical_load_operations();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_on_patient_insert
AFTER INSERT ON patient
FOR EACH STATEMENT
EXECUTE FUNCTION trg_check_medical_load();
