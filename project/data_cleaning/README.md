# Data Cleaning
here we clean the data by a detailed analysis of each column:

## 1. YEAR
deleted as same values.

## 2. QUARTER
deleted as filled with only 2 values, interpretable using `FL_DATE`

## 3. MONTH
no change

## 4. DAY_OF_MONTH
no change

## 5. DAY_OF_WEEK
- new column added which gives us day in 3-letters instead of numbers like 1, 2, 3 etc, it gives Mon, Tue, Wed.
- datatype to string

## 6. FL_DATE
- datatype changed to date
- changed col_name to `FLIGHT_DATE`

## 7. MKT_UNIQUE_CARRIER
- datatype to string
- renamed to `MARKETING_CARRIER_CODE`

## 8. MKT_CARRIER_FL_NUM
- renamed to `MARKETING_FLIGHT_NUMBER`

## 9. TAIL_NUM
- datatype to string
- filled missing values - 162925 rows with `CANCELLED` as those flights were cancelled so no aircraft number
- filled missing values - 2 rows with `UNKNOWN` as those did run but their aircraft numbers were not entered
- renamed to `AIRCRAFT_TAIL_NUMBER`

## 10. ORIGIN
- string datatype
- renamed to `ORIGIN_AIRPORT_CODE`

## 11. ORIGIN_CITY_NAME
- string datatype

## 12. ORIGIN_STATE_ABR
- string datatype
- renamed to `ORIGIN_STATE_CODE`

## 13. ORIGIN_STATE_NM
- string datatype
- renamed to `ORIGIN_STATE_NAME`

## 14. DEST
- string datatype
- renamed to `DEST_AIRPORT_CODE`

## 15. DEST_CITY_NAME
- string datatype

## 16. DEST_STATE_ABR
- string datatype
- renamed to `DEST_STATE_CODE`

## 17. DEST_STATE_NM
- string datatype
- renamed to `DEST_STATE_NAME`

## 18. CRS_DEP_TIME
- created a new column: `CRS_DEP_HOUR` which extracts the HOUR of that departure time. This is useful for grouping flights by hour of departure.
- need to make a DAY/NIGHT column in DAX
- renamed `CRS_DEP_TIME` to `SCHEDULED_DEP_TIME` and `CRS_DEP_HOUR` to `SCHEDULED_DEP_HOUR`

## 19. DEP_TIME
- converted to int
- filled missing values: filled all cancelled flights with -1 (as they didn't depart)
- inconsistency: fixed 2400 values to 0000
- created a new column: `DEP_HOUR`
- renamed `DEP_TIME` to `ACTUAL_DEP_TIME` and `DEP_HOUR` to `ACTUAL_DEP_HOUR`

## 20. DEP_DELAY
- converted to int
- filled missing values: filled all cancelled flights with 
    - 9999 as its a placeholder that they did not depart. this is for columns: `DEP_DELAY` and `ARR_DELAY`. 
    - then for the rest of the cancelled flights, filled with -1 (as they didn't depart). did this for all cancelled flight columns: '`DEP_DELAY_NEW`', '`TAXI_OUT`', '`TAXI_IN`', '`WHEELS_OFF`', '`WHEELS_ON`', '`ARR_TIME`',  '`ARR_DELAY_NEW`', '`CARRIER_DELAY`', '`WEATHER_DELAY`', '`NAS_DELAY`', '`SECURITY_DELAY`', '`LATE_AIRCRAFT_DELAY`' 
    - and then filled all cancelled flight columns with 0: '`ACTUAL_ELAPSED_TIME`', '`AIR_TIME`'. 

## 21. DEP_DELAY_NEW
- dropped as its the same thing as `DEP_DELAY` but with a filter for less than 0 values.

## 22. DEP_DEL15
- filled missing values: cancelled flights were missing - filled with -1 as 0 indicated less than 15 min and 1 indicated more than 15min. so -1 indicates cancelled.
    - then extracted overall all cancelled flights and some flights had taken off but were cancelled, so they had `dep_delay` values, so put all their values as -1
- mapped the column to 
```
cancel_map = {
    0.0: 'Less than 15',
    1.0: 'Greater than 15',
    -1.0: 'Cancelled'
}
```
- datatype to string
- renamed col to `DEP_DELAY_15_MIN`

## 23. DEP_DELAY_GROUP
- filled missing values: cancelled flights were missing, filled with 9999 as -2 to 12 was taken.
- mapped the column:
```
cancel_map = {
    -2.0: '15-30 min early',
    -1.0: '0-15 min early',
    0.0: '0-15 min late', 
    1.0: '15-30 min late', 
    2.0: '30-45 min late', 
    3.0: '45-60 min late', 
    4.0: '60-75 min late', 
    5.0: '75-90 min late', 
    6.0: '90-105 min late', 
    7.0: '105-120 min late', 
    8.0: '120-135 min late', 
    9.0: '135-150 min late', 
    10.0: '150-165 min late', 
    11.0: '165-180 min late', 
    12.0: '180-195 min late',
    9999.0: 'Cancelled'
}
```
- converted to string datatype

## 24. DEP_TIME_BLK
- dropped as same to `SCHEDULED_DEP_HOUR`

## 25. TAXI_OUT
- filled missing values: all are cancelled flights,
    - filled -1 to signify time that it was cancelled in the columns: '`TAXI_OUT`', '`TAXI_IN`', '`WHEELS_OFF`', '`WHEELS_ON`', '`ARR_TIME`', '`ARR_DELAY_NEW`', '`CARRIER_DELAY`', '`WEATHER_DELAY`', '`NAS_DELAY`', '`SECURITY_DELAY`', '`LATE_AIRCRAFT_DELAY`'
    - filled 0 to signify time taken that it was cancelled in the columns: '`ACTUAL_ELAPSED_TIME`', '`AIR_TIME`'
- converted from float to integer