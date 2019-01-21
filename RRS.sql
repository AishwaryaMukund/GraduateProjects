CREATE SCHEMA RAILWAY_RESERVATION_SYSTEM;

USE RAILWAY_RESERVATION_SYSTEM;

/* ================= Data Definition Language ==================*/

/* Create USER Table  */
create table if not exists USER(userId int primary key,firstName varchar(50),lastName varchar(50),age int,gender char,
											      phoneNo varchar(50),email varchar(50),address varchar(100));

/* Create TRAIN Table  */
create table if not exists TRAIN(trainNo int primary key,trainName varchar(50),source varchar(50),destination varchar(50),acCost float, genCost float); 

/* Create TRAINSTATUS Table  */
create table if not exists TRAINSTATUS(trainNo int,trainDate date, availabilityOfSeats char, acSeat int,genSeat int,bookedAcSeat int,bookedGenSeat int,
																primary key(trainNo,trainDate), 
																constraint foreign key(trainNo) references TRAIN(trainNo));

/* Create TICKET Table  */
create table if not exists TICKET(ticketId int primary key,userId int,status char,trainNo int, travelingDate date,
													constraint foreign key(userId) references USER(userId),
													constraint foreign key(trainNo) references TRAIN(trainNo));
						
/* Create PASSENGER Table  */						
create table if not exists PASSENGER(passengerId int primary key,passengerName varchar(50), age int,gender char,
																userId int,reservationStatus char,seatNo varchar(5), ticketId int, category varchar(10),
																constraint foreign key(userId) references USER(userId),
                                                                constraint foreign key(ticketId) references TICKET(ticketId));
/* Create STATION Table  */															
create table if not exists STATION(stationNo int ,stationName varchar(50),Time time,trainNo int,
														primary key(stationNo,trainNo), 
                                                        constraint foreign key(trainNo) references TRAIN(trainNo));
/* Create BOOKING Table  */													
create table if not exists BOOKING( userId int,ticketId int, bookedDate date, category varchar(10),
														 constraint foreign key(userId) references USER(userId),
                                                         constraint foreign key(ticketId) references TICKET(ticketId));
														
/* Create CANCEL Table  */
create table if not exists CANCEL(userId int,ticketId int,passengerId int,
														constraint foreign key(ticketId) references TICKET(ticketId),
                                                        constraint foreign key(passengerId) references PASSENGER(passengerId),
                                                        constraint foreign key(userId) references USER(userId));
/* Create STARTS Table  */												
create table if not exists STARTS(trainNo int,stationNo int,
													 constraint foreign key(trainNo) references TRAIN(trainNo),
                                                     constraint foreign key(stationNo) references STATION(stationNo));

/* Create STOPSAT Table  */
create table if not exists STOPSAT(trainNo int,stationNo int,
														constraint foreign key(trainNo) references TRAIN(trainNo),
                                                        constraint foreign key(stationNo) references STATION(stationNo));
                                                        
/* ============== Data Manipulation Language ================= */
insert into USER values(1001, 'Robin', 'Hood', 30, 'M', '7026355630', 'robin@gmail.com', '123 N 6th St Fresno, CA');
insert into USER values(1002, 'Ted', 'Mosby', 35, 'M', '5596355630', 'ted@gmail.com', '456 N 6th St Fresno, CA');
insert into USER values(1003, 'Mary', 'Hawkins', 20, 'F', '7026355645', 'mary@gmail.com', '123 N 9th St Fresno, CA');
insert into USER values(1004, 'Monica', 'Geller', 28, 'F', '4426355630', 'monica@gmail.com', '131 S 6th St Fresno, CA');
insert into USER values(1005, 'Kumar', 'Vihaan', 38, 'M', '7028855630', 'vihaan@gmail.com', '183 E Alamos Ave Fresno, CA');

insert into TRAIN values(2001, 'Safety Express', 'Fresno', 'Madera', 30, 25);
insert into TRAIN values(2002, 'Bull Express', 'Fresno', 'Visalia', 35, 30);
insert into TRAIN values(2003, 'Dog Express', 'Fresno', 'Sacramento',  40, 35);
insert into TRAIN values(2004, 'Fresno Express', 'Sacramento', 'Modesto', 30, 25);
insert into TRAIN values(2005, 'Speedway', 'Sacramento', 'Los Angeles', 40, 35);
insert into TRAIN values(2006, 'TEST', 'Los Angeles', 'San Fransisco', 50, 45);
insert into TRAIN values(2007, 'Royal Blue', 'Madera', 'Los Angeles', 50, 45);

insert into TRAINSTATUS values(2001,20180801, 'Y',20, 30, 0, 1);
insert into TRAINSTATUS values(2002,20180801, 'Y',20, 30, 2, 4);
insert into TRAINSTATUS values(2003,20180903, 'Y',20, 30, 1, 1);
insert into TRAINSTATUS values(2004,20180804, 'Y',20, 30, 2, 2);
insert into TRAINSTATUS values(2005,20180701, 'Y',20, 30, 0, 0);
insert into TRAINSTATUS values(2006,20180701, 'N',20, 30, 20, 30);
insert into TRAINSTATUS values(2007,20180701, 'Y',20, 30, 1, 2);

insert into TICKET(ticketId,userId,trainNo, travelingDate) values(3001, 1001, 2001,20180801);
insert into TICKET(ticketId,userId,trainNo,travelingDate) values(3002, 1002, 2002, 20180801 );
insert into TICKET(ticketId,userId,trainNo, travelingDate) values(3003, 1003, 2003, 20180903);
insert into TICKET(ticketId,userId,trainNo, travelingDate) values(3004, 1004, 2004, 20180804);
insert into TICKET(ticketId,userId,trainNo, travelingDate) values(3005, 1005, 2005, 20180701);
insert into TICKET(ticketId,userId,trainNo, travelingDate) values(3007, 1005, 2004, 20180804);
insert into TICKET(ticketId,userId,trainNo, travelingDate) values(3008, 1002, 2007, 20180701);

insert into PASSENGER values(2050, 'Barney Stinson', 29, 'M', 1001, 'C', 'A112', 3001, 'AC');
insert into PASSENGER values(2051, 'Ted Mosby', 35, 'M', 1002, 'C', 'B012', 3002, 'GEN');
insert into PASSENGER values(2052, 'Tom Hawkins', 35, 'M', 1003, 'C', 'B111', 3005,'AC');
insert into PASSENGER values(2053, 'Tony Hawkins', 10, 'M', 1003, 'C', 'B112', 3007,'AC');
insert into PASSENGER values(2054, 'Theresa Hawkins', 8, 'F', 1004, 'C', 'B113', 3008, 'AC');
insert into PASSENGER values(2055, 'Maria Hawkins', 65, 'F', 1005, 'C', 'B114', 3003,'GEN');
insert into PASSENGER values(2056, 'John Hawkins', 80, 'M', 1003, 'C', 'B115', 3005,'GEN');


insert into STATION values(4001, 'Fresno', '113000', 2001);
insert into STATION values(4002, 'Madera', '133000', 2001);
insert into STATION values(4003, 'Visalia', '103000', 2002);
insert into STATION values(4004, 'Sacramento', '083000', 2003);
insert into STATION values(4005, 'Modesto', '113000', 2004);
insert into STATION values(4006, 'Los Angeles', '110000', 2005);
insert into STATION values(4007, 'Bakersfield', '020000', 2007);

insert into BOOKING values(1001, 3001, 20180801, 'AC');
insert into BOOKING values(1002, 3002, 20180702, 'GEN');
insert into BOOKING values(1003, 3003, 20180610, 'AC');
insert into BOOKING values(1004, 3004, 20180701, 'AC');
insert into BOOKING values(1005, 3005, 20180625, 'GEN');

insert into STARTS values(2001, 4001);
insert into STARTS values(2002, 4001);
insert into STARTS values(2003, 4001);
insert into STARTS values(2004, 4004);
insert into STARTS values(2005, 4004);
insert into STARTS values(2006, 4006);

insert into STOPSAT values(2001, 4006);
insert into STOPSAT values(2002, 4005);
insert into STOPSAT values(2003, 4004);
insert into STOPSAT values(2004, 4003);
insert into STOPSAT values(2005, 4001);
insert into STOPSAT values(2002, 4005);


/* query to display User Ids and names of the  users who booked ticket for Fresno Express*/
SELECT U.USERID, CONCAT(U.FIRSTNAME, U.LASTNAME) AS NAME 
FROM USER U, TRAIN T, TICKET TC
WHERE U.USERID = TC.USERID AND T.TRAINNO = TC.TRAINNO AND T.TRAINNAME LIKE 'FRESNO EXPRESS';

/* query to display the train  from Fresno to Sacramento */
SELECT  T.TRAINNO , T.TRAINNAME
FROM TRAIN T, STARTS ST, STOPSAT SA
WHERE ST.STATIONNO = (SELECT STATIONNO FROM STATION WHERE STATIONNAME LIKE 'FRESNO')
AND SA.STATIONNO = (SELECT STATIONNO FROM STATION WHERE STATIONNAME LIKE 'SACRAMENTO')
AND T.TRAINNO = ST.TRAINNO AND T.TRAINNO = SA.TRAINNO AND ST.TRAINNO = SA.TRAINNO;

/* Number of passengers who have booked tickets to Los Angeles */
SELECT COUNT(*)
FROM PASSENGER PA, TRAIN TR, TICKET TI
WHERE PA.TICKETID = TI.TICKETID AND TI.TRAINNO = TR.TRAINNO AND TR.DESTINATION LIKE 'LOS ANGELES';

/* query to update the arrivalTime of the train safety express arriving at the station Madera */ 
UPDATE STATION SET TIME= '103500' WHERE STATIONNAME LIKE 'MADERA' AND TRAINNO = (SELECT TRAINNO FROM TRAIN WHERE TRAINNAME LIKE 'SAFETY EXPRESS');



/* Trigger TICKET_BEFORE_INSERT checks for the availability of seats before inserting the value */
DELIMITER //

CREATE TRIGGER TICKET_BEFORE_INSERT
BEFORE INSERT
   ON TICKET FOR EACH ROW

BEGIN

DECLARE TRAINNUMBER INT;

SELECT TRAINNO INTO TRAINNUMBER FROM TRAINSTATUS WHERE AVAILABILITYOFSEATS = 'N' AND TRAINNO = NEW.TRAINNO;

IF (NEW.TRAINNO = TRAINNUMBER)
THEN SIGNAL SQLSTATE '45000'  SET MESSAGE_TEXT = "SEATS ARE NOT AVAILABLE";
END IF;

END; //

DELIMITER ;

insert into TICKET(ticketId,userId,status,trainNo) values(3006, 1001, 'C', 2002);

Insert into TICKET(ticketId,userId,status,trainNo) values(3007, 1004, 'C', 2006);

/* Trigger TICKET_AFTER_INSERT is triggered after inserting a row to the ticket table and updates the seats availability to N(no) in Train Status table if all the general and AC seats are booked.*/
DELIMITER //

CREATE  TRIGGER TICKET_AFTER_INSERT
AFTER INSERT
   ON TICKET FOR EACH ROW

BEGIN

DECLARE AC1 INT;
DECLARE GEN1 INT;

SELECT ACSEAT - BOOKEDACSEAT, GENSEAT - BOOKEDGENSEAT INTO AC1, GEN1 FROM TRAINSTATUS WHERE NEW.TRAINNO = TRAINSTATUS.TRAINNO AND NEW.TRAVELINGDATE = TRAINSTATUS.TRAINDATE;

IF(AC1 <=0 AND GEN1 <=0 ) THEN
Update TRAINSTATUS SET AVAILABILITYOFSEATS='N' 
                    WHERE NEW.TRAINNO = TRAINSTATUS.TRAINNO AND NEW.TRAVELINGDATE = TRAINSTATUS.TRAINDATE;
END IF;

END; //

DELIMITER ;

insert into TRAINSTATUS values(2007,20180725, 'Y',20, 30, 20, 30);

Insert into TICKET(ticketId,userId,status,trainNo, travelingDate) values(3010, 1004, 'C', 2007, 20180725);

/* Stored Procedure to update the ac and general seats after booking a ticket, throws error if all the seats are booked*/
DELIMITER //

CREATE  PROCEDURE BOOKTICKET_UPDATE_SEAT(IN TRAINNUMBER INT, IN ASEAT VARCHAR(50), IN GSEAT VARCHAR(50), IN TRAINDAT DATE)

BEGIN

	DECLARE AS1 INT;
    DECLARE GS1 INT;
    DECLARE BAS1 INT;
    DECLARE BGS1 INT;
 

SELECT ACSEAT, GENSEAT, BOOKEDACSEAT, BOOKEDGENSEAT INTO AS1, GS1, BAS1, BGS1
    FROM TRAINSTATUS
   WHERE TRAINNO = TRAINNUMBER AND TRAINDATE = TRAINDAT;
   
    IF ( BAS1 + ASEAT <= AS1) THEN UPDATE  TRAINSTATUS SET BOOKEDACSEAT = BOOKEDACSEAT + ASEAT WHERE TRAINNO = TRAINNUMBER AND TRAINDATE = TRAINDAT; 
		END IF;
	IF ( BGS1 + GSEAT <= GS1) THEN UPDATE  TRAINSTATUS SET BOOKEDGENSEAT = BOOKEDGENSEAT + GSEAT WHERE TRAINNO = TRAINNUMBER AND TRAINDATE = TRAINDAT; 
		END IF; 
    
         
	IF (BAS1 + ASEAT > AS1 ) THEN SIGNAL SQLSTATE '45000'  SET MESSAGE_TEXT = "ACSEATS ARE NOT AVAILABLE"; END IF;
    IF (BGS1 + GSEAT > GS1 ) THEN SIGNAL SQLSTATE '45000'  SET MESSAGE_TEXT = "GENSEATS ARE NOT AVAILABLE"; END IF;
   
END //

DELIMITER ;
    
    DROP PROCEDURE BOOKTICKET_UPDATE_SEAT;
    
CALL BOOKTICKET_UPDATE_SEAT(2007, 21, 30, 20180701);


/* Stored Procedure to update the ac and general seats after canceling the ticket, throws error if all the seats are empty*/
DELIMITER //

CREATE  PROCEDURE CANCELTICKET_UPDATE_SEAT(IN TRAINNUMBER INT, IN ASEAT VARCHAR(50), IN GSEAT VARCHAR(50), IN TRAINDAT DATE)

BEGIN

    DECLARE BAS1 INT;
    DECLARE BGS1 INT;
 

SELECT BOOKEDACSEAT, BOOKEDGENSEAT INTO BAS1, BGS1
    FROM TRAINSTATUS
   WHERE TRAINNO = TRAINNUMBER AND TRAINDATE = TRAINDAT;
   
    IF ( ASEAT <= BAS1) THEN UPDATE  TRAINSTATUS SET BOOKEDACSEAT = BOOKEDACSEAT - ASEAT WHERE TRAINNO = TRAINNUMBER AND TRAINDATE = TRAINDAT; 
		END IF;
	IF ( GSEAT <= BGS1) THEN UPDATE  TRAINSTATUS SET BOOKEDGENSEAT = BOOKEDGENSEAT - GSEAT WHERE TRAINNO = TRAINNUMBER AND TRAINDATE = TRAINDAT; 
		END IF; 
    
         
	IF (ASEAT > BAS1 ) THEN SIGNAL SQLSTATE '45000'  SET MESSAGE_TEXT = "CANNOT CANCEL ACSEATS"; END IF;
    IF (GSEAT > BGS1) THEN SIGNAL SQLSTATE '45000'  SET MESSAGE_TEXT = "CANNOT CANCEL GENSEATS"; END IF;
   
END //

DELIMITER ;

CALL CANCELTICKET_UPDATE_SEAT(2005, 0, 25, 20180701);



