-- --  FIXING ALL THE DATA TYPE

ALTER TABLE ola_data_clean ADD COLUMN new_date DATE;
UPDATE ola_data_clean 
SET 
    new_date = STR_TO_DATE(TRIM(Date), '%m/%d/%Y');
ALTER TABLE ola_data_clean DROP COLUMN Date;
ALTER TABLE ola_data_clean CHANGE new_date Date DATE;
ALTER TABLE ola_data_clean ADD COLUMN temp_time TIME;
UPDATE ola_data_clean 
SET 
    temp_time = CAST(TRIM(`Time`) AS TIME);
SELECT 
    COUNT(*)
FROM
    ola_data_clean
WHERE
    temp_time IS NULL;
ALTER TABLE ola_data_clean DROP COLUMN `Time`;
ALTER TABLE ola_data_clean CHANGE temp_time `Time` TIME;
ALTER TABLE ola_data_clean 
DROP COLUMN new_datetime,
DROP COLUMN new_date,
DROP COLUMN new_time;
ALTER TABLE ola_data_clean
MODIFY COLUMN Ride_Distance FLOAT,
MODIFY COLUMN V_TAT FLOAT,
MODIFY COLUMN C_TAT FLOAT,
MODIFY COLUMN Driver_Ratings FLOAT,
MODIFY COLUMN Booking_Value int,
MODIFY COLUMN Customer_Rating FLOAT;



-- -- STARTING ANALYZE AND ANSWERING BUSINESS QUESTION

select * from ola_project.ola_data_clean;

-- -- 1. RETRIEVE ALL SUCCESSFULL BOOKING
SELECT 
    *
FROM
    ola_project.ola_data_clean
WHERE
    Booking_Status = 'Success';
SELECT 
    COUNT(*) AS Total_Successfull_Booking
FROM
    ola_project.ola_data_clean
WHERE
    Booking_Status = 'Success';
    

-- -- 2. FIND THE AVERAGE RIDE DISTANCE FOR EACH VEHICLE TYPE
SELECT 
    Vehicle_Type,
    ROUND(AVG(Ride_Distance), 2) AS Average_Distance
FROM
    ola_project.ola_data_clean
GROUP BY Vehicle_Type;


-- -- 3. GET THE TOTAL NUMBER OF CANCELLED RIDES BY CUSTOMER
SELECT 
    COUNT(*) AS Rides_Cancelled_By_Customers
FROM
    ola_project.ola_data_clean
WHERE
    Canceled_Rides_by_Customer = 'Not Cancelled';


-- -- 4. LIST THE TOP 5 CUSTOMERS WHO BOOKED THE HIGHEST NUMBER OF RIDES
SELECT 
    Customer_ID, COUNT(*) AS Total_Rides
FROM
    ola_project.ola_data_clean
GROUP BY Customer_ID
ORDER BY total_rides DESC
LIMIT 5;


-- -- 5. GET THE NUMBER OF RIDES CANCELLED BY DRIVER DUE TO PERSONAL OR CAR RELATED ISSUES
SELECT 
    COUNT(*) AS Total_Rides_Cancelled_By_Driver
FROM
    ola_project.ola_data_clean
WHERE
    Canceled_Rides_by_Driver = 'Personal & Car related issue';
    
    
-- -- 6. FIND THE MINIMUM AND MAXIMUM DRIVER RATINGS FROM PRIME SEDAN BOOKINGS
SELECT 
    MAX(Driver_Ratings) AS Maximum_Rating,
    MIN(Driver_Ratings) AS Minimum_Rating
FROM
    ola_project.ola_data_clean
WHERE
    Vehicle_Type = 'Prime Sedan';


-- -- 7. RETRIVE ALL RIDES WHERE PAYMENT WAS MADE BY UPI
SELECT 
    *
FROM
    ola_project.ola_data_clean
WHERE
    Payment_Method = 'UPI';
SELECT 
    COUNT(*) AS Total_UPI_Payment
FROM
    ola_project.ola_data_clean
WHERE
    Payment_Method = 'UPI';
    
    
-- -- 8. FIND AVERAGE CUSTOMER RATING PER VEHICLE TYPE
SELECT 
    Vehicle_Type,
    ROUND(AVG(Customer_Rating), 2) AS Average_Rating
FROM
    ola_project.ola_data_clean
GROUP BY Vehicle_Type;


-- -- 9. CALCULATE THE TOTAL BOOKING VALUE OF RIDES COMPLETED SUCCESSFULLY
SELECT 
    SUM(Booking_Value) AS Total_Booking_Value
FROM
    ola_project.ola_data_clean
WHERE
    Booking_Status = 'Success';
    
    
-- -- 10. LIST ALL INCOMPLETE RIDES ALONG WITH THE REASON
SELECT 
    Booking_ID, Incomplete_Rides_Reason
FROM
    ola_data_clean
WHERE
    Incomplete_Rides_Reason != 'Not Applicable'
ORDER BY Incomplete_Rides_Reason;