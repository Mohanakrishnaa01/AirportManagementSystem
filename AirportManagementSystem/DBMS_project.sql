-- Design an airport database to organize the information about all the airplanes stationed and
-- maintained at the airport. Every airplane has a registration number, and each airplane is of a
-- specific model. The airport accommodates a number of airplane models, and each model is
-- identified by a model number and has a capacity and a weight. A number of technicians work at
-- the airport. You need to store the name, SSN, address, phone number, and salary of each
-- technician. Each technician is an expert on one or more plane model(s), and his or her expertise
-- may overlap with that of other technicians. This information about technicians must also be
-- recorded. The airport has a number of tests that are used periodically to ensure that airplanes are
-- still airworthy. Each test has a test number, a name, and a maximum possible score. For each
-- testing event, the information needed is the date, the number of hours the technician spent doing
-- the test, and the score the airplane received on the test. 

CLEAR SCREEN;

DROP TABLE Airplanes CASCADE CONSTRAINT;
DROP TABLE AirplaneModel CASCADE CONSTRAINT;
DROP TABLE Technicians CASCADE CONSTRAINT;
DROP TABLE TEST CASCADE CONSTRAINT;
DROP TABLE Testingevent CASCADE CONSTRAINT;

DROP TABLE Users;
CREATE TABLE Users(
    username varchar(20),
    email varchar(25),
    password varchar(20),
    address varchar(25)
);

CREATE TABLE AirplaneModel(
    model_id int PRIMARY KEY,
    model_name varchar(20),
    capacity int,
    weight int
);

CREATE TABLE Airplanes(
    plane_name varchar(20),
    plane_regNo int PRIMARY KEY,
    model_id int,
    FOREIGN KEY (model_id) REFERENCES AirplaneModel(model_id)
);



CREATE TABLE Technicians(
    tech_id int PRIMARY KEY,
    tech_name varchar(20),
    tech_address varchar(30),
    tech_phoneNo number(10),
    salary decimal(10,2),
    expert_in varchar(7)
);

CREATE TABLE Test(
    test_no int PRIMARY KEY,
    test_name varchar(25),
    max_score int
);

CREATE TABLE Testingevent(
    event_id int PRIMARY KEY,
    test_no int,
    tech_id int,
    plane_regNo int,
    test_date DATE,
    hours_spent int,
    score int,
    status varchar(10),
    FOREIGN KEY (test_no) REFERENCES Test(test_no),
    FOREIGN KEY (tech_id) REFERENCES Technicians(tech_id),
    FOREIGN KEY (plane_regNo) REFERENCES Airplanes(plane_regNo)
);

update Testingevent
set score = 0 and status = 'pending'
where status='COMPLETED' and status='FAILED';

commit;




CREATE OR REPLACE TRIGGER check_test_no
BEFORE INSERT ON Testingevent
FOR EACH ROW
DECLARE
    tests_no Testingevent.test_no%TYPE;
BEGIN
    SELECT COUNT(*) INTO tests_no FROM Test WHERE test_no = :new.test_no;

    IF tests_no = 0 THEN
        RAISE_APPLICATION_ERROR(-20001,'Invalid test no');
    END IF;
END;
/

CREATE OR REPLACE TRIGGER check_tech_id
BEFORE INSERT ON Testingevent
FOR EACH ROW
DECLARE
    techs_id Technicians.tech_id%TYPE;
BEGIN
    SELECT COUNT(*) INTO techs_id FROM Technicians WHERE tech_id = :new.tech_id;

    IF techs_id = 0 THEN
        RAISE_APPLICATION_ERROR(-20001,'Invalid tech id');
    END IF;
END;
/

CREATE OR REPLACE TRIGGER check_plane_regNo
BEFORE INSERT ON Testingevent
FOR EACH ROW
DECLARE
    reg_nos Airplanes.plane_regNo%TYPE;
BEGIN
    SELECT COUNT(*) INTO reg_nos FROM Airplanes WHERE plane_regNo = :new.plane_regNo;

    IF reg_nos = 0 THEN
        RAISE_APPLICATION_ERROR(-20001,'Invalid reg no');
    END IF;
END;
/

CREATE OR REPLACE TRIGGER check_model_id
BEFORE INSERT ON Airplanes
FOR EACH ROW
DECLARE
    models_id AirplaneModel.model_id%TYPE;
BEGIN
    SELECT count(*) INTO models_id FROM AirplaneModel WHERE model_id = :new.model_id;

    IF models_id = 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Invalid model id');
    END IF;
END;
/



CREATE OR REPLACE PROCEDURE update_testing_event(p_event_id IN INT)
IS
BEGIN
    UPDATE Testingevent
    SET status = 'COMPLETED',
        score = ROUND(DBMS_RANDOM.VALUE(1,100))
    WHERE event_id = p_event_id;
END update_testing_event;
/

CREATE OR REPLACE PROCEDURE update_all_testing_event
IS
BEGIN
    UPDATE Testingevent
    SET STATUS = 'FAILED'
    WHERE TRUNC(SYSDATE) > test_date and status='pending';
END update_all_testing_event;
/



update Testingevent
set status = 'pending', score = 0;