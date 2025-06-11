CREATE OR REPLACE FUNCTION trg_check_logistic_risk()
RETURNS TRIGGER AS $$
BEGIN
    CALL check_logistic_risk_operations();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_on_requires_update
AFTER INSERT OR UPDATE ON requires
FOR EACH STATEMENT
EXECUTE FUNCTION trg_check_logistic_risk();