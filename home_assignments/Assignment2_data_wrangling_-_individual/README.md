# Business Intelligence

**Assignment 02: Data Wrangling and Exploratory Data Analysis (EDA)**

**Submitted by:**
**Zuha Aqib (ERP: 26106)**     
**Section:** M/W 10AM – Miss Abeera Tariq     
**Date:** 28th March 2025

---

## Objective

The goal of this assignment was to demonstrate proficiency in data wrangling, cleaning, and exploratory data analysis (EDA) using Python. The task also included handling inconsistencies, treating missing values, performing statistical tests, and optionally creating a reusable API for future data cleaning and analysis workflows. The dataset chosen was related to healthcare, involving patient admission details, billing, and medical records.

---

## Dataset

**Dataset Used:** `Healthcare.csv`
**Source:** Provided via course-approved dataset link
**Context:** The dataset contains synthetic healthcare records including patient demographics, billing information, medical conditions, room details, admission/discharge dates, insurance, and test results.

---

## Assignment Requirements

### Task Breakdown

1. **Dataset Selection** – Choose a relevant dataset from a provided list.
2. **Data Familiarization** – Understand the dataset structure and context.
3. **Data Inconsistencies & Cleaning**

   * Identify and fix inconsistencies and incorrect entries.
   * Clean column names, correct mismatches (e.g., title vs. gender), and remove invalid rows.
4. **Missing Values Handling**

   * Visualize missing values using `missingno`.
   * Define tailored strategies for each column using domain logic.
5. **Univariate Analysis**

   * Analyze numerical and categorical columns via histograms, boxplots, and density plots.
   * Identify outliers using IQR method.
6. **Bivariate & Multivariate Analysis**

   * Use statistical tests: T-test, ANOVA, Chi-squared, Tukey, correlation heatmaps.
7. **Bonus Task (Optional)** – Develop reusable Python API functions for EDA and data cleaning.
8. **AI Usage Disclosure** – Clearly mark where any AI assistance was used.

---

## What Was Done

### Data Cleaning & Inconsistencies

* **Column Name Fixes:** Special characters removed, renamed columns (e.g., '?Name' → 'Name').
* **Name & Gender Check:** Title-based gender correction using logical mapping (`Mr.` → Male, etc.).
* **Standardization:** Lowercased/capitalized values for consistency (e.g., gender, blood types).
* **Error Corrections:**

  * Fixed typos like 'Hypertensions' → 'Hypertension'
  * Standardized entries in columns like Insurance Provider and Test Results
* **Value Validations:**

  * Checked age bounds (0–100), removed invalid or too-short entries
  * Ensured Billing and Tax Amounts were within logical thresholds
  * Validated Admission and Discharge Dates using `datetime`

---

### Missing Value Handling

* **Gender:** Corrected manually using name-based logic
* **Billing Amount:** Row dropped due to lack of approximation
* **Tax Amount:** Filled using average tax percentage (\~15%) derived from valid rows
* **Medication:** Filled using mode of medication given to patients with the same medical condition
* **Room Number:** Imputed based on most frequent room number given to others with the same insurance provider

**Tools Used:** `missingno` for visual diagnostics (matrix, bar, heatmap, dendrogram)

---

### Univariate Analysis

* **Numerical Columns Analyzed:** `Age`, `Billing Amount`, `TaxAmount`, `Room Number`

  * Distribution checked using histograms, boxplots, and density plots
  * No significant outliers found using IQR method
* **Categorical Columns Analyzed:** `Gender`, `Blood Type`, `Medical Condition`, `Admission Type`, `Medication`, `Test Results`

  * Frequencies visualized using count plots
  * Findings:

    * Balanced gender distribution
    * “Penicillin” was the most prescribed medication
    * Most admissions were elective or emergency
    * Higher number of abnormal test results suggests critical patient base

---

### Bivariate & Multivariate Analysis

* **Numerical vs. Numerical:**

  * Correlation heatmap showed strong positive correlation between Billing Amount and Tax Amount (as expected)
* **Numerical vs. Categorical:**

  * **T-test/ANOVA Findings:**

    * Admission Type had a statistically significant effect on Billing Amount
    * Gender, Blood Type, and Medical Condition showed no impact on numerical columns
* **Categorical vs. Categorical:**

  * Chi-squared tests showed no statistically significant associations between categories (e.g., Gender vs. Test Results)

---

## API Development (Bonus Task)

Several reusable functions were created to streamline data wrangling and EDA:

* `api_to_string()`, `api_to_int()`, `api_to_float()`: Type conversion utilities
* `api_remove_small_size_names()`: Drops invalid entries based on string length
* `api_limit_checker()`: Drops numerical outliers outside specified bounds
* `api_to_date_time()`: Converts date columns
* Visualization functions:

  * `api_histogram()`, `api_boxplot()`, `api_density_plot()`, `api_frequency()`
* Statistical helpers:

  * `api_view_outliers()`, `api_numerical_vs_numerical()`, `api_numerical_vs_categorical()`, `api_categorical_vs_categorical()`

---

## Final Results & Insights

* The dataset was successfully cleaned, missing values handled, and all inconsistencies corrected.
* Clear insights were derived about billing trends, admission patterns, and patient demographics.
* No significant associations were found between most categorical variables, but admission type clearly impacts costs.
* The API functions developed will help in future EDA and cleaning projects, ensuring consistency and speed.
* The cleaned dataset was saved as `Healthcare_cleaned.csv`.

---

## AI Usage

Minimal AI usage was applied. ChatGPT was consulted to help structure some API functions and generate example plot code for Tasks 5 & 6. All interpretation, strategy, and logic for Tasks 3 and 4 were done independently.

---

## Submission Contents

* `BI_A2_Zuha_Aqib_26106.ipynb`: Main analysis script
* `Healthcare.csv`: Original dataset
* `Healthcare_cleaned.csv`: Cleaned dataset after wrangling
