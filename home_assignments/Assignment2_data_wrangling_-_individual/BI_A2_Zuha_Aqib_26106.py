#!/usr/bin/env python
# coding: utf-8

# Name: Zuha Aqib   
# ERP ID: 26106    
# Section: M/W 10am - Miss Abeera Tariq    
# Date: 28th March 2025 

# In[1788]:


from datetime import datetime
print("Last time code executed:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# # Imports
# here we import all necessary documents at once

# In[1789]:


from datetime import datetime

# step1: import the data and to access it
import pandas as pd

# step2: numerically manipulate the data
import numpy as np

# step3: visualize the data
import matplotlib.pyplot as plt
import seaborn as sns

# step4: fix missing values in the data
from sklearn.impute import SimpleImputer
import missingno as msno
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
from statistics import mode

# step5: perform statistical processing on the data
from scipy import stats
from scipy.stats import ttest_ind, f_oneway, chi2_contingency, pearsonr
from statsmodels.stats.multicomp import pairwise_tukeyhsd


# In[1790]:


# Function to get current date and time as a string
def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# In[1791]:


print(pd.__version__)

# so because the version is >= 1.0, dataframe column types can be kept as "string" and not specifically "object"


# # Load the dataset
# here we load the dataset - using a pandas dataframe

# ## <span style="background-color: yellow"> Task 1 </span>
# Select a dataset of your choice from here https://tinyurl.com/BI-Assignment02-Datasets

# In[1792]:


file_path = "data/Healthcare.csv"
file_path


# In[1793]:


df = pd.read_csv(file_path, encoding="ISO-8859-1")

# Display basic info
df.info()


# In[1794]:


# so gender, billing amount, tax amount, room number and medication have missing values - rest are full. 
missing_columns = ['Gender', 'Billing Amount', 'TaxAmount', 'Room Number', 'Medication']
# this array will be used later in the code in TASK 4


# In[1795]:


df.describe(include='all')


# In[1796]:


df  # Show first few rows


# ## <span style="background-color: yellow"> Task 2 </span>
# Acquire some basic background knowledge about dataset to understand its context
# and relevance (if needed).

# # Data Preprocessing
# here we perform preprocessing steps on the data like cleaning, handling missing values, normalizing etc

# ## <span style="background-color: yellow"> Task 3 </span>
# - a. Develop a strategy to identify and correct data inconsistencies and data entry errors.
# - b. Write your strategy in the notebook as markdowns.
# - c. Provide brief interpretations of the corrections made.
# - d. Majority marks are for this interpretation and for the strategy (not for Python code)

# In[1797]:


# i can see that the first column is "?Name" so i will rename it to "Name"
df.rename(columns={df.columns[0]: "Name"}, inplace=True)
print(df.columns)


# In[1798]:


# Clean column names (strip special characters, extra spaces)
df.columns = df.columns.str.strip().str.replace(r"[^\w\s]", "").str.replace("  ", " ")
print(df.columns)


# In[1799]:


# remove whitespaces
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)


# ### Analyzing Name Column
# - first convert column to string
# - here i noticed an inconsistency that if its "Mrs." so the gender type should also match and be "Female", but for row 4, its "Male" which is wrong. So i will correct it.
# - then drop all names that have less than 1 length

# In[1800]:


# Convert to 'string' dtype (pandas 1.0+)
df['Name'] = df['Name'].astype('string')
print(df['Name'].dtype)  


# In[1801]:


count_changed = 0

# Define title-gender rules (case-insensitive)
title_rules = {
    'mr.': 'Male',       # Mr. → Male
    'mrs.': 'Female',      # Mrs. → Female
    'miss': 'Female',      # Miss → Female
    'ms.': 'Female'        # Ms. → Female
}

# Check and correct genders
for index, row in df.iterrows():
    name = str(row['Name']).lower()  # Convert to lowercase for case-insensitive check
    current_gender = row['Gender']

    for title, expected_gender in title_rules.items():
        if title in name:
            if pd.isna(row['Gender']):
                print(f"Correcting '{row['Name']}': Gender '{expected_gender}'")
                df.at[index, 'Gender'] = expected_gender
                count_changed += 1
            elif current_gender != expected_gender:
                print(f"Correcting '{row['Name']}': Gender '{current_gender}' → '{expected_gender}'")
                df.at[index, 'Gender'] = expected_gender
                count_changed += 1
            break  # Stop after first title match
print(count_changed)


# In[1802]:


# wow thats alot of mismatch. i had added some code for doctors and professors, but then it was becoming a hassle so i removed it.

# lets also remove names with less than <=1 length
total_rows_before = len(df)  # Count total rows before dropping

# Drop rows where 'hospital' has <=1 character 
df= df[df['Name'].str.len() > 1 | df['Name'].isna()].copy()  # Using .copy() to avoid SettingWithCopyWarning

# Calculate rows dropped
rows_dropped = total_rows_before - len(df)

# Display results
print(f"Total rows before dropping: {total_rows_before}")
print(f"Rows dropped (Name ≤1 char): {rows_dropped}")
print(f"Remaining rows: {len(df)}")


# ### <span style="background-color: orange"> API WORK </span>
# - here we make a function `to_string()` which basically converts a given column name to a string type
# - next we will make a function `to_int()` which converts a given column name to an integer type
# - next we will make a function `to_float()` which converts a given column name to a float type
# - next we will make a function `remove_small_size_names()` which removes all small sized names

# In[1803]:


def api_to_string(df, column_name):
    """
    Convert a pandas DataFrame column to a string.
    """
    df[column_name] = df[column_name].astype('string')
    print(f"Column Name: '{column_name}', Type: {df[column_name].dtype}")
    return df  


# In[1804]:


def api_to_int(df, column_name):
    """
    Convert a pandas DataFrame column to a int.
    """
    df[column_name] = df[column_name].astype('int64')
    print(f"Column Name: '{column_name}', Type: {df[column_name].dtype}")
    return df  


# In[1805]:


def api_to_float(df, column_name):
    """
    Convert a pandas DataFrame column to a float.
    """
    df[column_name] = df[column_name].astype('float64')
    print(f"Column Name: '{column_name}', Type: {df[column_name].dtype}")
    return df  


# In[1806]:


def api_remove_small_size_names(df, column_name, lower_limit=1):
    # lets also remove names with less than <=lowerlimit length
    total_rows_before = len(df)  # Count total rows before dropping

    # Drop rows where column has <=1 character 
    df= df[df[column_name].str.len() > lower_limit | df[column_name].isna()].copy()  # Using .copy() to avoid SettingWithCopyWarning

    # Calculate rows dropped
    rows_dropped = total_rows_before - len(df)

    # Display results
    print(f"Total rows before dropping: {total_rows_before}")
    print(f"Rows dropped ('{column_name}' ≤{lower_limit} char): {rows_dropped}")
    print(f"Remaining rows: {len(df)}")

    return df


# ### Analyzing Age Column
# - here we can check that all ages should be >0 and <100, and we can also find the counts of each age group to see which ones we mostly deal with. 
# - we will also additionally convert the age column to a numerical type to be able to perform numerical operations on it.

# In[1807]:


# Count ages less than 0 or greater than 100
invalid_age_count = ((df['Age'] < 0) | (df['Age'] > 100)).sum()
print("Number of invalid ages (<0 or >100):", invalid_age_count)


# In[1808]:


# okay great! none invalid. lets apply a loop to see how many ages are in which range
for category in range(10, 101, 10):
    age_range_count = ((df['Age'] >= (category-10)) & (df['Age'] <= category)).sum()
    print("(",(category-10),",",category,") = ", age_range_count)


# In[1809]:


# so from these range counts we see that we don't have too young or too old people, and majority are adults between 20 and 80. there is no data inconsistency. 

# lets lastly convert all the data to numeric and see how many are null
df = api_to_int(df, 'Age')

print(df['Age'].isnull().sum())


# ### <span style="background-color: orange"> API WORK </span>
# - create a function `limit_checker()` that drops all rows of a numeric column that are less than a certain threshold

# In[1810]:


def api_limit_checker(df, lower_limit, upper_limit, column_name):
    if upper_limit is None:
        invalid_mask = (df[column_name] < lower_limit)
    else:
        invalid_mask = (df[column_name] < lower_limit) | (df[column_name] > upper_limit)
    invalid = invalid_mask.sum()
    print(f"Number of invalid (<{lower_limit} or >{upper_limit}):{invalid}")

    if invalid > 0:
        # Drop invalid rows and keep the rest
        df_filtered = df[~invalid_mask].copy()  # ~ means logical NOT
        dropped_count = len(df) - len(df_filtered)

        print(f"Dropped {dropped_count} rows.")
        return df_filtered
    else:
        print("No rows to drop.")
        return df.copy()


# ### Analyzing Gender Column
# - here we first need to make everyone lowercase and remove trailing spaces because 'male', 'Male', 'Male ', ' Male' all are same
# - then we can convert to M F to make it more readable and less data storage
# - then we can find the empty spaces that don't have a gender. these will be dealt later in task 4
# - then we convert the column to string

# In[1811]:


# now lets all see the count of all of the males and females
gender_counts = df['Gender'].value_counts()
print("Gender Counts:\n", gender_counts)


# In[1812]:


# convert genders to lowercase
df['Gender'] = df['Gender'].str.lower()

# now lets convert all 'Male' to M and 'Female' to F
df['Gender'] = df['Gender'].replace({'male': 'M', 'female': 'F'})

# now lets all see the count of all of the males and females
gender_counts = df['Gender'].value_counts()
print("Gender Counts:\n", gender_counts)


# In[1813]:


# so theres not much of a difference between males and females.

# lets convert the column to gender
df = api_to_string(df, 'Gender')


# ### Analyzing Blood Type Column
# - so according to the internet there are 8 blood types, there are many more but they are very unquie and rare.
# - we can first extract the unique blood types and their count. if there are some blood types which EXIST and only occur RARELY then we can keep them but if there are blood types which DONT EXIST then we can remove all those rows.
# - we can also capitalize all of them first to make it more easier
# - also convert column to string

# In[1814]:


# Convert to 'string' dtype (pandas 1.0+)
df = api_to_string(df, 'Blood Type')


# In[1815]:


# before beginning the unique extraction, lets make them all capital
df['Blood Type'] = df['Blood Type'].str.upper()

# lets extract all unique values
unique_blood_types = df['Blood Type'].unique()
print("Unique Blood Types:", unique_blood_types)


# In[1816]:


# so these are the 8 blood types in the world. but lets just find their counts to see if any of them are rare?
blood_type_counts = df['Blood Type'].value_counts()
print("\nBlood Type Counts:\n", blood_type_counts)


# In[1817]:


# so all the blood types are fine. we dont have to remove any.


# ### Analyzing Medical Condition Column
# - same as blood type, lets first extract the unique columns and analyse their counts. 
# - here we wont convert the entire thing to lower/upper, we will convert while counting but not fix it
# - also convert to string

# In[1818]:


# Convert to 'string' dtype (pandas 1.0+)
df = api_to_string(df, 'Medical Condition')


# In[1819]:


# lets see how many medical conditions we have
unique_medical_conditions = df['Medical Condition'].str.lower().unique()
print("Unique Medical Conditions:", unique_medical_conditions)


# In[1820]:


# oh so we see that hypertension is repeated with one difference. lets first find the counts to see how many are repeated differently
medical_conditions_counts = df['Medical Condition'].value_counts()
print("\nMedical Condition Counts:\n", medical_conditions_counts)


# In[1821]:


# so we can clearly see that 'Hypertensions' is a simple mistake made in data entry. lets convert that single one to 'Hypertension'
df['Medical Condition'] = df['Medical Condition'].replace('Hypertensions', 'Hypertension')
# now instead of printing the df again, lets re-calculate the count of conditions and analyze that
medical_conditions_counts = df['Medical Condition'].value_counts()
print("\nMedical Condition Counts:\n", medical_conditions_counts)


# ### Analyzing Date of Admission Column
# - lets first try a unique() and see it, it will give us the count of unique values in the column.
# - then lets convert all to date_time format

# In[1822]:


unique_admission_date = df['Date of Admission'].value_counts()
print("\nunique_admission_date Counts:\n", unique_admission_date)


# In[1823]:


# okay so reading all 1800 values is a hassle, lets just convert to date and time format
df['Date of Admission'] = pd.to_datetime(df['Date of Admission'], errors='coerce', dayfirst=True)
df['Date of Admission']


# In[1824]:


# after printing we can see its converted. lets also see how many are null.
print(df['Date of Admission'].isna().sum())


# ### <span style="background-color: orange"> API WORK </span>
# - create a function `to_date_time()` which converts a columns datatype to date_time

# In[1825]:


def api_to_date_time(df, column_name):
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce', dayfirst=True)
    df[column_name]
    print(f"Column Name: '{column_name}', Type: {df[column_name].dtype}")
    return df  


# ### Analyzing Doctor Column
# - convert to string
# - extract unique doctor names, and count of each name
# - drop all rows with names less than length 1 (i.e., empty strings, or single letter names)

# In[1826]:


# Convert to 'string' dtype (pandas 1.0+)
df = api_to_string(df, 'Doctor')


# In[1827]:


unique_doctor = df['Doctor'].value_counts()
print("\n unique_doctor Counts:\n", unique_doctor)


# In[1828]:


df = api_remove_small_size_names(df, 'Doctor')


# ### Analyzing Hospital Column
# - convert to string
# - extract unique hospital names and count of each name
# - drop all hospital names that have less than one length and are not empty

# In[1829]:


# Convert to 'string' dtype (pandas 1.0+)
df['Hospital'] = df['Hospital'].astype('string')
print(df['Hospital'].dtype)  


# In[1830]:


unique_hospital = df['Hospital'].value_counts()
print("\n unique_hospital Counts:\n", unique_hospital)


# In[1831]:


# im not really sure what to clean here, i can run the reject all length lesser than 1 names, but i dont think there shall be such a case
df = api_remove_small_size_names(df, 'Hospital')


# ### Analyzing Insurance Provider Column
# - convert to string
# - fix any miss spellings

# In[1832]:


df = api_to_string(df, 'Insurance Provider')


# In[1833]:


unique = df['Insurance Provider'].value_counts()
print("\n unique Counts:\n", unique)


# In[1834]:


df['Insurance Provider'] = df['Insurance Provider'].replace('Blue Crosser', 'Blue Cross')
df['Insurance Provider'] = df['Insurance Provider'].replace('Blue Crossss', 'Blue Cross')

unique = df['Insurance Provider'].value_counts()
print("\n unique Counts:\n", unique)


# ### Analyzing Billing Amount Column
# - already in correct type
# - check if any of the values are out of bound

# In[1835]:


df = api_limit_checker(df, 0, None, 'Billing Amount')


# ### Analyzing Tax Amount Column
# - compute the average tax percentage
# - remove all rows that are not having the average tax percentage

# In[1836]:


# Calculate tax percentages (only where tax is not empty)
tax_percentages = []
rows_to_drop = [] # these rows we will drop if they are too different from the tax %

for index, row in df.iterrows():
    # Skip if TaxAmount is NaN or Billing Amount is zero/NaN
    if not pd.isna(row['TaxAmount']) and not pd.isna(row['Billing Amount']) and row['Billing Amount'] != 0:
        tax_percent = (row['TaxAmount'] / row['Billing Amount']) * 100
        if not (14 <= tax_percent <= 16):
            rows_to_drop.append(index)
        tax_percentages.append(tax_percent)

# Compute average tax percentage
average_tax_percent = np.mean(tax_percentages) if tax_percentages else 0

df = df.drop(rows_to_drop)
print(f"Rows dropped: {len(rows_to_drop)}")

print(f"Average Tax Percentage: {average_tax_percent:.2f}%")


# In[1837]:


# so here in the previous code we first iterated over the values, computed the average tax % and dropped all the incorrect values.


# ### Analyzing Room Number Column
# - check if the column can be converted to integer, else keep at float
# - get all unique values and check

# In[1838]:


df = api_to_float(df, 'Room Number')


# In[1839]:


unique = df['Room Number'].value_counts()
print("\n unique Counts:\n", unique)


# ### Analyzing Admission Type Column
# - convert to string
# - extract all unique values and fix incorrect ones

# In[1840]:


df = api_to_string(df, 'Admission Type')


# In[1841]:


unique = df['Admission Type'].value_counts()
print("\n unique Counts:\n", unique)


# In[1842]:


df['Admission Type'] = df['Admission Type'].replace('ELECTIvess', 'Elective')
df['Admission Type'] = df['Admission Type'].replace('Electivess', 'Elective')
df['Admission Type'] = df['Admission Type'].replace('Emergecn.', 'Emergency')

unique = df['Admission Type'].value_counts()
print("\n unique Counts:\n", unique)


# ### Analyzing Discharge Date Column
# - convert to date, time format

# In[1843]:


# lets just convert to date and time format
df = api_to_date_time(df, 'Discharge Date')


# ### Analyzing Medication Column
# - cpnvert to string
# - analyse strings to find any misspelled

# In[1844]:


df = api_to_string(df, 'Medication')


# In[1845]:


unique = df['Medication'].value_counts()
print("\n unique Counts:\n", unique)


# ### Analyzing Test Results Column
# - convert to string
# - fix any misspells

# In[1846]:


df = api_to_string(df, 'Test Results')


# In[1847]:


unique = df['Test Results'].value_counts()
print("\n unique Counts:\n", unique)


# In[1848]:


df['Test Results'] = df['Test Results'].replace('Normalll', 'Normal')
df['Test Results'] = df['Test Results'].replace('Abnormall', 'Abnormal')
df['Test Results'] = df['Test Results'].replace('Inconclusiveity', 'Inconclusive')

unique = df['Test Results'].value_counts()
print("\n unique Counts:\n", unique)


# ### Recheck
# now lets see the dataset after all columns have been cleaned

# In[1849]:


df.info()


# ## <span style="background-color: yellow"> Task 4 </span>
# - a. Develop a strategy to handle missing values for each column separately.
# - b. Write down your strategy in the notebook before you execute it.
# - c. Ensure to make use of missingno library for missing value type identification and strategy building.
# - d. Write down the interpretation of your results in your notebook as much as is possible. This should be brief, e.g., one sentence to describe a visual output, or 2-3 sentences summarizing a sequence of results etc.
# - e. Majority marks are for this interpretation and for the strategy (not for Python code)

# In[1850]:


df.isnull().sum()


# In[1851]:


# so the missing columns are
missing_columns


# ### Graphing
# here lets do some statistical testing to see the attributes

# In[1852]:


# Visualize missing data with missingno
msno.matrix(df)
plt.show()

msno.bar(df)
plt.show()


# In[1853]:


df.shape


# In[1854]:


msno.heatmap(df, figsize=(10,6))


# In[1855]:


msno.dendrogram(df)


# ### Gender
# - because its a single case, just display the name of the missing gender row and manually update the gender

# In[1856]:


null_gender_rows = df[df['Gender'].isnull()]
null_gender_rows


# In[1857]:


gender_missing_index = null_gender_rows.index[0]
gender_missing_index


# In[1858]:


# her name is TIFFANY so a female. lets update it as female
df.at[gender_missing_index, 'Gender'] = 'F'
df.head(gender_missing_index+1) # display that row


# In[1859]:


df.isnull().sum()


# ### Billing Amount
# - because we dont know the potenial bill for the null case, we drop that row. 

# In[1860]:


rows_before = len(df)
df = df.dropna(subset=['Billing Amount'])
rows_after = len(df)
print(f"Before: {rows_before}, After: {rows_after}, Dropped: {rows_before-rows_after}")


# In[1861]:


df.isnull().sum()


# ### Tax Amount
# - now use the `average_tax_percentage` we computed above while cleaning and use it to fill all the empty values

# In[1862]:


count_filled = 0
for index, row in df.iterrows():
    # Check if TaxAmount is null AND Billing Amount is valid (not null and not zero)
    if (pd.isna(row['TaxAmount']) and 
        not pd.isna(row['Billing Amount']) and 
        row['Billing Amount'] != 0):

        # Calculate tax using average percentage
        calculated_tax = (row['Billing Amount'] * average_tax_percent) / 100
        df.at[index, 'TaxAmount'] = calculated_tax
        count_filled += 1

count_filled


# In[1863]:


df.isnull().sum()


# ### Medication
# - here we have one empty cell. so one way is to drop it. but lets use some stretegy.
# - there are many people with the same medical condition. lets first extract what medical condition the empty cell has. then lets extract all the medications given to the people with the SAME medical condition. now whatever people are given the most (mode), lets give it that medication.
# - ai has been used here, i gave it the whole idea and prompt, it gave me code. 

# In[1864]:


# Find row with missing medication
missing_med_row = df[df['Medication'].isna() & df['Medical Condition'].notna()]
missing_med_row


# In[1865]:


if not missing_med_row.empty:
    # Get medical condition and row index
    condition = missing_med_row.iloc[0]['Medical Condition']
    row_index = missing_med_row.index[0]

    print(f"Found missing medication at row {row_index}")
    print(f"Medical Condition: {condition}")

    # Get all medications for this condition
    condition_meds = df[df['Medical Condition'] == condition]['Medication']
    med_counts = condition_meds.value_counts()

    print("\nMedication distribution for this condition:")
    print(med_counts)

    try:
        # Get mode (most common medication)
        most_common_med = mode(condition_meds)
        df.at[row_index, 'Medication'] = most_common_med

        print(f"\nAssigned medication: {most_common_med}")
    except:
        print("\nNo medication data available for this condition")
else:
    print("No rows with missing medication found")


# In[1866]:


df.isnull().sum()


# ### Room Number
# - so there are 4 empty cells out of 10022 cells. we can drop them.
# - OR lets apply something meangingful. lets extract all the patients who have the same insurance provider, doctor and hospital and count what room numbers they are given.

# In[1867]:


# Find row with missing medication
missing_room_row = df[df['Room Number'].isna()]
missing_room_row


# In[1868]:


print(f"Found {len(missing_room_row)} rows with missing room numbers")


# In[1869]:


for index, row in missing_room_row.iterrows():
    insurance = row['Insurance Provider']
    hospital = row['Hospital']
    doctor = row['Doctor']
    row_index = index

    print(f"Found missing medication at row {row_index}")
    print(f"Insurance Provider: {insurance}")
    print(f"Hospital: {hospital}")
    print(f"Doctor: {doctor}")

    # Get matching room numbers (with proper boolean conditions)
    room_mask = (
        (df['Insurance Provider'] == insurance) & 
        (df['Hospital'] == hospital) & 
        (df['Doctor'] == doctor)
    )
    room_num = df.loc[room_mask, 'Room Number'].dropna()

    print(len(room_num))

    if not room_num.empty:
        counts = room_num.value_counts()
        print("\nRoom Number distribution:")
        print(counts)


# In[1870]:


# ok so none. lets try it without doctor
for index, row in missing_room_row.iterrows():
    insurance = row['Insurance Provider']
    hospital = row['Hospital']
    # doctor = row['Doctor']
    row_index = index

    print(f"Found missing medication at row {row_index}")
    print(f"Insurance Provider: {insurance}")
    print(f"Hospital: {hospital}")
    # print(f"Doctor: {doctor}")

    # Get matching room numbers (with proper boolean conditions)
    room_mask = (
        (df['Insurance Provider'] == insurance) & 
        (df['Hospital'] == hospital) 
        # (df['Doctor'] == doctor)
    )
    room_num = df.loc[room_mask, 'Room Number'].dropna()

    print(len(room_num))

    if not room_num.empty:
        counts = room_num.value_counts()
        print("\nRoom Number distribution:")
        print(counts)


# In[1871]:


# so none again. lets remove hospital as well
for index, row in missing_room_row.iterrows():
    insurance = row['Insurance Provider']
    # hospital = row['Hospital']
    # doctor = row['Doctor']
    row_index = index

    print(f"Found missing medication at row {row_index}")
    print(f"Insurance Provider: {insurance}")
    # print(f"Hospital: {hospital}")
    # print(f"Doctor: {doctor}")

    # Get matching room numbers (with proper boolean conditions)
    room_mask = (
        (df['Insurance Provider'] == insurance) 
        # (df['Hospital'] == hospital) 
        # (df['Doctor'] == doctor)
    )
    room_num = df.loc[room_mask, 'Room Number'].dropna()

    print(len(room_num))

    if not room_num.empty:
        counts = room_num.value_counts()
        print("\nRoom Number distribution:")
        print(counts)


# In[1872]:


# okay good! lets assign the MODE of them.

for index, row in missing_room_row.iterrows():
    insurance = row['Insurance Provider']
    # hospital = row['Hospital']
    # doctor = row['Doctor']
    row_index = index

    print(f"Found missing medication at row {row_index}")
    print(f"Insurance Provider: {insurance}")
    # print(f"Hospital: {hospital}")
    # print(f"Doctor: {doctor}")

    # Get matching room numbers (with proper boolean conditions)
    room_mask = (
        (df['Insurance Provider'] == insurance) 
        # (df['Hospital'] == hospital) 
        # (df['Doctor'] == doctor)
    )
    room_num = df.loc[room_mask, 'Room Number'].dropna()

    print(len(room_num))

    if not room_num.empty:
        counts = room_num.value_counts()
        print("\nRoom Number distribution:")
        print(counts)

        try:
            # Get mode
            most_common = mode(room_num)
            df.at[index, 'Room Number'] = most_common
            print(f"\nAssigned room number: {most_common} \n\n")
        except:
            print("\nNo room number data available for this condition")


# In[1873]:


df.isnull().sum()


# # Stastical Testing
# here we perform stastical testing

# ## <span style="background-color: yellow"> Task 5 </span>
# Univariate Analysis
# - a. Histograms, boxplots, density plots of important numerical columns
# - b. Frequency histograms of important categorical data
# - c. Focus on outlier analysis, anomaly detection (if applicable)
# - d. Provide brief interpretations of the findings, focusing on insights rather than code.

# In[1874]:


important_numerical_columns = ['Age', 'Billing Amount', 'TaxAmount', 'Room Number']


# In[1875]:


df.dtypes


# In[1876]:


important_categorical_columns = ['Gender', 'Blood Type', 'Medical Condition', 'Admission Type', 'Medication', 'Test Results']
# hospital, doctor, insurance are not included as they were too diverse, as seen in task 3


# ### <span style="background-color: orange"> API WORK </span>
# - here lets make a function `api_histogram` which makes a histogram
# - same for `api_boxplot`, `api_density_plot`
# - same for `api_frequency`

# In[1877]:


def api_boxplot(df, col):
    fig, axs = plt.subplots(figsize=(8, 4))
    fig.suptitle(f"Univariate Analysis for {col}", fontsize=16)

    # Boxplot
    sns.boxplot(x=df[col])
    # axs[1].set_title("Boxplot")

    plt.tight_layout()
    plt.show()


# In[1878]:


def api_histogram(df, col):
    fig, axs = plt.subplots(figsize=(8, 4))
    fig.suptitle(f"Univariate Analysis for {col}", fontsize=16)

    # Histogram
    sns.histplot(df[col], kde=False)
    # axs[0].set_title("Histogram")

    plt.tight_layout()
    plt.show()


# In[1879]:


def api_density_plot(df, col):
    fig, axs = plt.subplots(figsize=(8, 4))
    fig.suptitle(f"Univariate Analysis for {col}", fontsize=16)

    # KDE/Distribution plot
    sns.kdeplot(df[col], fill=True)
    # axs[2].set_title("Density Plot")

    plt.tight_layout()
    plt.show()


# In[1880]:


def api_frequency(df, col):
    plt.figure(figsize=(10, 4))
    sns.countplot(data=df, x=col, order=df[col].value_counts().index)
    plt.title(f"Frequency of {col}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# ### N U M E R I C A L

# In[1881]:


len(important_numerical_columns)


# ### COL 1

# In[1882]:


col = important_numerical_columns[0]
api_histogram(df, col)
api_boxplot(df, col)
api_density_plot(df, col)


# In[1883]:


# seems evenly distributed, more younger teenagers though.


# ### COL 2

# In[1884]:


col = important_numerical_columns[1]
api_histogram(df, col)
api_boxplot(df, col)
api_density_plot(df, col)


# In[1885]:


# its highly likely that you wont get a smaller bill - however bills are distributed thus telling us that people are charged normally


# ### COL 3

# In[1886]:


col = important_numerical_columns[2]
api_histogram(df, col)
api_boxplot(df, col)
api_density_plot(df, col)


# In[1887]:


# evenly distributed


# ### COL 4

# In[1888]:


col = important_numerical_columns[3]
api_histogram(df, col)
api_boxplot(df, col)
api_density_plot(df, col)


# In[1889]:


# the chance of getting any room is even


# ### C A T E G O R I C A L

# In[1890]:


len(important_categorical_columns)


# ### COL 1

# In[1891]:


col = important_categorical_columns[0]
api_frequency(df, col)


# In[1892]:


# both genders get equal chance, no discrimination


# ### COL 2

# In[1893]:


col = important_categorical_columns[1]
api_frequency(df, col)


# In[1894]:


# no rare blood types


# ### COL 3

# In[1895]:


col = important_categorical_columns[2]
api_frequency(df, col)


# In[1896]:


# these 6 medical conditions are having equal probability - there are no rare ones.


# ### COL 4

# In[1897]:


col = important_categorical_columns[3]
api_frequency(df, col)


# In[1898]:


# there is slighly more urgent admission types


# ### COL 5

# In[1899]:


col = important_categorical_columns[4]
api_frequency(df, col)


# In[1900]:


# pencilin is most given, however all medications seem general purpose


# ### COL 6

# In[1901]:


col = important_categorical_columns[5]
api_frequency(df, col)


# In[1902]:


# there is higher abnormal test results meaning people are sick more


# ### O U T L I E R
# - we can see there are no outliers but lets just test it

# ### <span style="background-color: orange"> API WORK </span>
# - for outlier analysis

# In[1903]:


def api_view_outliers(df, col):
  q1 = df[col].quantile(0.25)
  q3 = df[col].quantile(0.75)
  iqr = q3 - q1
  lower_bound = q1 - 1.5 * iqr
  upper_bound = q3 + 1.5 * iqr
  outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
  return outliers


# In[1904]:


for col in important_numerical_columns:
    print(col)
    print(api_view_outliers(df, col) , "\n\n")


# In[1905]:


# so no outliers proved.


# ## <span style="background-color: yellow"> Task 6 </span>
# Bivariate/Multi-variate Analysis
# - a. Perform analysis using various statistical tests as studied including ANOVA, Ttest, Tukey, Chi-squared, and correlation heatmaps.
# - b. Optionally, explore additional techniques like clustering or regression.
# - c. Provide brief interpretations of the findings

# ### <span style="background-color: orange"> API WORK </span>
# - for correlation heatmap: `numerical_vs_numerical`
# - for annova and t-text: `numerical_vs_categorical`
# - for chisquared: `categorical_vs_categorical`

# In[1906]:


def api_numerical_vs_numerical(df):
    numeric_df = df.select_dtypes(include=['number'])
    # Calculate the correlation matrix
    correlation_matrix = numeric_df.corr()

    # Create the heatmap
    plt.figure(figsize=(6, 5))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
    plt.title('Correlation Heatmap of Numerical Features')
    plt.show()


# In[1907]:


def api_numerical_vs_categorical(df, numerical_cols, categorical_cols):
    for num_col in numerical_cols:
        for cat_col in categorical_cols:
            unique_vals = df[cat_col].dropna().unique()
            if len(unique_vals) == 2:
                # T-test
                groups = [df[df[cat_col] == val][num_col].dropna() for val in unique_vals]
                if all(len(g) > 1 for g in groups):
                    t_stat, p_val = ttest_ind(*groups)
                    print(f"T-test between {unique_vals[0]} and {unique_vals[1]} for {num_col}: t={t_stat:.2f}, p={p_val:.4f}")
            elif len(unique_vals) > 2:
                # ANOVA
                groups = [df[df[cat_col] == val][num_col].dropna() for val in unique_vals]
                if all(len(g) > 1 for g in groups):
                    f_stat, p_val = f_oneway(*groups)
                    print(f"ANOVA for {num_col} across {cat_col}: F={f_stat:.2f}, p={p_val:.4f}")
                    if p_val < 0.05:
                        tukey = pairwise_tukeyhsd(df[num_col], df[cat_col])
                        print(f"\nTukey HSD Post-Hoc Test for {num_col} vs {cat_col}")
                        print(tukey)


# In[1908]:


def api_categorical_vs_categorical(df, categorical_cols):
    for i in range(len(categorical_cols)):
        for j in range(i + 1, len(categorical_cols)):
            col1 = categorical_cols[i]
            col2 = categorical_cols[j]
            contingency = pd.crosstab(df[col1], df[col2])
            if contingency.shape[0] > 1 and contingency.shape[1] > 1:
                chi2, p, dof, expected = chi2_contingency(contingency)
                print(f"Chi-squared Test between {col1} and {col2}: chi2={chi2:.2f}, p={p:.4f}")


# ### NUMERICAL VS NUMERICAL
# - correlation heatmap

# In[1909]:


api_numerical_vs_numerical(df)


# In[1910]:


# so billing amount and tax amount are correlated. we already know this as tax = 15% of bill. 


# ### NUMERICAL VS CATEGORICAL
# - annova and t-test

# In[1911]:


api_numerical_vs_categorical(df, important_numerical_columns, important_categorical_columns)


# - gender does not impact patient
# - cost, room number, bill all are independent of gender
# - no effect of blood type
# - no medical condition effects any age, charges, room number
# - emergency patients are billed more
# - cost is only affected by admission type and nothing else. medication may effect but not enough evudence

# ### CATEGORICAL VS CATEGORICAL
# - chisquared

# In[1912]:


api_categorical_vs_categorical(df, important_categorical_columns)


# - all are greater than 0.5 meaning no significant associations found
# - everything is independent of each other

# # AI USAGE
# i have mentioned in the part i used AI, task 3, 4 were done by myself, in task 5 6 i used ai to help code plots.  
# i used chatgpt

# # Submission
# save the df file at the end

# In[1913]:


df.to_csv('data/Healthcare_cleaned.csv', index=False)  # Doesn't save row indices
df

