#!/usr/bin/env python
# coding: utf-8

# In[256]:


#!pip install statsmodels
#!pip install scipy


# In[257]:


#import the libraries
import pandas as pd
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols


# In[258]:


# Read Sales.Dirty.xls
salesdf = pd.read_excel('Sales.xls')


# In[259]:


salesdf.dtypes


# In[260]:


salesdf.shape


# In[261]:


salesdf.head(10)


# ## Anova Tests

# In[262]:


model = ols('Sales ~ C(Q("Order Priority"))', data=salesdf).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print ("\nAnova => Sales - Order Priority")
display(anova_table)


# In[263]:


model = ols('Sales ~ C(Q("Ship Mode"))', data=salesdf).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print ("\nAnova => Sales - Ship Mode")
display(anova_table)


# In[264]:


model = ols('Sales ~ C(Q("Region"))', data=salesdf).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print ("\nAnova => Sales - Region")
display(anova_table)


# In[265]:


model = ols('Sales ~ C(Q("Province"))', data=salesdf).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print ("\nAnova => Sales - Province")
display(anova_table)


# In[266]:


model = ols('Sales ~ C(Q("Customer Segment"))', data=salesdf).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print ("\nAnova => Sales - Customer Segment")
display(anova_table)


# In[267]:


model = ols('Sales ~ C(Q("Product Category"))', data=salesdf).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print ("\nAnova => Sales - Product Category")
display(anova_table)


# In[268]:


model = ols('Sales ~ C(Q("Product Sub-Category"))', data=salesdf).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print ("\nAnova => Sales - Product Sub-Category")
display(anova_table)


# In[269]:


model = ols('Sales ~ C(Q("Product Container"))', data=salesdf).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print ("\nAnova => Sales - Product Container")
display(anova_table)


# ## Tukey Tests

# In[270]:


salesdf['Ship Mode'].unique()


# In[271]:


from statsmodels.stats.multicomp import pairwise_tukeyhsd

tukey = pairwise_tukeyhsd(endog=salesdf['Sales'],
                          groups=salesdf['Ship Mode'],
                          alpha=0.05)

#display results
print(tukey)


# In[272]:


salesdf['Product Category'].unique()


# In[273]:


tukey = pairwise_tukeyhsd(endog=salesdf['Sales'],
                          groups=salesdf['Product Category'],
                          alpha=0.05)

#display results
print(tukey)


# In[274]:


salesdf['Product Sub-Category'].unique()


# In[275]:


salesdf['Product Sub-Category'].nunique()


# In[276]:


tukey = pairwise_tukeyhsd(endog=salesdf['Sales'],
                          groups=salesdf['Product Sub-Category'],
                          alpha=0.05)

#display results
print(tukey)


# In[277]:


tukey = pairwise_tukeyhsd(endog=salesdf['Sales'],
                          groups=salesdf['Product Container'],
                          alpha=0.05)

#display results
print(tukey)


# ## Chi-Squared Tests

# In[278]:


from scipy.stats import chi2_contingency
from scipy.stats import chi2

# count of occurences of all combinations of the 2 columns
data_crosstab = pd.crosstab(salesdf['Customer Segment'], salesdf['Product Category'], 
margins = False) 
print(data_crosstab) 



# In[279]:


stat, p, dof, expected = chi2_contingency(data_crosstab)
print('dof=%d' % dof)
print(expected)

# interpret p-value
alpha = 0.05
print('significance=%.3f, p=%.3f' % (alpha, p))
if p <= alpha:
    print('Dependent (reject H0)')
else:
    print('Independent (fail to reject H0)')


# In[280]:


data_crosstab = pd.crosstab(salesdf['Product Container'], salesdf['Product Category'], 
margins = False) 
print(data_crosstab) 

stat, p, dof, expected = chi2_contingency(data_crosstab)
print('dof=%d' % dof)
print(expected)

# interpret p-value
alpha = 0.05
print('significance=%.3f, p=%.3f' % (alpha, p))
if p <= alpha:
    print('Dependent (reject H0)')
else:
    print('Independent (fail to reject H0)')


# ## t-tests

# In[281]:


salesdf.dtypes


# In[282]:


#Extracts the data types of each column and stores them in a dictionary called types_map. 
#Then select data in numeric format to be kept in a num_columns list. 
# Allows to have the list of all numerical columns

types_map = salesdf.dtypes.to_dict()
num_columns = []
for k,v in types_map.items():
    if np.issubdtype(np.int64, v) or np.issubdtype(np.float64, v):
        num_columns.append(k)

print(num_columns)




# In[283]:


# independent two-sample t-test 
# The t-test is used to determine whether there is a significant difference between the means of these two samples.

t_val, p_val = stats.ttest_ind(salesdf[num_columns[3]], salesdf[num_columns[8]])
print("(Sales,Profit) => t-value=%s, p-value=%s" % (str(t_val), str(p_val)))


# Nans? 
# 
# Possible that one or both of the samples being compared in the t-test contain missing values (NaNs). As a result, the t-test function (stats.ttest_ind) returns NaN values for the t-value and p-value. Attempt to remove the missing values to see the results. Hence, this highlights the importance of DATA WRANGLING before EDA.

# In[284]:


salesdf[num_columns[3]].fillna(0, inplace=True)  # Fill missing values with 0
salesdf[num_columns[8]].fillna(0, inplace=True)

t_val, p_val = stats.ttest_ind(salesdf[num_columns[3]], salesdf[num_columns[8]])
print("(Sales,Profit) => t-value=%s, p-value=%s" % (str(t_val), str(p_val)))


# Comparing 'Sales' and 'Profit' could be more appropriately approached using correlation analysis, such as Pearson correlation coefficient, which measures the linear relationship between two continuous variables.
# 
# Better example here could have been to compare a categorical variable with 2 categories VS Sales. Example, a comparison of gender and sales or if there were 2 categories however, we are limited to the columns available in this dataset. 

# # IN-CLASS SUBMISSION
# Zuha Aqib 26106, 10am Batch

# In[285]:


import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


# ## ANOVA

# In[286]:


variables = ['Order Priority', 'Ship Mode', 'Region', 'Province', 'Customer Segment', 'Product Category', 'Product Sub-Category', 'Product Container']


# In[287]:


for variable in variables:
    model = ols(f'Profit ~ C(Q("{variable}"))', data=salesdf).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    print (f"\nAnova => Profit - {variable}")
    # display(anova_table)

    # Extract the p-value
    p_value = anova_table["PR(>F)"].iloc[0]  # Extracting p-value from ANOVA table

    # Decision based on p-value
    alpha = 0.05
    if p_value < alpha:
        print(f"  P-value ({p_value:.5f}) < 0.05: Reject the null hypothesis. There is a significant effect of '{variable}' on 'Profit'.")
    else:
        print(f"  P-value ({p_value:.5f}) >= 0.05: Fail to reject the null hypothesis. '{variable}' does not significantly affect 'Profit'.")


# so we got to know that profit is affected by order priority, product category, product sub-category, product container. thus we will perform tukey test on these 4

# ## Tukey Test

# In[288]:


def apply_tukey(variable1, variable2):
    from statsmodels.stats.multicomp import pairwise_tukeyhsd

    print(salesdf[variable2].unique(), "\n")

    tukey = pairwise_tukeyhsd(endog=salesdf[variable1],
                            groups=salesdf[variable2],
                            alpha=0.05)

    #display results
    print(tukey)

    # Convert Tukey's results into a DataFrame for easier analysis
    import pandas as pd

    # Convert results into a DataFrame
    tukey_df = pd.DataFrame(data=tukey.summary().data[1:], 
                            columns=tukey.summary().data[0])

    # Extract significant (reject=True) and non-significant (reject=False) pairs
    significant_pairs = list(tukey_df[tukey_df['reject'] == True][['group1', 'group2']].itertuples(index=False, name=None))
    non_significant_pairs = list(tukey_df[tukey_df['reject'] == False][['group1', 'group2']].itertuples(index=False, name=None))

    # Display the lists
    print("\nSignificant Differences (Reject H0):")
    print(significant_pairs)

    print("\nNon-Significant Differences (Fail to Reject H0):")
    print(non_significant_pairs)


# In[289]:


print(salesdf['Profit'].unique())


# In[290]:


apply_tukey('Profit', 'Order Priority')


# In[291]:


apply_tukey('Profit', 'Product Category')


# In[292]:


apply_tukey('Profit', 'Product Sub-Category')


# In[293]:


apply_tukey('Profit', 'Product Container')


# ## CHI-Square

# In[294]:


import itertools
import pandas as pd
import scipy.stats as stats

# Define categorical variables
categorical_vars = [
    "Order Priority", "Ship Mode", "Customer Name", "Province", "Region",
    "Customer Segment", "Product Category", "Product Sub-Category",
    "Product Name", "Product Container"
]

# Iterate over all unique pairs of categorical variables
results = []
alpha = 0.05  # Significance level

for var1, var2 in itertools.combinations(categorical_vars, 2):
    contingency_table = pd.crosstab(salesdf[var1], salesdf[var2])  # Create contingency table
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)  # Chi-Square test

    # Interpretation based on p-value
    if p < alpha:
        interpretation = "Significant association (Reject H0)"
    else:
        interpretation = "No significant association (Fail to Reject H0)"

    # Store results
    results.append((var1, var2, round(chi2, 3), round(p, 3), interpretation))

# Convert results to DataFrame for better display
chi2_results_df = pd.DataFrame(results, columns=["Variable 1", "Variable 2", "Chi-Square", "P-Value", "Conclusion"])

# Display results
chi2_results_df


# ## Correlation Heat Map

# In[295]:


import seaborn as sns
import matplotlib.pyplot as plt

# Compute the correlation matrix (only numeric columns)
corr_matrix = salesdf.corr(numeric_only=True)

# Initialize lists for categorized correlations
high_positive = []
mid_positive = []
high_negative = []
mid_negative = []

# Extract pairs without repetition (upper triangle of the correlation matrix)
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):  # Avoid duplicate pairs
        var1, var2 = corr_matrix.columns[i], corr_matrix.columns[j]
        corr_value = corr_matrix.iloc[i, j]

        if corr_value > 0.5:
            high_positive.append((var1, var2, round(corr_value, 3)))
        elif 0.3 <= corr_value <= 0.5:
            mid_positive.append((var1, var2, round(corr_value, 3)))
        elif corr_value < -0.5:
            high_negative.append((var1, var2, round(corr_value, 3)))
        elif -0.5 <= corr_value <= -0.3:
            mid_negative.append((var1, var2, round(corr_value, 3)))

# Print categorized correlation pairs
print("\nHigh Positive Correlation (>0.5):", high_positive)
print("\nMid Positive Correlation (0.3 - 0.5):", mid_positive)
print("\nHigh Negative Correlation (<-0.5):", high_negative)
print("\nMid Negative Correlation (-0.3 to -0.5):", mid_negative)

# Plot the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Heatmap')
plt.show()


# here we can see two major correlations: sales is affected by profit and unit price, and vice versa. minor coorelations include sales being affected by shipping cost, and product base marigin being affected by shipping cost
