#!/usr/bin/env python
# coding: utf-8

# Business Intelligence Project    
# Name: Zehra Ahmed, Farah Inayat, Kisa Fatima, Zuha Aqib    
# Date: 31-May-2025

# In[29]:


# print when the last code was run
from datetime import datetime
datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# In[30]:


# Capture start time
start_time = datetime.now()


# # Imports

# In[31]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')


# In[32]:


# Function to get current date and time as a string
def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# # Data Loading

# In[33]:


# Load the dataset
df = pd.read_csv('../data/flights_jantojun2020_3M_cleaned.csv')

pd.set_option('display.max_columns', None)


# In[34]:


df


# In[35]:


df.dtypes


# In[36]:


df.shape


# # PRE TESTING

# In[37]:


# Identify numerical and categorical columns
numerical_cols   = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()

print(f"Detected {len(numerical_cols)} numerical columns: {numerical_cols}")
print(f"\nDetected {len(categorical_cols)} categorical columns: {categorical_cols}\n")


# In[38]:


# For detailed CSV output
csv_results = []  # each entry: [Column A, Column B, Test Name, Result, Inference]

# For summary TXT output
normal_columns     = []
non_normal_columns = []
outlier_columns    = []
strong_corr_pairs  = []
chi_assoc_pairs    = []


# # NORMALITY TESTING

# In[39]:


print("=== 1. Normality Testing (Shapiro–Wilk with subsample) ===\n")

# Define max sample size for Shapiro–Wilk
MAX_SW_SAMPLE = 5000

for col in numerical_cols:
    # Drop NA and get the non‐null values
    data_full = df[col].dropna()
    n_full = len(data_full)
    if n_full < 3:
        print(f"• {col}: only {n_full} non‐NA rows, skipping normality test.")
        continue

    # If more than MAX_SW_SAMPLE, take a random subsample of size MAX_SW_SAMPLE
    if n_full > MAX_SW_SAMPLE:
        data = data_full.sample(n=MAX_SW_SAMPLE, random_state=42).values
        used_n = MAX_SW_SAMPLE
        note = f"(used random subsample of {MAX_SW_SAMPLE}/{n_full})"
    else:
        data = data_full.values
        used_n = n_full
        note = f"(using full {n_full})"

    # Now run Shapiro–Wilk on data (length ≤ 5000)
    stat, p_value = stats.shapiro(data)
    if p_value > 0.05:
        inference = "Normally distributed"
        normal_columns.append(col)
    else:
        inference = "Not normally distributed"
        non_normal_columns.append(col)

    result_str = f"statistic={stat:.4f}, p={p_value:.4f}, n={used_n} {note}"
    # print(f"• {col}: p = {p_value:.4f} → {inference} {note}")
    csv_results.append([col, "", "Shapiro-Wilk", result_str, inference])

    # —– ALTERNATIVE (D’Agostino’s K²) on full data: uncomment if you prefer 
    # k2, p2 = stats.normaltest(data_full)
    # inf2 = "Normally distributed" if p2 > 0.05 else "Not normally distributed"
    # result2 = f"statistic={k2:.4f}, p={p2:.4f}, n={n_full}"
    # print(f"   (D’Agostino K²) → p = {p2:.4f} → {inf2} (n={n_full})")
    # csv_results.append([col, "", "Normaltest (D’Agostino)", result2, inf2])

print("\nNormal columns    :", ", ".join(normal_columns)     if normal_columns     else "None")
print("Non-normal columns:", ", ".join(non_normal_columns) if non_normal_columns else "None")
print("\n")


# # OUTLIER TESTING

# In[40]:


print("=== 2. Outlier Detection (Z-Score Method) ===\n")
for col in numerical_cols:
    col_data = df[col].dropna()
    z_scores = np.abs(stats.zscore(col_data))
    num_outliers = (z_scores > 3).sum()
    if num_outliers > 0:
        inference = f"{num_outliers} outlier(s) present"
        outlier_columns.append(col)
    else:
        inference = "No significant outliers"
    result_str = f"num_outliers={num_outliers}"
    
    # print(f"• {col}: {num_outliers} outlier(s) → {inference}")
    csv_results.append([col, "", "Z-Score Outlier", result_str, inference])
print("\n► Columns with outliers:", ", ".join(outlier_columns) if outlier_columns else "None")
print("\n")


# # CORRELATION TESTING

# In[41]:


print("=== 3. Correlation Analysis (Pearson) ===\n")
corr_matrix = df[numerical_cols].corr()

for i in range(len(numerical_cols)):
    for j in range(i+1, len(numerical_cols)):
        col1 = numerical_cols[i]
        col2 = numerical_cols[j]
        r_value = corr_matrix.loc[col1, col2]
        
        if abs(r_value) > 0.85:
            strength = "Strong correlation"
            strong_corr_pairs.append(f"{col1} & {col2} (r={r_value:.4f})")
        elif abs(r_value) > 0.5:
            strength = "Moderate correlation"
        else:
            strength = "Weak correlation"
        
        result_str = f"r={r_value:.4f}"
        # print(f"• {col1} vs {col2}: r = {r_value:.4f} → {strength}")
        csv_results.append([col1, col2, "Pearson Correlation", result_str, strength])
print("\n► Strongly correlated pairs:", ", ".join(strong_corr_pairs) if strong_corr_pairs else "None")
print("\n")


# # CHI SQUARE

# In[42]:


print("=== 4. Chi-Square Tests (Categorical vs Categorical, Subsampled) ===\n")
MAX_CS_SAMPLE = 5000

print(len(categorical_cols)*len(categorical_cols))
count = 0

for col1 in categorical_cols:
    for col2 in categorical_cols:
        print(count)
        count+=1
        if col1 == col2:
            continue

        # Keep only rows where both columns are non-null
        sub = df[[col1, col2]].dropna()
        n_sub = len(sub)
        if n_sub < 2:
            print(f"• {col1} vs {col2}: too few non‐NA rows ({n_sub}), skipping.")
            continue

        # If more than MAX_CS_SAMPLE, sample down:
        if n_sub > MAX_CS_SAMPLE:
            sub = sub.sample(n=MAX_CS_SAMPLE, random_state=42)
            note = f"(sampled {MAX_CS_SAMPLE}/{n_sub})"
        else:
            note = f"(using full {n_sub})"

        # Build crosstab and run Chi‐Square
        try:
            ctab     = pd.crosstab(sub[col1], sub[col2])
            chi2, p_val, dof, expected = stats.chi2_contingency(ctab)

            if p_val < 0.05:
                inference = "Associated (p < 0.05)"
                chi_assoc_pairs.append(f"{col1} & {col2} (p={p_val:.4f})")
            else:
                inference = "Independent (p ≥ 0.05)"

            result_str = f"chi2={chi2:.4f}, p={p_val:.4f}, dof={dof}, n={len(sub)} {note}"
            print(f"• {col1} vs {col2}: p = {p_val:.4f} → {inference} {note}")
            csv_results.append([col1, col2, "Chi-Square Test", result_str, inference])

        except Exception as e:
            print(f"• {col1} vs {col2}: skipped (error: {e})")

print("\n► Highly associated categorical pairs:", 
      ", ".join(chi_assoc_pairs) if chi_assoc_pairs else "None")
print("\n")


# # HEATMAP

# In[43]:


print("=== 5. Displaying Correlation Heatmap ===\n")
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", square=True)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()
print("\n")


# # FILING

# In[44]:


# ----- SAVE TO CSV -----
csv_df = pd.DataFrame(csv_results, columns=["Column A", "Column B", "Test", "Result", "Inference"])
csv_path = "testing_results.csv"
csv_df.to_csv(csv_path, index=False)
print(f"Detailed test results written to '{csv_path}'\n")

# ----- WRITE TXT SUMMARY -----
txt_lines = [
    "SUMMARY OF TESTING RESULTS\n",
    "Normal Columns:           " + (", ".join(normal_columns)     if normal_columns     else "None"),
    "Non-Normal Columns:       " + (", ".join(non_normal_columns) if non_normal_columns else "None"),
    "Columns with Outliers:    " + (", ".join(outlier_columns)    if outlier_columns    else "None"),
    "Strongly Correlated Pairs:" + (", ".join(strong_corr_pairs)  if strong_corr_pairs  else "None"),
    "Chi-Square Associated Pairs:" + (", ".join(chi_assoc_pairs)  if chi_assoc_pairs   else "None")
]

txt_path = "testing_summary.txt"
with open(txt_path, "w") as f:
    f.write("\n".join(txt_lines))

print(f"Summary of key results written to '{txt_path}'\n")


# # Last Execution

# In[45]:


get_current_datetime()


# In[46]:


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

