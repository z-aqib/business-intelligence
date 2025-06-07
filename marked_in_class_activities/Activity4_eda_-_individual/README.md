# Business Intelligence

**In-Class Activity: Enhanced Statistical Analysis on Sales Dataset**    
**Instructor:** Miss Abeera Tariq    
**Student:** Zuha Aqib (ERP: 26106)    
**Section:** 10AM   

## Objective

This activity was designed to practice **statistical hypothesis testing** and data analysis using Python. The original goal was to explore how various categorical features (like ship mode or product type) impact numerical business metrics such as **Sales** and **Profit**, using statistical methods like **ANOVA**, **Tukey's HSD**, **Chi-Square tests**, and **t-tests**.

## What Was Given

The original script provided by the instructor included:

* Basic **ANOVA** tests to check if sales differ across several categorical groups.
* A few **Tukey HSD** post-hoc tests following ANOVA.
* A couple of **Chi-square tests** between two categorical variables.
* Two **t-tests** between numerical columns (e.g., Sales vs Profit).
* A brief note on **missing values (NaNs)** affecting t-test results.

The script was static and somewhat limited in scope. It did not:

* Test the impact of categorical variables on **Profit**.
* Perform automated or looped analysis.
* Generalize or reuse analysis functions.
* Clean or format Tukey outputs for easier interpretation.
* Provide any correlation heatmap or grouped insights.

## What I Did Differently

Here’s a summary of the enhancements I made to the analysis:

### 1. Extended ANOVA to **Profit**

* **Change:** Added a loop to run ANOVA across all key categorical variables **against Profit** (not just Sales).
* **Why:** To find out which variables significantly influence profit in addition to sales.
* **Impact:** Identified `Order Priority`, `Product Category`, `Sub-Category`, and `Product Container` as significant factors affecting profit.

### 2. Dynamic Tukey Test Function

* **Change:** Created a reusable function `apply_tukey()` for running Tukey's HSD test.
* **Why:** To automate post-ANOVA analysis for profit-related variables.
* **Enhancement:** The function not only prints the Tukey result but also separates and displays:

  * Significant pairs (where null hypothesis was rejected).
  * Non-significant pairs.

### 3. Full Chi-Square Grid Across Categorical Pairs

* **Change:** Used nested loops (`itertools.combinations`) to perform Chi-square tests on **all pairs** of categorical variables.
* **Why:** To discover **any hidden relationships** between groupings (e.g., Customer Segment vs Region).
* **Improvement:** Results were stored in a DataFrame and displayed as a summary with p-values and interpretations.

### 4. Cleaned and Properly Interpreted t-Tests

* **Change:** Identified columns with NaNs and filled them with zeroes to prevent the t-test from breaking.
* **Adjustment:** Focused on meaningful comparisons (e.g., Sales vs Profit), while acknowledging limitations.
* **Insight:** Added explanation that t-tests may not be ideal when comparing continuous variables like sales and profit—**correlation** is more appropriate.

### 5. Added Correlation Heatmap

* **Change:** Created a correlation matrix of all numeric columns and visualized it using a seaborn heatmap.
* **Why:** To identify strong positive or negative correlations between continuous variables.
* **Categorized Findings:** Separated pairs into:

  * High Positive (> 0.5)
  * Medium Positive (0.3–0.5)
  * High Negative (< -0.5)
  * Medium Negative (-0.3 to -0.5)

### 6. Warnings Handling

* **Added:** A small script to suppress common warnings (future, runtime, user).
* **Reason:** To keep output clean during iterative analysis.

## Summary of Key Results

* **ANOVA:** Profit is significantly affected by `Order Priority`, `Product Category`, `Product Sub-Category`, and `Product Container`.
* **Tukey Test:** Post-hoc comparisons revealed exactly which categories within those variables were statistically different in terms of average profit.
* **Chi-Square Tests:** Several significant relationships were found among categorical variables—especially between customer segment, product container, and region.
* **Correlation:**

  * High correlation between **Sales and Profit**, and **Sales and Unit Price**.
  * Moderate correlation between **Profit and Shipping Cost**.
* **T-Test Insight:** Not the best method for comparing Sales and Profit directly due to data type compatibility; correlation is more suitable.

## Skills Demonstrated

* ANOVA modeling with `statsmodels`
* Custom post-hoc Tukey test function
* Chi-squared contingency testing across all variable pairs
* Advanced use of `scipy`, `statsmodels`, `seaborn`, and `matplotlib`
* Data wrangling and handling of NaNs
* Interpretation of p-values and statistical conclusions

## Conclusion

This extended version of the statistical analysis script transformed a simple, static code sample into a dynamic, reusable, and fully interpreted exploratory analysis notebook. By applying a wide range of statistical methods, handling missing data, and summarizing outputs clearly, the analysis now gives richer and more actionable business insights—especially in understanding **what affects profit**, **how categorical factors are associated**, and **how numerical metrics relate to each other**.