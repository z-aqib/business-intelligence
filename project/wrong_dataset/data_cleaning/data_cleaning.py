#!/usr/bin/env python
# coding: utf-8

# Business Intelligence Project    
# Name: Zehra Ahmed, Farah Inayat, Kisa Fatima, Zuha Aqib    
# Date: 18-May-2025

# In[736]:


# print when the last code was run
from datetime import datetime
datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# # Imports

# In[737]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime, timedelta


# ### Some Functions
# some preliminary functions we can use in the code

# In[738]:


# Function to get current date and time as a string
def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# # Data Loading

# In[739]:


# Load the dataset
df = pd.read_csv('../data/flights_sample_3m.csv')

pd.set_option('display.max_columns', None)


# In[740]:


df


# In[741]:


df.shape


# # Data Preparation

# ## Data Statistics

# In[742]:


# Check for missing values
print("Missing values per column:")
df.isnull().sum()


# In[743]:


# Display data types
print("\nData types:")
df.dtypes


# In[744]:


# Get summary statistics
print("\nSummary statistics:")
df.describe(include='all')


# ## Changing Data Type

# ### Defined Functions
# here are some functions we can use for changing the datatype

# In[745]:


def to_string(df, column_name):
    """
    Convert a pandas DataFrame column to a string.
    """
    df[column_name] = df[column_name].astype('string')
    print(f"Column Name: '{column_name}', Type: {df[column_name].dtype}")
    return df  


# In[746]:


def to_date(df, column_name, format=None):
    """
    Convert a pandas DataFrame column to datetime.
    """
    df[column_name] = pd.to_datetime(df[column_name], format=format)
    print(f"Column Name: '{column_name}', Type: {df[column_name].dtype}")
    return df


# In[747]:


def to_int(df, column_name):
    """
    Convert a pandas DataFrame column to a int.
    """
    df[column_name] = df[column_name].astype('int64')
    print(f"Column Name: '{column_name}', Type: {df[column_name].dtype}")
    return df  


# In[748]:


def to_float(df, column_name):
    """
    Convert a pandas DataFrame column to a float.
    """
    df[column_name] = df[column_name].astype('float64')
    print(f"Column Name: '{column_name}', Type: {df[column_name].dtype}")
    return df  


# ### Implementation
# so there is a date column lets make it a type date column, and there is a few columns which are object datatype, lets change to string for better readability

# In[749]:


df = to_date(df, 'FL_DATE', '%Y-%m-%d')


# In[750]:


df = to_string(df, 'AIRLINE')
df = to_string(df, 'AIRLINE_DOT')
df = to_string(df, 'AIRLINE_CODE')
df = to_string(df, 'ORIGIN')
df = to_string(df, 'ORIGIN_CITY')
df = to_string(df, 'DEST')
df = to_string(df, 'DEST_CITY')
df = to_string(df, 'CANCELLATION_CODE')


# ## Fixing columns saath saath
# so for each column we're just gonna check is it coherenet? are there any errors like mistypes? this is for only those columns which are text and have some textual information and their unique values are small and checkable

# ### AIRLINE
# here lets extract its 18 unique values and check it

# In[751]:


# Just checking unique airline names
print(df['AIRLINE'].value_counts())


# so there is no typo. lets move ahead to the next one
# 
# ### AIRLINE DOT

# In[752]:


print(df['AIRLINE_DOT'].value_counts())


# nothing again
# 
# ### AIRLINE CODE

# In[753]:


print(df['AIRLINE_CODE'].value_counts())


# nothing again but the column `AIRLINE_DOT` is very similar to the columns we already have - its just a concatentation of `AIRLINES` AND `AIRLINE_CODE`. So lets drop it.

# In[754]:


df = df.drop('AIRLINE_DOT', axis=1)


# In[755]:


df


# ### DOT_CODE
# now lets explore dot_code to see what its values are like

# In[756]:


df['DOT_CODE'].value_counts()


# okay so its our intutiton that its related to the airline. according to the html dictionary - IT IS. so we can use that to our advantage - any cell that is empty, we can just find the related airline and extract its airline code and fill with that value. so we will do this in the MISSING VALUES section. lets see if we have any missing values:

# In[757]:


df['DOT_CODE'].isnull().sum()


# ok so we don't have missing values. thats clear.

# # Missing Values
# here we handle missing values for each column. 

# In[758]:


df.shape


# In[759]:


df.isnull().sum()


# ## DEP_TIME

# In[760]:


df['DEP_TIME'].isnull().sum()


# In[761]:


df['DEP_TIME'].value_counts()


# so we see that all the missing values are either 77615 or more. we have an intuition that maybe those rows are those rows that have ALL the missing values. so we get all the missing values which are 77615 >= and extract their rows and see how many are extracted. if they are 77615, that means all those rows have majority columns empty - they have the important columns empty

# In[762]:


null_rows = df[
    df['DEP_TIME'].isnull() & 
    df['DEP_DELAY'].isnull() & 
    df['TAXI_OUT'].isnull() & 
    df['WHEELS_OFF'].isnull() & 
    df['WHEELS_ON'].isnull() & 
    df['TAXI_IN'].isnull() & 
    df['ARR_TIME'].isnull() & 
    df['ARR_DELAY'].isnull() & 
    df['ELAPSED_TIME'].isnull() &
    df['AIR_TIME'].isnull() &
    df['DELAY_DUE_CARRIER'].isnull() &
    df['DELAY_DUE_WEATHER'].isnull() &
    df['DELAY_DUE_NAS'].isnull() &
    df['DELAY_DUE_SECURITY'].isnull() &
    df['DELAY_DUE_LATE_AIRCRAFT'].isnull()
]

null_rows


# so we see here that those 77615 rows have majority columns empty, so lets check if all of them were cancelled or diverted.

# In[763]:


df[df['DEP_TIME'].isna()][['CANCELLED', 'DIVERTED']].value_counts()


# so all of them were cancelled! this gives alot of information. lets fill everything with 0, as all those times were 0.

# In[764]:


null_rows.isna().sum()


# so all of them are 77615 empty meaning all are empty. but 13 rows dont have `crs_elapsed_time` which can be computed using `crs_arr_time` - `crs_dep_time`. we will handle this later. lets handle the rest. 
# ### DEP_TIME, DEP_DELAY, TAXI_OUT, WHEELS_OFF, WHEELS_ON, TAXI_IN, ARR_TIME, ARR_DELAY, ELAPSED_TIME, AIR_TIME, DELAY_DUE_WEATHER, DELAY_DUE_NAS, DELAY_DUE_SECURITY, DELAY_DUE_LATE_AIRCRAFT

# In[765]:


cols_to_fill = ['DEP_TIME', 'DEP_DELAY', 'TAXI_OUT', 'WHEELS_OFF', 'WHEELS_ON', 'TAXI_IN', 'ARR_TIME', 'ARR_DELAY', 'ELAPSED_TIME', 'AIR_TIME', 'DELAY_DUE_WEATHER', 'DELAY_DUE_NAS', 'DELAY_DUE_SECURITY', 'DELAY_DUE_LATE_AIRCRAFT']


# In[766]:


# Loop over each column and fill NaNs with 0 in the original df using cancelled_only's index
for col in cols_to_fill:
    missing_idx = null_rows[null_rows[col].isna()].index
    df.loc[missing_idx, col] = 0


# In[767]:


df['DEP_TIME'].isna().sum()


# ## DEP_DELAY

# okay so we see that CRS_DEP_TIME and DEP_TIME is 0 null values that means we can compute DEP_DELAY null values using DEP_TIME - CRS_DEP_TIME to find the delay. however as both are in hhmm we will need to convert to minutes first 

# In[768]:


df['DEP_DELAY'].isna().sum()


# so we have 29 rows that are empty. lets first extract those 29 rows to work on

# In[769]:


# Only fill DEP_DELAY where both times are present
mask = df[df['DEP_DELAY'].isna() & df['DEP_TIME'].notna() & df['CRS_DEP_TIME'].notna()]
mask


# In[770]:


mask.shape


# ok so we have extracted those rows. lets now apply the formula 

# In[771]:


# Function to convert hhmm to total minutes since midnight
def hhmm_to_minutes(hhmm):
    hhmm = int(hhmm)
    hours = hhmm // 100
    minutes = hhmm % 100
    return hours * 60 + minutes


# In[772]:


# Apply the conversion and calculate DEP_DELAY for masked rows
df.loc[mask.index, 'DEP_DELAY'] = (
    mask['DEP_TIME'].apply(hhmm_to_minutes) -
    mask['CRS_DEP_TIME'].apply(hhmm_to_minutes)
)

df['DEP_DELAY'].isna().sum()


# In[773]:


df['DEP_DELAY'].value_counts()


# ## TAXI_OUT
# so `taxi_out` is the time from gate pushback to takeoff.
# so here lets first see how many rows are empty

# In[774]:


df['TAXI_OUT'].isnull().sum()


# so now 1191 is not a very large value out of 3 million. we have one option to drop those rows. but lets think of something better - lets check those `taxi_out` rows, are they all cancelled or diverted flights - then `taxi_out` will be null. lets extract the cancelled and diverted status of those rows.

# In[775]:


df[df['TAXI_OUT'].isna()][['CANCELLED', 'DIVERTED']].value_counts()


# so we see that in all those 1191 rows, those flights are CANCELLED. thus the plane has never left the origin - thus there is no `taxi_out`. respectively, there won't be any `wheels_off`, `wheels_on`, `arr_time`, `taxi_in`, `air_time`, `elapsed_time` either. so first lets extract those `taxi_out` rows, and then lets extract ALL the cancelled rows and see what is `taxi_out` is filled? lets fill that with it exactly to maintain consistency.

# In[776]:


# Extract rows with CANCELLED = 1 and DIVERTED = 0
cancelled_only = df[(df['CANCELLED'] == 1) & (df['DIVERTED'] == 0)]
cancelled_only.shape


# In[777]:


cancelled_only['TAXI_OUT'].isna().sum()


# In[778]:


cancelled_only['TAXI_OUT'].notna().sum()


# so there does exist 77949 rows that have `taxi_out` values, lets check their values

# In[779]:


cancelled_only['TAXI_OUT'].value_counts()


# so this is weird. even if the flight is cancelled, there is a taxi_out. this might mean the flight was ready to take off, but was cancelled before the wheels started moving. lets see if we have a `wheels_off` for these cancelled rows

# In[780]:


cancelled_only['WHEELS_OFF'].isna().sum()


# In[781]:


cancelled_only['WHEELS_OFF'].value_counts()


# look how the majority values of CANCLEDD FLIGHTS have 0. this means that we fill cancelled flights with 0      
# okay so this is great - our suspicions have been confirmed. the plane had taken off, but was cancelled before reaching the destination, maybe due to bad weather or a technical fault. lets extract those cancelled reasons too

# In[782]:


cancelled_only['CANCELLATION_CODE'].value_counts()


# ah so majority was due to weather. so lets fill with some value to show that there is no value. lets say 0. but before we do that, lets extract all the null values in these cancelled rows and get their counts so that we can fill with 0

# In[783]:


cancelled_nulls = cancelled_only[cancelled_only['TAXI_OUT'].isna()]
cancelled_nulls.isna().sum()


# now lets fill all the empty cells with 0
# ### TAXI_OUT, WHEELS_OFF, WHEELS_ON, TAXI_IN, ARR_TIME, ARR_DELAY, ELAPSED_TIME, AIR_TIME, DELAY_DUE_CARRIER, DELAY_DUE_WEATHER, DELAY_DUE_NAS, DELAY_DUE_SECURITY, DELAY_DUE_LATE_AIRCRAFT

# In[784]:


cols_to_fill = ['TAXI_OUT', 'WHEELS_OFF', 'WHEELS_ON', 'TAXI_IN', 'ARR_TIME', 'ARR_DELAY', 'ELAPSED_TIME', 'AIR_TIME', 'DELAY_DUE_CARRIER', 'DELAY_DUE_WEATHER', 'DELAY_DUE_NAS', 'DELAY_DUE_SECURITY', 'DELAY_DUE_LATE_AIRCRAFT']


# In[785]:


# Loop over each column and fill NaNs with 0 in the original df using cancelled_nulls's index
for col in cols_to_fill:
    missing_idx = cancelled_nulls[cancelled_nulls[col].isna()].index
    df.loc[missing_idx, col] = 0


# In[786]:


df['TAXI_OUT'].isna().sum()


# ## WHEELS_OFF
# none are empty

# In[787]:


df['WHEELS_OFF'].isna().sum()


# ## WHEELS_ON

# In[788]:


df['WHEELS_ON'].isna().sum()


# so we found some null values. lets see the status of all these null values

# In[789]:


df[df['WHEELS_ON'].isna()][['CANCELLED', 'DIVERTED']].value_counts()


# so 802 flights are diverted menaing that did not land at the intended destination. It was rerouted in the air due to weather, technical issues, airport congestion, etc. 2 flights were neither cancelled nor diverted so we will deal with these first.

# In[790]:


rows_null = df[df['WHEELS_ON'].isna()]
data_missing_rows = rows_null[(rows_null['DIVERTED'] == 0.0) & (rows_null['CANCELLED'] == 0.0)]
data_missing_rows


# so these 2 rows, they did take off, they were not diverted, and were not cancelled - yet we dont have any data of them landing, no `wheels_on`, `taxi_in`, `arr_time`. thus this is a data missing entry and we cannot deal with it. it is better to drop. 

# In[791]:


df = df.drop(index=data_missing_rows.index)


# so lets extract those 802 flights first and fill all their null values with 0 like we did for all the cancelled flights. we will also do this for the cancelled flights

# In[792]:


rows_null.shape


# In[793]:


rows_null


# first lets do it for the diverted flights

# In[794]:


# Extract rows with CANCELLED = 0 and DIVERTED = 1
diverted_only = rows_null[(rows_null['CANCELLED'] == 0) & (rows_null['DIVERTED'] == 1)]
diverted_only.shape


# In[795]:


diverted_only.isna().sum()


# so we spotted something new: `arr_time` does have 2 entries which the others do not have. lets work on those and extract those rows and fill them accordingly.

# In[796]:


arr_time_full = diverted_only[diverted_only['ARR_TIME'].notna()]
arr_time_full


# In[797]:


arr_time_full.isna().sum()


# now for this specific case we can't fill all the rows with 0, there does exist `arr_time` so thus `elapsed_time` can be computed, `air_time` cannot as we dont have `wheels_on`. so lets just make `wheels_on`, `taxi_in`, `air_time` with 0s, the rest can be filled later on.

# In[798]:


cols_to_fill = ['WHEELS_ON', 'TAXI_IN', 'AIR_TIME']
for col in cols_to_fill:
    missing_idx = arr_time_full[arr_time_full[col].isna()].index
    df.loc[missing_idx, col] = 0


# now lets remove these two columns from `diverted_only` dataframe

# In[799]:


diverted_only = diverted_only[diverted_only['ARR_TIME'].isna()]
diverted_only.isna().sum()


# so lets fill all the empty values with 0
# ### WHEELS_ON, TAXI_IN, ARR_TIME, ARR_DELAY, CANCELLATION_CODE, ELAPSED_TIME, AIR_TIME, DELAY_DUE_CARRIER, DELAY_DUE_WEATHER, DELAY_DUE_NAS, DELAY_DUE_SECURITY, DELAY_DUE_LATE_AIRCRAFT

# In[800]:


cols_to_fill = ['WHEELS_ON', 'TAXI_IN', 'ARR_TIME', 'ARR_DELAY', 'ELAPSED_TIME', 'AIR_TIME', 'DELAY_DUE_CARRIER', 'DELAY_DUE_WEATHER', 'DELAY_DUE_NAS', 'DELAY_DUE_SECURITY', 'DELAY_DUE_LATE_AIRCRAFT']


# In[801]:


# Loop over each column and fill NaNs with 0 in the original df using diverted_only's index
for col in cols_to_fill:
    missing_idx = diverted_only[diverted_only[col].isna()].index
    df.loc[missing_idx, col] = 0


# In[802]:


df['WHEELS_ON'].isna().sum()


# now lets do it for the cancelled flights

# In[803]:


# Extract rows with CANCELLED = 0 and DIVERTED = 1
cancelled_only = rows_null[(rows_null['CANCELLED'] == 1) & (rows_null['DIVERTED'] == 0)]
cancelled_only.shape


# In[804]:


cancelled_only.isna().sum()


# ### WHEELS_ON, TAXI_IN, ARR_TIME, ARR_DELAY, ELAPSED_TIME, AIR_TIME, DELAY_DUE_CARRIER, DELAY_DUE_WEATHER, DELAY_DUE_NAS, DELAY_DUE_SECURITY, DELAY_DUE_LATE_AIRCRAFT

# In[805]:


cols_to_fill = ['WHEELS_ON', 'TAXI_IN', 'ARR_TIME', 'ARR_DELAY', 'ELAPSED_TIME', 'AIR_TIME', 'DELAY_DUE_CARRIER', 'DELAY_DUE_WEATHER', 'DELAY_DUE_NAS', 'DELAY_DUE_SECURITY', 'DELAY_DUE_LATE_AIRCRAFT']


# In[806]:


# Loop over each column and fill NaNs with 0 in the original df using cancelled_only's index
for col in cols_to_fill:
    missing_idx = cancelled_only[cancelled_only[col].isna()].index
    df.loc[missing_idx, col] = 0


# In[807]:


df['WHEELS_ON'].isna().sum()


# ## TAXI_IN
# none are empty

# In[808]:


df['TAXI_IN'].isna().sum()


# ## ARR_TIME
# none are empty

# In[809]:


df['ARR_TIME'].isna().sum()


# ## ARR_DELAY
# so as we discussed about `dep_delay` we said that it was the difference between the scheduled departure time and actual departure time. here it is the same thing - `arr_delay` is the difference between the scheduled arrival time and the actual arrival time. lets now do the same implementation we did for `dep_delay`.

# In[810]:


df['ARR_DELAY'].isnull().sum()


# In[811]:


mask = df[df['ARR_DELAY'].isna() & df['ARR_TIME'].notna() & df['CRS_ARR_TIME'].notna()]
mask.shape


# In[812]:


df.loc[mask.index, 'ARR_DELAY'] = (
    mask['ARR_TIME'].apply(hhmm_to_minutes) -
    mask['CRS_ARR_TIME'].apply(hhmm_to_minutes)
)


# In[813]:


df['ARR_DELAY'].isnull().sum()


# ## CANCELLATION_CODE
# so we can see that the cancellation_code empty values are BECAUSE THAT FLIGHT WAS NOT CANCELLED. AS IT IS A STRING type we can just fill with a string of "not cancelled"

# In[814]:


df['CANCELLATION_CODE'].isna().sum()


# In[815]:


df['CANCELLATION_CODE'].notna().sum()


# In[816]:


df['CANCELLATION_CODE'].value_counts()


# so here we see that this is not interpretable. we searched up and dug up the internet to get to know that from the U.S. Department of Transportation (DOT) flight data standards, here is what each cancellation code means:
# - A = Carrier — airline-related (crew, aircraft, etc.)
# - B = Weather — adverse weather at origin/destination or en route
# - C = NAS — National Airspace System (ATC, delays, airport congestion)
# - D = Security — e.g., TSA delays, threats, evacuations     
# 
# so instead of leaving it just like this, lets make it more visualizeable.
# 
# along with mapping each one, lets replace all null values with "Not Cancelled"

# In[817]:


cancel_map = {
    'A': 'Carrier',
    'B': 'Weather',
    'C': 'Airspace System (NAS)',
    'D': 'Security',
    'Not Cancelled': 'Not Cancelled'
}

df['CANCELLATION_CODE'] = df['CANCELLATION_CODE'].fillna('Not Cancelled').map(cancel_map)
df = to_string(df, 'CANCELLATION_CODE')


# In[818]:


df['CANCELLATION_CODE'].value_counts()


# In[819]:


df['CANCELLATION_CODE'].isna().sum()


# ## CRS_ELAPSED_TIME
# so we know we can compute this as the difference between the `CRS_DEP_TIME` and the `CRS_ARR_TIME`. same as `DEP_DELAY` we first compute the hhmm accordingly and then compute differnece

# In[820]:


df['CRS_ELAPSED_TIME'].isnull().sum()


# In[821]:


mask = df[df['CRS_ELAPSED_TIME'].isna() & df['CRS_ARR_TIME'].notna() & df['CRS_DEP_TIME'].notna()]
mask.shape


# yep so we have extracted all the relevant rows. lets apply it on them.

# In[822]:


scheduled_elapsed = (
    mask['CRS_ARR_TIME'].apply(hhmm_to_minutes) -
    mask['CRS_DEP_TIME'].apply(hhmm_to_minutes)
)

scheduled_elapsed = scheduled_elapsed.apply(lambda x: x + 1440 if x < 0 else x)

df.loc[mask.index, 'CRS_ELAPSED_TIME'] = scheduled_elapsed


# In[823]:


df['CRS_ELAPSED_TIME'].isnull().sum()


# ## ELAPSED_TIME
# as discussed in dep_delay, elapsed_time is the time of the flight. its the actual elapsed time so same as `crs_elapsed_time`, its just `arr_time` - `dep_time`. so lets do the same thing as above.

# In[824]:


df['ELAPSED_TIME'].isnull().sum()


# In[825]:


mask = df[df['ELAPSED_TIME'].isna() & df['ARR_TIME'].notna() & df['DEP_TIME'].notna()]
mask.shape


# In[826]:


def safe_hhmm_to_minutes(hhmm):
    try:
        hhmm = int(hhmm)
        return (hhmm // 100) * 60 + (hhmm % 100)
    except:
        return None


# In[827]:


elapsed_minutes = (
    mask['ARR_TIME'].apply(safe_hhmm_to_minutes) -
    mask['DEP_TIME'].apply(safe_hhmm_to_minutes)
)

# Adjust for overnight flights
elapsed_minutes = elapsed_minutes.apply(lambda x: x + 1440 if x < 0 else x)

df.loc[mask.index, 'ELAPSED_TIME'] = elapsed_minutes


# In[828]:


df['ELAPSED_TIME'].isnull().sum()


# ## AIR_TIME
# so now this is same as `crs_elapsed_time` and `elapsed_time`. `air_time` is just `wheels_on` and `wheels_off` difference. so lets do the same implementation

# In[829]:


df['AIR_TIME'].isnull().sum()


# In[830]:


mask = df[df['AIR_TIME'].isna() & df['WHEELS_ON'].notna() & df['WHEELS_OFF'].notna()]
mask.shape


# In[831]:


air_minutes = (
    mask['WHEELS_ON'].apply(safe_hhmm_to_minutes) -
    mask['WHEELS_OFF'].apply(safe_hhmm_to_minutes)
)

air_minutes = air_minutes.apply(lambda x: x + 1440 if x < 0 else x)

df.loc[mask.index, 'AIR_TIME'] = air_minutes


# In[832]:


df['AIR_TIME'].isnull().sum()


# ## DELAY_DUE_CARRIER, DELAY_DUE_WEATHER, DELAY_DUE_NAS, DELAY_DUE_SECURITY, DELAY_DUE_LATE_AIRCRAFT
# now every column here has one thing in common: same missing values. this also means that whenever there was NOT A DELAY, then they were left blank. so it is better to fill them with 0s to show that there was NO DELAY. if i fill them with -1, it will hinder the mean/median/average, and saying -1minutes of delay does not make sense, wheras 0 minutes of delay does.

# In[833]:


df['DELAY_DUE_CARRIER'].isnull().sum()


# In[834]:


df['DELAY_DUE_CARRIER'].value_counts()


# so we see from the value_counts that the majority is 0s which means there is no delay of this cause. so we will fill all NANs wth 0s

# In[835]:


delay_columns = ['DELAY_DUE_CARRIER', 'DELAY_DUE_WEATHER', 'DELAY_DUE_NAS', 'DELAY_DUE_SECURITY', 'DELAY_DUE_LATE_AIRCRAFT']
for col in delay_columns:
    df[col] = df[col].fillna(0.0)
    
df['DELAY_DUE_CARRIER'].isnull().sum()


# ## New columns
# here we analyse if we need new columns in integers or not for example of destination city etc so that we can see common ones

# ### FL_DATE
# here we add 4 new columns for year, quarter, month, day to make visualisation easier

# In[836]:


# for FL_DATE, add 4 new columns which have the year, quarter, month, date for better preprocessing and display
df['year'] = df['FL_DATE'].dt.year
df['quarter'] = df['FL_DATE'].dt.quarter
df['month'] = df['FL_DATE'].dt.strftime('%b')  # 3-letter month name
df = to_string(df, 'month')
df['day'] = df['FL_DATE'].dt.day

df


# In[837]:


# Move the new columns after FL_DATE
# Get all column names
cols = list(df.columns)

# Get index of FL_DATE
fl_date_index = cols.index('FL_DATE')

# Remove the new columns from the end
for col in ['year', 'quarter', 'month', 'day']:
    cols.remove(col)

# Insert new columns right after FL_DATE
for i, col in enumerate(['year', 'quarter', 'month', 'day']):
    cols.insert(fl_date_index + 1 + i, col)

# Reorder the DataFrame
df = df[cols]


# ### Categorical Columns
# so the CANCELLED column and DIVERTED column are according to `dictionary.html` binary values of 0 1, so to improve visualisation in BI, we can convert them to categorical values of 'No' and 'Yes' respectively.

# In[838]:


df['CANCELLED'].value_counts()


# In[839]:


df['DIVERTED'].value_counts()


# so we can convert CANCELLED and DIVERTED to integers, and then add columns for categorical

# In[840]:


df = to_int(df, 'CANCELLED')
df = to_int(df, 'DIVERTED')


# In[841]:


df['DIVERTED'].value_counts()


# In[842]:


df['CANCELLED'].value_counts()


# In[843]:


# Mapping for a new column
mapping = {
    0: 'No', 
    1: 'Yes'
}

# Create a new column 
df['cancelled_c'] = df['CANCELLED'].map(mapping)
df = to_string(df, 'cancelled_c')

df['diverted_c'] = df['DIVERTED'].map(mapping)
df = to_string(df, 'diverted_c')


# In[844]:


df['cancelled_c'].value_counts()


# In[845]:


df['diverted_c'].value_counts()


# ## Changing Column names
# to improve understandability

# In[846]:


df.rename(columns={'CRS_DEP_TIME': 'SCHEDULED_DEP_TIME'}, inplace=True)
df.rename(columns={'DEP_TIME': 'ACTUAL_DEP_TIME'}, inplace=True)
df.rename(columns={'CRS_ARR_TIME': 'SCHEDULED_ARR_TIME'}, inplace=True)
df.rename(columns={'ARR_TIME': 'ACTUAL_ARR_TIME'}, inplace=True)
df.rename(columns={'CRS_ELAPSED_TIME': 'SCHEDULED_ELAPSED_TIME'}, inplace=True)
df.rename(columns={'ELAPSED_TIME': 'ACTUAL_ELAPSED_TIME'}, inplace=True)
df.rename(columns={'FL_DATE': 'FLIGHT_DATE'}, inplace=True)
df.rename(columns={'FL_NUMBER': 'FLIGHT_NUMBER'}, inplace=True)

df.rename(columns={'WHEELS_OFF': 'WHEELS_LEFT_ORIGIN'}, inplace=True)
df.rename(columns={'WHEELS_ON': 'WHEELS_REACHED_DESTINATION'}, inplace=True)
df.rename(columns={'TAXI_IN': 'TAXI_TIME_DESTINATION'}, inplace=True)
df.rename(columns={'TAXI_OUT': 'TAXI_TIME_ORIGIN'}, inplace=True)
df.rename(columns={'AIR_TIME': 'IN_AIR_DURATION'}, inplace=True)


# # Recheck
# a simple recheck of all data statistics to see if the data is fine before donwloading

# In[847]:


df.shape


# In[848]:


# Check for missing values
df.isnull().sum()


# In[849]:


# Display data types
df.dtypes


# In[850]:


df


# # Download cleaned dataset

# In[851]:


# Save the cleaned DataFrame to a CSV file
df.to_csv('../data/flights_sample_3m_cleaned.csv', index=False)


# In[852]:


# Extract first 1000 rows
df_1000 = df.head(1000)

# Save to CSV with column headers
df_1000.to_csv('../data/flights_sample_1k_cleaned.csv', index=False)


# In[853]:


# revert pandas settings back to normal
pd.reset_option('display.max_columns')


# # Last run

# In[854]:


get_current_datetime()

