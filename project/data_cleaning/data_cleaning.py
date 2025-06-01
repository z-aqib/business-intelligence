#!/usr/bin/env python
# coding: utf-8

# Business Intelligence Project    
# Name: Zehra Ahmed, Farah Inayat, Kisa Fatima, Zuha Aqib    
# Date: 18-May-2025

# In[252]:


# print when the last code was run
from datetime import datetime
datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# In[253]:


# Capture start time
start_time = datetime.now()


# # Imports

# In[254]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime, timedelta

import math


# ### Some Functions
# some preliminary functions we can use in the code

# # Data Loading

# In[255]:


# Load the dataset
df = pd.read_csv('../data/flights_jantojun2020_3M.csv')

pd.set_option('display.max_columns', None)


# In[256]:


df


# In[257]:


df.shape


# In[258]:


# Function to get current date and time as a string
def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# # Data Preparation

# ## Data Statistics

# In[259]:


# Check for missing values
print("Missing values per column:")
df.isnull().sum()


# In[260]:


# Display data types
print("\nData types:")
df.dtypes


# In[261]:


# Get summary statistics
print("\nSummary statistics:")
df.describe(include='all')


# In[ ]:





# ## Changing Data Type

# ### Defined Functions
# here are some functions we can use for changing the datatype

# In[262]:


def to_string(df, column_name):
    """
    Convert a pandas DataFrame column to a string.
    """
    df[column_name] = df[column_name].astype('string')
    print(f"Column Name: '{column_name}', Type: {df[column_name].dtype}")
    return df  


# In[263]:


def to_date(df, column_name, format=None):
    """
    Convert a pandas DataFrame column to datetime.
    """
    df[column_name] = pd.to_datetime(df[column_name], format=format)
    print(f"Column Name: '{column_name}', Type: {df[column_name].dtype}")
    return df


# In[264]:


def to_int(df, column_name):
    """
    Convert a pandas DataFrame column to a int.
    """
    df[column_name] = df[column_name].notna().astype('int64')
    print(f"Column Name: '{column_name}', Type: {df[column_name].dtype}")
    return df  


# In[265]:


def to_float(df, column_name):
    """
    Convert a pandas DataFrame column to a float.
    """
    df[column_name] = df[column_name].astype('float64')
    print(f"Column Name: '{column_name}', Type: {df[column_name].dtype}")
    return df  


# # Column by Column Analysis
# so here for each of the 47 columns, we will be doing a thourough analysis on each like whether we are keeping them, dropping them, if they need to be renamed, any datatype to be changed, are there any missing values, etc. 

# In[266]:


# a function to display all statistics of a column
def show_unique_missing_dtype(df, columnName):
    print(df[columnName].value_counts())
    print("\nmissing values: ", df[columnName].isna().sum())
    print("\ndatatype: ", df[columnName].dtype)


# ## YEAR

# In[267]:


show_unique_missing_dtype(df, 'YEAR')


# so every row is just filled with 2020's so it is useless. so better to drop the column as it does not give us any insight.

# In[268]:


df = df.drop('YEAR', axis=1)


# ## QUARTER

# In[269]:


show_unique_missing_dtype(df, 'QUARTER')


# so this is just filled with 2 values - 1 and 2. not very effective. we can also get the QUARTER using drill down strategy using `FL_DATE` in powerBI. so better to drop.

# In[270]:


df = df.drop('QUARTER', axis=1)


# ## MONTH

# In[271]:


show_unique_missing_dtype(df, 'MONTH')


# so there are no missing values, and the value counts seem fine. the datatype is fine too.

# ## DAY_OF_MONTH

# In[272]:


show_unique_missing_dtype(df, 'DAY_OF_MONTH')


# so we see that majority of flights take place on 3rd of each month and the least flights tak place on 31st. theres a very large decrease of flights on 30th and 31st. now the datatype is fine, there are no missing values, and they do give some meaning. so no need to remove column.

# ## DAY_OF_WEEK

# In[273]:


show_unique_missing_dtype(df, 'DAY_OF_WEEK')


# so majority of flights flew at 5:Friday and least amount of flights on 6:Saturday. not a very large difference, but there is a difference. so it does give some analysis. there are no missing values. but this is not very understandable, especially the 1-7. so lets map it to actual days, but only the first three letters to save space.

# In[274]:


# define the mapping
num_to_day = {
    1: "Mon",
    2: "Tue",
    3: "Wed",
    4: "Thu",
    5: "Fri",
    6: "Sat",
    7: "Sun"
}

# replace in your DataFrame (in-place)
df['day_of_week_c'] = df['DAY_OF_WEEK'].map(num_to_day)


# In[275]:


# Get list of current columns
cols = list(df.columns)

# Move 'day_of_week_c' to be right after 'DAY_OF_WEEK'
day_index = cols.index('DAY_OF_WEEK')
cols.insert(day_index + 1, cols.pop(cols.index('day_of_week_c')))

# Reorder DataFrame
df = df[cols]


# change the datatype to string and recheck the unique values to verify that the mapping is done correctly

# In[276]:


df = to_string(df, 'day_of_week_c')


# In[277]:


show_unique_missing_dtype(df, 'day_of_week_c')


# ## FL_DATE

# In[278]:


show_unique_missing_dtype(df, 'FL_DATE')


# so we see that the majority flights were on 20th March 2020. now convert the data to datatype `DATE`. no missing values. 

# In[279]:


# convert FL_DATE from '3/20/2020' strings to actual dates
df = to_date(df, 'FL_DATE', format='%m/%d/%Y')


# lets rename the column to make it more clear, to `flight_date`

# In[280]:


df.rename(columns={
    'FL_DATE': 'FLIGHT_DATE'
}, inplace=True)


# ## MKT_UNIQUE_CARRIER

# In[281]:


show_unique_missing_dtype(df, 'MKT_UNIQUE_CARRIER')


# so we see that the `AA` carrier is most used whereas the `HA` carrier is least. no missing values. does give meaningful information. lets convert its `dtype` to `string`.

# In[282]:


df = to_string(df, 'MKT_UNIQUE_CARRIER')


# lets make the name more meaningful - so this column is basically the airline that MARKETS you the ticket. the airline that flies you is the OPERATING CARRIER. so lets rename as `marketing_carrier_code`    
# - Marketing Carrier (MKT_UNIQUE_CARRIER): the airline that sells or markets the flight—i.e. whose flight number appears on your ticket.
# - Operating Carrier (OP_CARRIER): the airline that actually operates the flight (the plane and crew).

# In[283]:


df.rename(columns={
    'MKT_UNIQUE_CARRIER': 'MARKETING_CARRIER_CODE'
}, inplace=True)


# ## MKT_CARRIER_FL_NUM

# In[284]:


show_unique_missing_dtype(df, 'MKT_CARRIER_FL_NUM')


# so `MKT_CARRIER_FL_NUM` is the flight number. we see that flight number `1095` is flown the most. no missing values. datatype is fine. again, lets rename to something more menaingful and understandable

# In[285]:


df.rename(columns={
    'MKT_CARRIER_FL_NUM': 'MARKETING_FLIGHT_NUMBER'
}, inplace=True)


# ## TAIL_NUM

# In[286]:


show_unique_missing_dtype(df, 'TAIL_NUM')


# so `tail_num` is the Aircraft Tail Number. it usually starts with N. it has 160k missing values. first lets change its datatype to string.

# In[287]:


df = to_string(df, 'TAIL_NUM')


# now lets move to missing values. first we need to check if all those flights were cancelled

# In[288]:


# 1. Filter to only the rows where TAIL_NUM is missing
missing_tail = df[df['TAIL_NUM'].isna()]

# 2. How many of those were cancelled?
cancel_counts = missing_tail['CANCELLED'].value_counts(dropna=False)

cancel_counts


# In[289]:


# Of the missing-tail flights, how many have a non-null CANCELLATION_CODE?
missing_tail['CANCELLATION_CODE'].notna().value_counts()


# oh so only 2 rows were not cancelled but majority was. so a cancelled flight will obviously not have an aircraft. so lets fill those aircraft numbers with 'CANCELLED'

# In[290]:


# Mark all cancelled flights’ TAIL_NUM as “CANCELLED”
df.loc[
    (df['TAIL_NUM'].isna()) & (df['CANCELLED'] == 1),
    'TAIL_NUM'
] = 'CANCELLED'


# done. lets just check it

# In[291]:


show_unique_missing_dtype(df, 'TAIL_NUM')


# ah so still 2 flights are left. so first lets extract them and see how they look, what other thing are missing, what they could be

# In[292]:


# get the two “non-cancelled but tail‐missing” flights
problem = df[(df['TAIL_NUM'].isna())]
problem


# so they flew on the same day = 31st march 2020 - one at 2:22pm and one at 5:21pm. both were not cancelled, just their aircraft numbers were not noted. now they are real flights and just dropping them would loose data. so lets just keep them and fill their `tail_num` with UNKNOWN.

# In[293]:


df.loc[
  (df['TAIL_NUM'].isna()) & (df['CANCELLED'] == 0),
  'TAIL_NUM'
] = 'UNKNOWN'


# and lets recheck

# In[294]:


show_unique_missing_dtype(df, 'TAIL_NUM')


# lets also make its name easier to understand and interpret. so lets change its name to `aircraft_tail_number`

# In[295]:


df.rename(columns={
    'TAIL_NUM': 'AIRCRAFT_TAIL_NUMBER'
}, inplace=True)


# ## ORIGIN

# In[296]:


show_unique_missing_dtype(df, 'ORIGIN')


# so this is Flight Departure 3-Letter Airport Abbreviation. no missing values. we do get insights of the most flew-out of city and least flew-out city - data is meaningful. lets just change the datatype to string. 

# In[297]:


df = to_string(df, 'ORIGIN')


# ## ORIGIN_CITY_NAME

# In[298]:


show_unique_missing_dtype(df, 'ORIGIN_CITY_NAME')


# before looking at the values, lets make the datatype as string

# In[299]:


df = to_string(df, 'ORIGIN_CITY_NAME')


# so thats very weird. according to the previous `origin`, we see that 
# - `Atlanta, GA` corresponds to `ATL`. 
# - `Dallas/Fort Worth, TX` corresponds to `DFW`. 
# - `Denver, CO` for `DEN`. 
# - `Charlotte, NC` for `CLT`. 
# - `Cold Bay, AK` for `CDB`. 
# - `Pago Pago, TT` for `PPG`. 
# - `Martha's Vineyard, MA` for `MVY`. 
# - `Quincy, IL` for `UIN`. 
# - `Branson, MO` for `BKG`.    
#  
# BUT      
# `Chicago, IL` doesnt correspond to any. `ORD` does not correspond to any. which is fishy - data is inconsistent.   

# so lets do this. lets get each unique value in `origin` and extract their rows. then lets extract all the `value_counts ()` and see if they have more than one unique value. if yes, lets see it, if not, ignore.

# In[300]:


# 1. How many unique ORIGIN values?
num_origins = df['ORIGIN'].nunique()
print(f"Number of unique ORIGIN codes: {num_origins}")

# 2. Iterate over each unique ORIGIN value
unique_col1 = df['ORIGIN'].unique()
count = 0
for col1_name in unique_col1:
    rows = df[df['ORIGIN'] == col1_name]
    num_uniques = rows['ORIGIN_CITY_NAME'].nunique()
    count+=1
    if num_uniques > 1:
        print(f"Processing ORIGIN = {col1_name}")
        print(rows['ORIGIN_CITY_NAME'].value_counts())
    if count % 20 == 0:
        print("processed", count)


# so basically we saw that all the `ORIGIN` map to one city. now lets do this: lets just explore the one we were fishy about - `ORIGIN = ORD`

# In[301]:


rows = df[df['ORIGIN'] == 'ORD']
rows['ORIGIN_CITY_NAME'].value_counts()


# so looks like `Chicago, IL` for `ORD` is fine. lets do the opposite now - for every `origin_city_name`, lets find its corresponding `origin` and extract all the >1 unique names. 

# In[302]:


# 1. How many unique ORIGIN_CITY_NAME values?
num_origins = df['ORIGIN_CITY_NAME'].nunique()
print(f"Number of unique ORIGIN_CITY_NAME codes: {num_origins}")

# 2. Iterate over each unique ORIGIN_CITY_NAME value
unique_col1 = df['ORIGIN_CITY_NAME'].unique()
count = 0
for col1_name in unique_col1:
    rows = df[df['ORIGIN_CITY_NAME'] == col1_name]
    num_uniques = rows['ORIGIN'].nunique()
    count+=1
    if num_uniques > 1:
        print(f"Processing ORIGIN_CITY_NAME = {col1_name}")
        print(rows['ORIGIN'].value_counts())
    if count % 20 == 0:
        print("----processed", count)


# so heres the tea. so after a little searching on internet (and chatGPT) multiple `origin` code does not mean data inconsistency, but it means that that city had more than one airport - as `origin` is the AIRPORT ABBREVIATION. not the CITY ABBREVIATION. so this is something to note. to make this more clearer, lets rename `origin` to something more meaningful like `origin_airport_code`

# In[303]:


df.rename(columns={'ORIGIN': 'ORIGIN_AIRPORT_CODE'}, inplace=True)


# lets give it a final recheck because it was altered

# In[304]:


show_unique_missing_dtype(df, 'ORIGIN_AIRPORT_CODE' )


# ## ORIGIN_STATE_ABR

# In[305]:


show_unique_missing_dtype(df, 'ORIGIN_STATE_ABR')


# so first off, lets change the datatype to string

# In[306]:


df = to_string(df, 'ORIGIN_STATE_ABR')


# so no missing values. this is a good thing. so this column basically tells us the Flight Departure 2-Letter State Abbreviation. So we can use this column to get the state of the flight departure. this is meaningful, we will keep it, but lets rename the column to something more meaningful like `origin_state_code`

# In[307]:


df.rename(columns={
    'ORIGIN_STATE_ABR': 'ORIGIN_STATE_CODE'
}, inplace=True)


# ## ORIGIN_STATE_NM

# In[308]:


show_unique_missing_dtype(df, 'ORIGIN_STATE_NM')


# so lets change its datatype to string

# In[309]:


df = to_string(df, 'ORIGIN_STATE_NM')


# so no missing values. this is the same as the last column however this is full name. lets check does it map 1 to 1? we need to check for any inconsistencies because last time we found the differenc in airport codes and city names. 

# In[310]:


column1 = 'ORIGIN_STATE_CODE'
column2 = 'ORIGIN_STATE_NM'

# 1. How many unique column1 values?
num_origins = df[column1].nunique()
print(f"Number of unique", column1, "codes: {num_origins}")

# 2. Iterate over each unique column1 value
unique_col1 = df[column1].unique()
count = 0
for col1_name in unique_col1:
    rows = df[df[column1] == col1_name]
    num_uniques = rows[column2].nunique()
    count+=1
    if num_uniques > 1:
        print(f"Processing ", column1, " = {col1_name}")
        print(rows[column2].value_counts())
    if count % 20 == 0:
        print("processed", count)


# In[311]:


column1 = 'ORIGIN_STATE_NM'
column2 = 'ORIGIN_STATE_CODE'

# 1. How many unique column1 values?
num_origins = df[column1].nunique()
print(f"Number of unique", column1, "codes: {num_origins}")

# 2. Iterate over each unique column1 value
unique_col1 = df[column1].unique()
count = 0
for col1_name in unique_col1:
    rows = df[df[column1] == col1_name]
    num_uniques = rows[column2].nunique()
    count+=1
    if num_uniques > 1:
        print(f"Processing ", column1, " = {col1_name}")
        print(rows[column2].value_counts())
    if count % 20 == 0:
        print("processed", count)


# so looks like all the data is consistent and maps to the same one. This is a good thing. lets just rename the column to something more meaningful

# In[312]:


df.rename(columns={
    'ORIGIN_STATE_NM': 'ORIGIN_STATE_NAME'
}, inplace=True)


# ## DEST

# In[313]:


show_unique_missing_dtype(df, 'DEST')


# so this is again AIRPORT CODES and not CITY CODES. lets rename this to `DEST_AIRPORT_CODE` 

# In[314]:


df.rename(columns={
    'DEST': 'DEST_AIRPORT_CODE'
}, inplace=True)


# and now lets change the datatype to string

# In[315]:


df = to_string(df, 'DEST_AIRPORT_CODE')


# ## DEST_CITY_NAME

# In[316]:


show_unique_missing_dtype(df, 'DEST_CITY_NAME')


# so no missing values. the data is same as we discussed for origin, this is destination city name. so name is menaingful and changing is not needed. so lets change datatype to string

# In[317]:


df = to_string(df, 'DEST_CITY_NAME')


# ## DEST_STATE_ABR

# In[318]:


show_unique_missing_dtype(df, 'DEST_STATE_ABR')


# so this is fine. no missing values. lets change the datatype to string

# In[319]:


df = to_string(df, 'DEST_STATE_ABR')


# lets rename the column in the same way for origin so that its consistent

# In[320]:


df.rename(columns={
    'DEST_STATE_ABR': 'DEST_STATE_CODE'
}, inplace=True)


# ## DEST_STATE_NM 

# In[321]:


show_unique_missing_dtype(df, 'DEST_STATE_NM')


# so no missing values. lets change datatype and rename the same way as origin

# In[322]:


df = to_string(df, 'DEST_STATE_NM')


# In[323]:


df.rename(columns={
    'DEST_STATE_NM': 'DEST_STATE_NAME'
}, inplace=True)


# ## CRS_DEP_TIME

# In[324]:


show_unique_missing_dtype(df, 'CRS_DEP_TIME')


# so no missing values. this is the SCHEDULED DEP TIME. majority flights happen at 6am and at whole numbers like 6am, 7am, 8am etc. but this is not very interpretable, we cannot make any understanding from this. but what is more interpretable is that we get the HOURS of departure. i.e. 4:52 means 4. 1:46 means 1. etc. i want to be able to interpret what is the most hour of departure flights? same for arrival.

# In[325]:


def extract_hour(df: pd.DataFrame, time_col: str, hour_col: str) -> pd.DataFrame:
    """
    Given a DataFrame and a column like 'CRS_DEP_TIME' or 'CRS_ARR_TIME' 
    in HMM or HHMM integer form, creates a new column with just the hour.

    Examples:
      3    → 0   (00:03)
      614  → 6   (06:14)
      2300 → 23  (23:00)
    """
    # ensure numeric, coerce errors to NaN
    times = pd.to_numeric(df[time_col], errors='coerce').fillna(0).astype(int)
    
    # integer-divide by 100 to get the hour bucket
    df[hour_col] = times // 100
    
    # Get list of current columns
    cols = list(df.columns)

    # Move hour_col to be right after time_col
    day_index = cols.index(time_col)
    cols.insert(day_index + 1, cols.pop(cols.index(hour_col)))
    
    # Reorder DataFrame
    df = df[cols]
    
    return df


# so lets make a new column which extracts the times

# In[326]:


df = extract_hour(df, 'CRS_DEP_TIME', 'CRS_DEP_HOUR')


# lets review its statistics and recheck

# In[327]:


show_unique_missing_dtype(df, 'CRS_DEP_HOUR')


# after this, we can even make a DAY/NIGHT column in `DAX`. right now its not necessary. now lets rename both column names to make it more understandable.

# In[328]:


df.rename(columns={
    'CRS_DEP_TIME': 'SCHEDULED_DEP_TIME',
    'CRS_DEP_HOUR': 'SCHEDULED_DEP_HOUR'
}, inplace=True)


# ## DEP_TIME

# In[329]:


show_unique_missing_dtype(df, 'DEP_TIME')


# so there are missing values in the data. lets deal with these in a bit. first lets deal with datatype - why is it float ? lets check if all values are whole floats so that we can easily convert to int?

# In[330]:


def check_if_int(df, col):
    # 1. Check for non-null values that aren’t whole numbers
    #    This will be False if any x has a fractional part.
    is_every_int = (df[col]
                    .dropna()              # ignore NaNs
                    .mod(1)                # x % 1
                    .eq(0)                 # check == 0
                    .all()                 # all True?
                )

    print(f"All non-missing ", col, " values are integers? {is_every_int}")
    return is_every_int

is_every_int = check_if_int(df, 'DEP_TIME')


# ah so they are whole decimals. lets convert datatype to integer

# In[331]:


def convert_int(is_every_int, df, col):
    # 2. If True, convert to an integer dtype.
    if is_every_int:
        if df[col].isna().sum() > 0:
            # If you still have NaNs, use the pandas nullable Int64 dtype:
            df[col] = df[col].astype('Int64')
        else:
            # Otherwise, for no-missing data, you can do:
            df[col] = df[col].astype('Int64')
        print("converted successfully")
    else:
        print("Warning: some ", col, " values have fractional parts—inspect those before casting.")
    return df

df = convert_int(is_every_int, df, 'DEP_TIME')


# In[332]:


def convert_to_int(df, column):
    int = check_if_int(df, column)
    df = convert_int(int, df, column)
    return df


# now lets revisit its statistics

# In[333]:


show_unique_missing_dtype(df, 'DEP_TIME')


# great, so now lets deal with missing values. lets extract all the missing rows and check - are they all cancelled?

# In[334]:


missing_rows = df[df['DEP_TIME'].isna()]
# 2. How many of those were cancelled?
cancel_counts = missing_rows['CANCELLED'].value_counts(dropna=False)

cancel_counts


# In[335]:


def check_if_cancelled(df, col):
    missing_rows = df[df[col].isna()]
    # 2. How many of those were cancelled?
    print(missing_rows['CANCELLED'].value_counts(dropna=False))
    return missing_rows


# ah so all were cancelled. lets fill with -1 to show its not departed

# In[336]:


missing_idx = missing_rows.index
df.loc[missing_idx, 'DEP_TIME'] = -1


# In[337]:


show_unique_missing_dtype(df, 'DEP_TIME')


# lets do the same for this, extract the hour

# In[338]:


df = extract_hour(df, 'DEP_TIME', 'DEP_HOUR')


# In[339]:


show_unique_missing_dtype(df, 'DEP_HOUR')


# okay so there is a problem - how can there be the hour "24"? looks like some data inconsistency is present which is causing it to be 24. lets extract and inspect those rows first

# In[340]:


# ensure the column is numeric
df['DEP_TIME_CLEAN'] = pd.to_numeric(df['DEP_TIME'], errors='coerce')

# filter rows with values > 2400
bad_times = df[df['DEP_TIME_CLEAN'] > 2400]
bad_times


# none. lets extract all those with equal to 2400

# In[341]:


# ensure the column is numeric
df['DEP_TIME_CLEAN'] = pd.to_numeric(df['DEP_TIME'], errors='coerce')

# filter rows with values = 2400
bad_times = df[df['DEP_TIME_CLEAN'] == 2400]
bad_times


# ah so it looks like all 2400 values mean raat 12 baje - i.e. 00:00. lets map all those values to 00:00 first

# In[342]:


# ensure numeric dtype
df['DEP_TIME'] = pd.to_numeric(df['DEP_TIME'], errors='coerce').astype('Int64')

# replace exactly 2400 → 0
df.loc[df['DEP_TIME'] == 2400, 'DEP_TIME'] = 0


# In[343]:


# RECHECK

# ensure the column is numeric
df['DEP_TIME_CLEAN'] = pd.to_numeric(df['DEP_TIME'], errors='coerce')

# filter rows with values = 2400
bad_times = df[df['DEP_TIME_CLEAN'] == 2400]
bad_times


# In[344]:


# remove dep_time_clean

df = df.drop('DEP_TIME_CLEAN', axis=1)


# lets re-evaluate dep_hour now

# In[345]:


df = extract_hour(df, 'DEP_TIME', 'DEP_HOUR')


# In[346]:


show_unique_missing_dtype(df, 'DEP_HOUR')


# and lets rename both columns to improve readability

# In[347]:


df.rename(columns={
    'DEP_TIME': 'ACTUAL_DEP_TIME',
    'DEP_HOUR': 'ACTUAL_DEP_HOUR'
}, inplace=True)


# ## DEP_DELAY

# In[348]:


show_unique_missing_dtype(df, 'DEP_DELAY')


# so lets check if its an integer or not and convert accordingly

# In[349]:


df = convert_to_int(df, 'DEP_DELAY')


# In[350]:


show_unique_missing_dtype(df, 'DEP_DELAY')


# so now lets deal with missing values by extracting them and their cancelled values

# In[351]:


missing_rows = check_if_cancelled(df, 'DEP_DELAY')


# In[352]:


missing_rows.isna().sum()


# so what do we fill them with? if we put `DEP_DELAY` as -1, it means all our flights were 1 minute early which skews and disrupts our analysis. so we need to fill with such a value that provides us a clear distinction that all these are cancelled. so lets try and extract the min/max values of the column

# In[353]:


min_delay = df['DEP_DELAY'].min()
max_delay = df['DEP_DELAY'].max()

print("min", min_delay)
print("max", max_delay)


# okay, lets also extract all the cancelled rows and see what they are filled with

# In[354]:


cancelled_all = df[df['CANCELLED'] == 1]
show_unique_missing_dtype(cancelled_all, 'DEP_DELAY')


# In[355]:


cancelled_all


# so this is giving us information that out of the 280k cancelled flights, roughly 1000 flights did take off before being cancelled - so they do have values for `dep_time` and `dep_delay`. now we dont want to loose that data. so lets fill the remaining null values with 9999 as its a unique placeholder which lets us know this flight never went. it was cancelled. we will do the same for `arr_delay`

# In[356]:


cols_to_fill = ['DEP_DELAY', 'ARR_DELAY']


# In[357]:


# Loop over each column and fill NaNs with 0 in the original df using cancelled_only's index
for col in cols_to_fill:
    missing_idx = missing_rows[missing_rows[col].isna()].index
    df.loc[missing_idx, col] = 9999


# so lets make all these null columns as -1 to show that it is a cancelled flight

# In[358]:


cols_to_fill = ['DEP_DELAY_NEW', 'TAXI_OUT', 'TAXI_IN', 'WHEELS_OFF', 'WHEELS_ON', 'ARR_TIME', 'ARR_DELAY_NEW', 'CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY']


# In[359]:


# Loop over each column and fill NaNs with 0 in the original df using cancelled_only's index
for col in cols_to_fill:
    missing_idx = missing_rows[missing_rows[col].isna()].index
    df.loc[missing_idx, col] = -1


# and now lets fill elapsed time and etc with 0 to indicate it was of 0 time

# In[360]:


cols_to_fill = ['ACTUAL_ELAPSED_TIME', 'AIR_TIME']


# In[361]:


# Loop over each column and fill NaNs with 0 in the original df using cancelled_only's index
for col in cols_to_fill:
    missing_idx = missing_rows[missing_rows[col].isna()].index
    df.loc[missing_idx, col] = 0


# lets just give a quick recheck

# In[362]:


show_unique_missing_dtype(df, 'DEP_DELAY')


# In[363]:


cancelled_all = df[df['CANCELLED'] == 1]
show_unique_missing_dtype(cancelled_all, 'DEP_DELAY')


# In[364]:


show_unique_missing_dtype(df, 'DEP_DELAY')


# ## DEP_DELAY_NEW

# In[365]:


show_unique_missing_dtype(df, 'DEP_DELAY_NEW')


# i feel as if this is just `DEP_DELAY` but all the `<0` values are put as 0. this is just the same data, repition and it can be achieved by putting a filter of greater than 0. so this column does not provide any meaningful information. we can just drop this column. 

# In[366]:


df = df.drop('DEP_DELAY_NEW', axis=1)


# ## DEP_DEL15

# In[367]:


show_unique_missing_dtype(df, 'DEP_DEL15')


# so this is not very meaningful. lets remap it to greater than 15 and lesser than 15. but before that, lets fill the missing values. so if `dep_delay` == 9999, then its cancelled. if its < 15 then its 0, and if its > 15 then its 1. lets first fill all the missing values. 

# In[368]:


missing_rows = df[df['DEP_DEL15'].isna()]
missing_rows.shape


# In[369]:


cancelled = missing_rows[missing_rows['DEP_DELAY'] == 9999]
cancelled.shape


# ah so all are cancelled, no need to fill with 0 or 1. just a direct fill of -1. 

# In[370]:


missing_idx = cancelled.index
df.loc[missing_idx, 'DEP_DEL15'] = -1


# In[371]:


show_unique_missing_dtype(df, 'DEP_DEL15')


# now lets map them

# In[372]:


cancel_map = {
    0.0: 'Less than 15',
    1.0: 'Greater than 15',
    -1.0: 'Cancelled'
}

df['DEP_DEL15'] = df['DEP_DEL15'].map(cancel_map)


# In[373]:


show_unique_missing_dtype(df, 'DEP_DEL15')


# that reminds me, we need to account for all the 1000 flights which took off but were cancelled. their `dep_delay` we will not change, but we can change their map

# In[374]:


missing_rows = df[df['CANCELLED'] == 1]
missing_rows['DEP_DEL15'].value_counts()


# so lets change them all to cancelled

# In[375]:


missing_idx = missing_rows.index
df.loc[missing_idx, 'DEP_DEL15'] = 'Cancelled'


# lets recheck

# In[376]:


missing_rows = df[df['CANCELLED'] == 1]
missing_rows['DEP_DEL15'].value_counts()


# In[377]:


show_unique_missing_dtype(df, 'DEP_DEL15')


# lets convert datatype to string and rename the column

# In[378]:


df = to_string(df, 'DEP_DEL15')


# In[379]:


df.rename(columns={
    'DEP_DEL15': 'DEP_DELAY_15_MIN'
}, inplace=True)


# ## DEP_DELAY_GROUP

# In[380]:


show_unique_missing_dtype(df, 'DEP_DELAY_GROUP')


# so this is 15 minute intervals. like -1 means -15 to 0, 0 means 0-15, 1 means 15-20 etc. so this isnt very readable or meaningful, better to map to strings. but first, lets fill the missing values - which by guess and proof - is cancelled flights. 

# In[381]:


missing_rows = df[df['DEP_DELAY_GROUP'].isna()]
missing_rows.shape


# In[382]:


cancelled = missing_rows[missing_rows['CANCELLED'] == 1]
cancelled.shape


# yep so all are cancelled. lets fill with 9999 to show cancelled

# In[383]:


missing_idx = cancelled.index
df.loc[missing_idx, 'DEP_DELAY_GROUP'] = 9999


# lets check it

# In[384]:


show_unique_missing_dtype(df, 'DEP_DELAY_GROUP')


# lets also analyse what all the cancelled flights are filled with

# In[385]:


cancelled_all = df[df['CANCELLED'] == 1]
cancelled_all['DEP_DELAY_GROUP'].value_counts()


# ah so thats not good. lets fill all with 9999 to make it consistent

# In[386]:


missing_idx = cancelled_all.index
df.loc[missing_idx, 'DEP_DELAY_GROUP'] = 9999


# In[387]:


cancelled_all = df[df['CANCELLED'] == 1]
cancelled_all['DEP_DELAY_GROUP'].value_counts()


# ah so we are done. lets make our map. before we do that, lets find the min/max so that we know how far and below to go

# In[388]:


min_delay = df['DEP_DELAY_GROUP'].min()
max_delay = df['DEP_DELAY_GROUP'].max()

print("min", min_delay)
print("max", max_delay)


# In[389]:


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

df['DEP_DELAY_GROUP'] = df['DEP_DELAY_GROUP'].map(cancel_map)


# In[390]:


show_unique_missing_dtype(df, 'DEP_DELAY_GROUP')


# In[391]:


df = to_string(df, 'DEP_DELAY_GROUP')


# ## DEP_TIME_BLK

# In[392]:


show_unique_missing_dtype(df, 'DEP_TIME_BLK')


# so no missing values. i think it is menaingful, but smth nice to see is that 12am - 6am is a one block, rest are hourly blocks. this is a bit inconsistent with the rest of the values. but something even more noticeable is that its the same as `SCHEDULED_DEP_HOUR`. lets see it,

# In[393]:


show_unique_missing_dtype(df, 'SCHEDULED_DEP_HOUR')


# so we dont need to convert this column, we can just drop it. but we acknowledge that this column is much more meaningful in terms of readability like 0700-0759 is much better than just 7. but then the 0700-0759 is a string datatype and makes categorical data which isnt very good.

# In[394]:


df = df.drop('DEP_TIME_BLK', axis=1)


# ## TAXI_OUT

# In[395]:


show_unique_missing_dtype(df, 'TAXI_OUT')


# so -1 means cancelled flight. this is in minutes. lets handle missing values. are they cancelled flights?

# In[396]:


cancelled = check_if_cancelled(df, 'TAXI_OUT')
cancelled.isna().sum()


# so lets fill with -1, as all times are cancelled and did not occur

# In[397]:


cols_to_fill = ['TAXI_OUT', 'TAXI_IN', 'WHEELS_OFF', 'WHEELS_ON', 'ARR_TIME', 'ARR_DELAY_NEW', 'CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY']


# In[398]:


# Loop over each column and fill NaNs with 0 in the original df using cancelled_only's index
for col in cols_to_fill:
    missing_idx = cancelled[cancelled[col].isna()].index
    df.loc[missing_idx, col] = -1


# and lets fill with 0 for elapsed_times

# In[399]:


cols_to_fill = ['ACTUAL_ELAPSED_TIME', 'AIR_TIME']


# In[400]:


# Loop over each column and fill NaNs with 0 in the original df using cancelled_only's index
for col in cols_to_fill:
    missing_idx = cancelled[cancelled[col].isna()].index
    df.loc[missing_idx, col] = 0


# lets recheck

# In[401]:


show_unique_missing_dtype(df, 'TAXI_OUT')


# In[402]:


cancelled_all = df[df['CANCELLED'] == 1]
cancelled_all['TAXI_OUT'].value_counts()


# In[403]:


cancelled_all


# lets check if we can convert to integer

# In[404]:


df = convert_to_int(df, 'TAXI_OUT')


# In[405]:


show_unique_missing_dtype(df, 'TAXI_OUT')


# rename to something more menaingful like `ORIGIN_TAXI_TIME`

# In[406]:


df.rename(columns={'TAXI_OUT': 'ORIGIN_TAXI_TIME'}, inplace=True)


# ## WHEELS_OFF

# In[407]:


show_unique_missing_dtype(df, 'WHEELS_OFF')


# so no missing values, lets convert to int and rename to more menaingful

# In[408]:


df = convert_to_int(df, 'WHEELS_OFF')


# In[409]:


show_unique_missing_dtype(df, 'WHEELS_OFF')


# In[410]:


df.rename(columns={'WHEELS_OFF': 'DEP_TAKEOFF_TIME'}, inplace=True)


# ## WHEELS_ON

# In[411]:


show_unique_missing_dtype(df, 'WHEELS_ON')


# ok so lets deal with missing first. lets check if they are cancelled flights

# In[412]:


cancelled = check_if_cancelled(df, 'WHEELS_ON')


# In[413]:


cancelled = cancelled[cancelled['CANCELLED'] == 1]
cancelled.isna().sum()


# so this is new. first lets make the cancelled ones -1 to signify their time is not valid.

# In[414]:


cols_to_fill = ['WHEELS_ON', 'TAXI_IN', 'ARR_TIME', 'CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY']


# In[415]:


for col in cols_to_fill:
    missing_idx = cancelled.index
    df.loc[missing_idx, col] = -1


# In[416]:


cols_to_fill = ['ACTUAL_ELAPSED_TIME', 'AIR_TIME']


# In[417]:


for col in cols_to_fill:
    missing_idx = cancelled.index
    df.loc[missing_idx, col] = 0


# In[418]:


cancelled = check_if_cancelled(df, 'WHEELS_ON')
cancelled = cancelled[cancelled['CANCELLED'] == 1]
cancelled.isna().sum()


# now lets extract the remaining columns and just look at them first

# In[419]:


missing_rows = df[df['WHEELS_ON'].isna()]
missing_rows.isna().sum()


# In[420]:


missing_rows


# so it seems like these flights left the origin but did not reach the destination, nor were they cancelled. looks like they were possibly diverted. thus we fill them with -1 because they do not exist. 

# In[421]:


cols_to_fill = ['WHEELS_ON', 'TAXI_IN', 'ARR_TIME']


# In[422]:


for col in cols_to_fill:
    missing_idx = missing_rows.index
    df.loc[missing_idx, col] = -1


# In[423]:


cols_to_fill = ['ACTUAL_ELAPSED_TIME', 'AIR_TIME']


# In[424]:


for col in cols_to_fill:
    missing_idx = missing_rows.index
    df.loc[missing_idx, col] = 0


# recheck

# In[425]:


missing_rows = df[df['WHEELS_ON'].isna()]
missing_rows.shape


# convert to int

# In[426]:


df = convert_to_int(df, 'WHEELS_ON')


# In[427]:


show_unique_missing_dtype(df, 'WHEELS_ON')


# rename it to something meaningful like `ARR_LANDING_TIME`

# In[428]:


df.rename(columns={'WHEELS_ON': 'ARR_LANDING_TIME'}, inplace=True)


# ## TAXI_IN

# In[429]:


show_unique_missing_dtype(df, 'TAXI_IN')


# rename to something similar as `TAXI_IN` to `DEST_TAXI_TIME` and convert to int

# In[430]:


df = convert_to_int(df, 'TAXI_IN')


# In[431]:


df.rename(columns={'TAXI_IN': 'DEST_TAXI_TIME'}, inplace=True)


# ## CRS_ARR_TIME

# In[432]:


show_unique_missing_dtype(df, 'CRS_ARR_TIME')


# so same logic as `CRS_dEP_TIME`, lets extract its hour

# In[433]:


df = extract_hour(df, 'CRS_ARR_TIME', 'CRS_ARR_HOUR')


# In[434]:


show_unique_missing_dtype(df, 'CRS_ARR_HOUR')


# so again we see some 24 values. lets extract those and convert to 0

# In[435]:


# ensure the column is numeric
df['ARR_TIME_CLEAN'] = pd.to_numeric(df['CRS_ARR_TIME'], errors='coerce')

# filter rows with values = 2400
bad_times = df[df['ARR_TIME_CLEAN'] == 2400]
bad_times.shape


# In[436]:


# ensure numeric dtype
df['CRS_ARR_TIME'] = pd.to_numeric(df['CRS_ARR_TIME'], errors='coerce').astype('Int64')

# replace exactly 2400 → 0
df.loc[df['CRS_ARR_TIME'] == 2400, 'CRS_ARR_TIME'] = 0


# In[437]:


# RECHECK

# ensure the column is numeric
df['ARR_TIME_CLEAN'] = pd.to_numeric(df['CRS_ARR_TIME'], errors='coerce')

# filter rows with values = 2400
bad_times = df[df['ARR_TIME_CLEAN'] == 2400]
bad_times.shape


# In[438]:


# remove arr_time_clean

df = df.drop('ARR_TIME_CLEAN', axis=1)


# In[439]:


df = extract_hour(df, 'CRS_ARR_TIME', 'CRS_ARR_HOUR')


# In[440]:


show_unique_missing_dtype(df, 'CRS_ARR_HOUR')


# finally, lets rename the columns

# In[441]:


df.rename(columns={
    'CRS_ARR_TIME': 'SCHEDULED_ARR_TIME',
    'CRS_ARR_HOUR': 'SCHEDULED_ARR_HOUR'
}, inplace=True)


# ## ARR_TIME

# In[442]:


show_unique_missing_dtype(df, 'ARR_TIME')


# seems fine. lets convert to int and also extract hours

# In[443]:


df = convert_to_int(df, 'ARR_TIME')


# In[444]:


df = extract_hour(df, 'ARR_TIME', 'ARR_HOUR')


# In[445]:


show_unique_missing_dtype(df, 'ARR_HOUR')


# again we have 2400 values. lets repeat what we did in `CRS_ARR_TIME`

# In[446]:


# ensure the column is numeric
df['ARR_TIME_CLEAN'] = pd.to_numeric(df['ARR_TIME'], errors='coerce')

# filter rows with values = 2400
bad_times = df[df['ARR_TIME_CLEAN'] == 2400]
bad_times.shape


# In[447]:


# ensure numeric dtype
df['ARR_TIME'] = pd.to_numeric(df['ARR_TIME'], errors='coerce').astype('Int64')

# replace exactly 2400 → 0
df.loc[df['ARR_TIME'] == 2400, 'ARR_TIME'] = 0


# In[448]:


# RECHECK

# ensure the column is numeric
df['ARR_TIME_CLEAN'] = pd.to_numeric(df['ARR_TIME'], errors='coerce')

# filter rows with values = 2400
bad_times = df[df['ARR_TIME_CLEAN'] == 2400]
bad_times.shape


# In[449]:


# remove arr_time_clean

df = df.drop('ARR_TIME_CLEAN', axis=1)


# In[450]:


df = extract_hour(df, 'ARR_TIME', 'ARR_HOUR')


# In[451]:


show_unique_missing_dtype(df, 'ARR_HOUR')


# In[452]:


df.rename(columns={
    'ARR_TIME': 'ACTUAL_ARR_TIME',
    'ARR_HOUR': 'ACTUAL_ARR_HOUR'
}, inplace=True)


# ## ARR_DELAY

# In[453]:


show_unique_missing_dtype(df, 'ARR_DELAY')


# lets convert to int first and extract these 5000 rows to see if they are cancelled flights

# In[454]:


df = convert_to_int(df, 'ARR_DELAY')


# In[455]:


cancelled = check_if_cancelled(df, 'ARR_DELAY')


# so for the cancelled flights, lets make them 9999 as discussed for `dep_delay`

# In[456]:


cancelled = cancelled[cancelled['CANCELLED'] == 1]
cancelled.isna().sum()


# In[457]:


missing_idx = cancelled.index
df.loc[missing_idx, 'ARR_DELAY'] = 9999


# now lets move on to the non-cancelled flights

# In[458]:


missing_rows = df[df['ARR_DELAY'].isna()]
missing_rows.shape


# In[459]:


missing_rows.isna().sum()


# so the `ARR_TIME` is present. lets check its `value_counts()`

# In[460]:


missing_rows['ACTUAL_ARR_TIME'].value_counts()


# so lets use the formula `delay = actual - scheduled` and compute the delays

# In[461]:


mask = df[df['ARR_DELAY'].isna() & df['ACTUAL_ARR_TIME'].notna() & df['SCHEDULED_ARR_TIME'].notna()]
mask = mask[mask['ACTUAL_ARR_TIME'] != -1]
mask = mask[mask['SCHEDULED_ARR_TIME'] != -1]
mask.shape


# In[462]:


# Function to convert hhmm to total minutes since midnight
def hhmm_to_minutes(hhmm):
    hhmm = int(hhmm)
    hours = hhmm // 100
    minutes = hhmm % 100
    return hours * 60 + minutes


# In[463]:


df.loc[mask.index, 'ARR_DELAY'] = (
    mask['ACTUAL_ARR_TIME'].apply(hhmm_to_minutes) -
    mask['SCHEDULED_ARR_TIME'].apply(hhmm_to_minutes)
)


# now lets check whats left

# In[464]:


missing_rows = df[df['ARR_DELAY'].isna()]
missing_rows.isna().sum()


# In[465]:


missing_rows


# so remember these are those flights which are NOT cancelled but they didnt land either, so we assume they might be diverted. lets fill with 9999 as to show this plane did not land and its delay is infinite.

# In[466]:


missing_idx = missing_rows.index
df.loc[missing_idx, 'ARR_DELAY'] = 9999


# lets recheck

# In[467]:


show_unique_missing_dtype(df, 'ARR_DELAY')


# ## ARR_DELAY_NEW

# In[468]:


show_unique_missing_dtype(df, 'ARR_DELAY_NEW')


# again same reasoning as `dep_delay_new`, this column does not provide us new menaingful information as it is just repitition and can be achieved using a negative filter. better to drop. 

# In[469]:


df = df.drop('ARR_DELAY_NEW', axis=1)


# ## ARR_DEL15

# In[470]:


show_unique_missing_dtype(df, 'ARR_DEL15')


# so same implementation as `dep_del15`. lets first extract all the null values and check if they are cancelled flights

# In[471]:


cancelled = check_if_cancelled(df, 'ARR_DEL15')


# so for the cancelled flights, just fill with -1 (0 means within 15 mins, 1 means greater than 15mins, -1 means cancelled)

# In[472]:


cancelled = cancelled[cancelled['CANCELLED'] == 1]


# In[473]:


missing_idx = cancelled.index
df.loc[missing_idx, 'ARR_DEL15'] = -1


# now lets go back to the remaining

# In[474]:


missing_rows = df[df['ARR_DEL15'].isna()]
missing_rows.shape


# so lets see if their delay exists. if yes, lets fill according to their delay

# In[475]:


mask_equal_9999 = missing_rows[missing_rows['ARR_DELAY'] == 9999]
print(mask_equal_9999.shape)

missing_idx = mask_equal_9999.index
df.loc[missing_idx, 'ARR_DEL15'] = -1


# In[476]:


mask_less_15 = missing_rows[missing_rows['ARR_DELAY'] <= 15]
print(mask_less_15.shape)

missing_idx = mask_less_15.index
df.loc[missing_idx, 'ARR_DEL15'] = 0


# In[477]:


mask_more_15 = missing_rows[(missing_rows['ARR_DELAY'] > 15) & (missing_rows['ARR_DELAY'] < 9999)]
print(mask_more_15.shape)

missing_idx = mask_more_15.index
df.loc[missing_idx, 'ARR_DEL15'] = 1


# In[478]:


show_unique_missing_dtype(df, 'ARR_DEL15')


# now lets map it

# In[479]:


cancel_map = {
    0.0: 'Less than 15',
    1.0: 'Greater than 15',
    -1.0: 'Cancelled'
}

df['ARR_DEL15'] = df['ARR_DEL15'].map(cancel_map)


# In[480]:


show_unique_missing_dtype(df, 'ARR_DEL15')


# In[481]:


missing_rows = df[df['CANCELLED'] == 1]
missing_rows['ARR_DEL15'].value_counts()


# convert to string and rename column name

# In[482]:


df = to_string(df, 'ARR_DEL15')


# In[483]:


df.rename(columns={
    'ARR_DEL15': 'ARR_DELAY_15_MIN'
}, inplace=True)


# ## ARR_DELAY_GROUP

# In[484]:


show_unique_missing_dtype(df, 'ARR_DELAY_GROUP')


# so same as `dep_delay_group`, lets check if they are cancelled

# In[485]:


cancelled = check_if_cancelled(df, 'ARR_DELAY_GROUP')


# so for the cancelled flights lets map to 9999

# In[486]:


cancelled = cancelled[cancelled['CANCELLED'] == 1]
missing_idx = cancelled.index
df.loc[missing_idx, 'ARR_DELAY_GROUP'] = 9999


# now for the remaining

# In[487]:


missing_rows = df[df['ARR_DELAY_GROUP'].isna()]
missing_rows.shape


# In[488]:


missing_rows['ARR_DELAY'].value_counts()


# ok so lets map it. like lets extract all the rows which have a valid `arr_delay`

# In[489]:


# Create a list to store computed values
arr_delay_group = []

for i in range(len(df)):
    arr_delay = df.at[i, "ARR_DELAY"]
    
    if arr_delay == 9999:
        # Keep existing value or None
        value = df.at[i, "ARR_DELAY_GROUP"] if "ARR_DELAY_GROUP" in df.columns else 9999
    else:
        # Divide by 15 and round DOWN
        value = math.floor(arr_delay / 15)
    
    arr_delay_group.append(value)

# Assign back to the DataFrame
df["ARR_DELAY_GROUP"] = arr_delay_group


# In[490]:


missing_rows = df[df['ARR_DELAY_GROUP'].isna()]
missing_rows.shape


# now lets fill all remaining with 9999 as they have `arr_delay` as 9999

# In[491]:


missing_rows['ARR_DELAY'].value_counts()


# In[492]:


missing_idx = missing_rows.index
df.loc[missing_idx, 'ARR_DELAY_GROUP'] = 9999


# In[493]:


show_unique_missing_dtype(df, 'ARR_DELAY_GROUP')


# In[494]:


second_highest = df["ARR_DELAY"].dropna().unique()
second_highest = sorted(second_highest, reverse=True)[1]
second_highest


# check if all cancelled have 9999

# In[495]:


cancelled_all = df[df['CANCELLED'] == 1]
cancelled_all['ARR_DELAY_GROUP'].value_counts()


# ok now lets apply the same mapping as we did for `dep_delay_group`

# In[496]:


min_delay = df['ARR_DELAY'].min()
max_delay = df['ARR_DELAY'].max()

print("min", min_delay)
print("max", max_delay)


# In[497]:


def delay_group_label(group):
    if pd.isna(group):
        return None
    group = int(group)
    if group < 0:
        start = abs((group + 1) * 15)
        end = abs(group * 15)
        return f"{start}-{end} min early"
    else:
        start = group * 15
        end = (group + 1) * 15
        return f"{start}-{end} min late"

df["ARR_DELAY_GROUP"] = df["ARR_DELAY_GROUP"].apply(delay_group_label)


# In[498]:


show_unique_missing_dtype(df, 'ARR_DELAY_GROUP')


# In[499]:


cancelled = df[df['ARR_DELAY'] == 9999]
cancelled.shape


# In[500]:


missing_idx = cancelled.index
df.loc[missing_idx, 'ARR_DELAY_GROUP'] = "Cancelled"


# In[501]:


show_unique_missing_dtype(df, 'ARR_DELAY_GROUP')


# In[502]:


df = to_string(df, 'ARR_DELAY_GROUP')


# ## ARR_TIME_BLK

# In[503]:


show_unique_missing_dtype(df, 'ARR_TIME_BLK')


# so same reasoning as `dep_time_blk`, this is same to `scheduled_arr_time` so lets drop it

# In[504]:


df = df.drop('ARR_TIME_BLK', axis=1)


# ## CANCELLED

# In[505]:


show_unique_missing_dtype(df, 'CANCELLED')


# ok perfect so lets make a categorical column as it would look much better in BI

# In[506]:


# Mapping for a new column
mapping = {
    0: 'No', 
    1: 'Yes'
}

# Create a new column 
df['cancelled_c'] = df['CANCELLED'].map(mapping)
df = to_string(df, 'cancelled_c')


# In[507]:


# Get list of current columns
cols = list(df.columns)

# Move 'cancelled_c' to be right after 'CANCELLED'
day_index = cols.index('CANCELLED')
cols.insert(day_index + 1, cols.pop(cols.index('cancelled_c')))

# Reorder DataFrame
df = df[cols]


# In[508]:


show_unique_missing_dtype(df, 'cancelled_c')


# ## CANCELLATION_CODE

# In[509]:


show_unique_missing_dtype(df, 'CANCELLATION_CODE')


# so in our BI dashboard, a b c d e isnt very meaningful and readable. so here we see that this is not interpretable. we searched up and dug up the internet to get to know that from the U.S. Department of Transportation (DOT) flight data standards, here is what each cancellation code means:
# - A = Carrier — airline-related (crew, aircraft, etc.)
# - B = Weather — adverse weather at origin/destination or en route
# - C = NAS — National Airspace System (ATC, delays, airport congestion)
# - D = Security — e.g., TSA delays, threats, evacuations     
# 
# so instead of leaving it just like this, lets make it more visualizeable.
# 
# along with mapping each one, lets replace all null values with "Not Cancelled"

# lets see if there are any aircraft reasons

# In[510]:


aircraft_delays = df[df['LATE_AIRCRAFT_DELAY'].notna()]
aircraft_delays['CANCELLATION_CODE'].value_counts()


# ah so theres no specific cancelling reason for late aircraft, it is only a reason for delay. lets do the mapping now.

# In[511]:


cancel_map = {
    'A': 'Carrier',
    'B': 'Weather',
    'C': 'Airspace System (NAS)',
    'D': 'Security',
    'Not Cancelled': 'Not Cancelled'
}

df['CANCELLATION_CODE'] = df['CANCELLATION_CODE'].fillna('Not Cancelled').map(cancel_map)
df = to_string(df, 'CANCELLATION_CODE')


# In[512]:


show_unique_missing_dtype(df, 'CANCELLATION_CODE')


# In[513]:


df.rename(columns={'CANCELLATION_CODE': 'CANCELLATION_REASON'}, inplace=True)


# ## CRS_ELAPSED_TIME

# In[514]:


show_unique_missing_dtype(df, 'CRS_ELAPSED_TIME')


# ah 2 columns empty. lets extract those and look at them

# In[515]:


missing_rows = df[df['CRS_ELAPSED_TIME'].isna()]
missing_rows


# so lets just compute the elapsed_time using `elapsed = arr - dep`

# In[516]:


mask = df[df['CRS_ELAPSED_TIME'].isna() & df['SCHEDULED_ARR_TIME'].notna() & df['SCHEDULED_DEP_TIME'].notna()]
mask.shape


# In[517]:


scheduled_elapsed = (
    mask['SCHEDULED_ARR_TIME'].apply(hhmm_to_minutes) -
    mask['SCHEDULED_DEP_TIME'].apply(hhmm_to_minutes)
)

scheduled_elapsed = scheduled_elapsed.apply(lambda x: x + 1440 if x < 0 else x)

df.loc[mask.index, 'CRS_ELAPSED_TIME'] = scheduled_elapsed


# In[518]:


show_unique_missing_dtype(df, 'CRS_ELAPSED_TIME')


# yup lets convert to int and rename

# In[519]:


df = convert_to_int(df, 'CRS_ELAPSED_TIME')


# In[520]:


df.rename(columns={'CRS_ELAPSED_TIME': 'SCHEDULED_ELAPSED_TIME'}, inplace=True)


# ## ACTUAL_ELAPSED_TIME

# In[521]:


show_unique_missing_dtype(df, 'ACTUAL_ELAPSED_TIME')


# using the same formula as before, `elapsed = arr - dep`

# In[522]:


mask = df[df['ACTUAL_ELAPSED_TIME'].isna() & df['ACTUAL_ARR_TIME'].notna() & df['ACTUAL_DEP_TIME'].notna()]
mask.shape


# In[523]:


def safe_hhmm_to_minutes(hhmm):
    try:
        hhmm = int(hhmm)
        return (hhmm // 100) * 60 + (hhmm % 100)
    except:
        return None


# In[524]:


elapsed_minutes = (
    mask['ACTUAL_ARR_TIME'].apply(safe_hhmm_to_minutes) -
    mask['ACTUAL_DEP_TIME'].apply(safe_hhmm_to_minutes)
)

# Adjust for overnight flights
elapsed_minutes = elapsed_minutes.apply(lambda x: x + 1440 if x < 0 else x)

df.loc[mask.index, 'ACTUAL_ELAPSED_TIME'] = elapsed_minutes


# In[525]:


show_unique_missing_dtype(df, 'ACTUAL_ELAPSED_TIME')


# convert to int

# In[526]:


df = convert_to_int(df, 'ACTUAL_ELAPSED_TIME')


# ## AIR_TIME

# In[527]:


show_unique_missing_dtype(df, 'AIR_TIME')


# now we can again apply formula `air_time = wheels_dest - wheels_origin`

# In[528]:


mask = df[df['AIR_TIME'].isna() & df['ARR_LANDING_TIME'].notna() & df['DEP_TAKEOFF_TIME'].notna()]
mask.shape


# In[529]:


air_minutes = (
    mask['ARR_LANDING_TIME'].apply(safe_hhmm_to_minutes) -
    mask['DEP_TAKEOFF_TIME'].apply(safe_hhmm_to_minutes)
)

air_minutes = air_minutes.apply(lambda x: x + 1440 if x < 0 else x)

df.loc[mask.index, 'AIR_TIME'] = air_minutes


# In[530]:


show_unique_missing_dtype(df, 'AIR_TIME')


# convert to int and rename as `IN_AIR_DURATION`

# In[531]:


df = convert_to_int(df, 'AIR_TIME')


# In[532]:


df.rename(columns={'AIR_TIME': 'IN_AIR_DURATION'}, inplace=True)


# ## DISTANCE

# In[533]:


show_unique_missing_dtype(df, 'DISTANCE')


# fine, no change needed. no missing. datatype is fine.

# ## DISTANCE_GROUP

# In[534]:


show_unique_missing_dtype(df, 'DISTANCE_GROUP')


# so not meaningful. lets map. it is - Distance Between Departure and Arrival Airports in Number of 250-Mile increments Rounded Down (e.g. 400 miles is a value of 1).

# In[535]:


df['DISTANCE_GROUP'].max()


# In[536]:


map = {
    0: '0-250 miles',
    1: '250-500 miles',
    2: '500-750 miles',
    3: '750-1000 miles',
    4: '1000-1250 miles',
    5: '1250-1500 miles',
    6: '1500-1750 miles',
    7: '1750-2000 miles',
    8: '2000-2250 miles',
    9: '2250-2500 miles',
    10: '2500-2750 miles',
    11: '2750-3000 miles'
}

df['DISTANCE_GROUP'] = df['DISTANCE_GROUP'].map(map)
df = to_string(df, 'DISTANCE_GROUP')


# In[537]:


show_unique_missing_dtype(df, 'DISTANCE_GROUP')


# ## CARRIER_DELAY

# In[538]:


show_unique_missing_dtype(df, 'CARRIER_DELAY')


# so this column is Carrier Delay (in Minutes). if it is null, then that probably means there was no `CARRIER_DELAY`. so we can just fill with 0. so first lets fill all cancelled with -1 and filled with 0. 

# In[539]:


def fill_delays(df, col):
    # fill all cancelled with -1
    cancelled = df[df['CANCELLED'] == 1] 
    print(cancelled[col].value_counts())
    print("\nmissing", cancelled[col].isna().sum(), "\n")
    missing_idx = cancelled.index
    df.loc[missing_idx, col] = -1
    
    # fill rest missing with 0
    missing_rows = df[df[col].isna()]
    missing_idx = missing_rows.index
    df.loc[missing_idx, col] = 0
    
    return df


# In[540]:


df = fill_delays(df, 'CARRIER_DELAY')
show_unique_missing_dtype(df, 'CARRIER_DELAY')


# convert to int

# In[541]:


df = convert_to_int(df, 'CARRIER_DELAY')


# In[542]:


show_unique_missing_dtype(df, 'CARRIER_DELAY')


# ## WEATHER_DELAY

# In[543]:


show_unique_missing_dtype(df, 'WEATHER_DELAY')


# so same as `CARRIER_DELAY`

# In[544]:


df = fill_delays(df, 'WEATHER_DELAY')
show_unique_missing_dtype(df, 'WEATHER_DELAY')


# In[545]:


df = convert_to_int(df, 'WEATHER_DELAY')
show_unique_missing_dtype(df, 'WEATHER_DELAY')


# ## NAS_DELAY

# In[546]:


show_unique_missing_dtype(df, 'NAS_DELAY')


# In[547]:


df = fill_delays(df, 'NAS_DELAY')
show_unique_missing_dtype(df, 'NAS_DELAY')


# In[548]:


df = convert_to_int(df, 'NAS_DELAY')
show_unique_missing_dtype(df, 'NAS_DELAY')


# ## SECURITY_DELAY

# In[549]:


show_unique_missing_dtype(df, 'SECURITY_DELAY')


# In[550]:


df = fill_delays(df, 'SECURITY_DELAY')
show_unique_missing_dtype(df, 'SECURITY_DELAY')


# In[551]:


df = convert_to_int(df, 'SECURITY_DELAY')
show_unique_missing_dtype(df, 'SECURITY_DELAY')


# ## LATE_AIRCRAFT_DELAY

# In[552]:


show_unique_missing_dtype(df, 'LATE_AIRCRAFT_DELAY')


# In[553]:


df = fill_delays(df, 'LATE_AIRCRAFT_DELAY')
show_unique_missing_dtype(df, 'LATE_AIRCRAFT_DELAY')


# In[554]:


df = convert_to_int(df, 'LATE_AIRCRAFT_DELAY')
show_unique_missing_dtype(df, 'LATE_AIRCRAFT_DELAY')


# # Recheck
# a simple recheck of all data statistics to see if the data is fine before donwloading

# In[555]:


df.shape


# In[556]:


# Check for missing values
df.isnull().sum()


# In[557]:


# Display data types
df.dtypes


# In[558]:


df


# # Download cleaned dataset

# In[559]:


# Save the cleaned DataFrame to a CSV file
df.to_csv('../data/flights_jantojun2020_3M_cleaned.csv', index=False)


# In[560]:


# Extract first 1000 rows
df_1000 = df.head(1000)

# Save to CSV with column headers
df_1000.to_csv('../data/flights_jantojun2020_1K_cleaned.csv', index=False)


# In[561]:


# revert pandas settings back to normal
# pd.reset_option('display.max_columns')


# # Last run

# In[562]:


get_current_datetime()


# In[563]:


# Capture end time
end_time = datetime.now()

# Compute time difference
diff = end_time - start_time

# Total seconds (float)
total_seconds = diff.total_seconds()

# Decompose
hours, rem = divmod(total_seconds, 3600)
minutes, rem = divmod(rem, 60)
seconds = int(rem)
milliseconds = diff.microseconds // 1000

# Display
print(f"Start time : {start_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
print(f"End time   : {end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
print(f"Duration   : {int(hours)}h {int(minutes)}m {seconds}s {milliseconds}ms")

