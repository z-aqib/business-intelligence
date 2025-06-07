    #!/usr/bin/env python
    # coding: utf-8

    # In[ ]:


    #!pip install statsmodels
    #!pip install scipy


    # In[ ]:


    #import the libraries
    import pandas as pd
    import numpy as np
    get_ipython().run_line_magic('matplotlib', 'inline')
    from scipy import stats
    import statsmodels.api as sm
    from statsmodels.formula.api import ols


    # In[ ]:


    # Read Sales.Dirty.xls
    salesdf = pd.read_excel('Sales.xls')


    # In[ ]:


    salesdf.dtypes


    # In[ ]:


    salesdf.shape


    # In[ ]:


    salesdf.head(10)


    # ## Anova Tests

    # In[ ]:


    model = ols('Sales ~ C(Q("Order Priority"))', data=salesdf).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print ("\nAnova => Sales - Order Priority")
    display(anova_table)


    # In[ ]:


    model = ols('Sales ~ C(Q("Ship Mode"))', data=salesdf).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print ("\nAnova => Sales - Ship Mode")
    display(anova_table)


    # In[ ]:


    model = ols('Sales ~ C(Q("Region"))', data=salesdf).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print ("\nAnova => Sales - Region")
    display(anova_table)


    # In[ ]:


    model = ols('Sales ~ C(Q("Province"))', data=salesdf).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print ("\nAnova => Sales - Province")
    display(anova_table)


    # In[ ]:


    model = ols('Sales ~ C(Q("Customer Segment"))', data=salesdf).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print ("\nAnova => Sales - Customer Segment")
    display(anova_table)


    # In[ ]:


    model = ols('Sales ~ C(Q("Product Category"))', data=salesdf).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print ("\nAnova => Sales - Product Category")
    display(anova_table)


    # In[ ]:


    model = ols('Sales ~ C(Q("Product Sub-Category"))', data=salesdf).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print ("\nAnova => Sales - Product Sub-Category")
    display(anova_table)


    # In[ ]:


    model = ols('Sales ~ C(Q("Product Container"))', data=salesdf).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print ("\nAnova => Sales - Product Container")
    display(anova_table)


    # ## Tukey Tests

    # In[ ]:


    salesdf['Ship Mode'].unique()


    # In[ ]:


    from statsmodels.stats.multicomp import pairwise_tukeyhsd

    tukey = pairwise_tukeyhsd(endog=salesdf['Sales'],
                            groups=salesdf['Ship Mode'],
                            alpha=0.05)

    #display results
    print(tukey)


    # In[ ]:


    salesdf['Product Category'].unique()


    # In[ ]:


    tukey = pairwise_tukeyhsd(endog=salesdf['Sales'],
                            groups=salesdf['Product Category'],
                            alpha=0.05)

    #display results
    print(tukey)


    # In[ ]:


    salesdf['Product Sub-Category'].unique()


    # In[ ]:


    salesdf['Product Sub-Category'].nunique()


    # In[ ]:


    tukey = pairwise_tukeyhsd(endog=salesdf['Sales'],
                            groups=salesdf['Product Sub-Category'],
                            alpha=0.05)

    #display results
    print(tukey)


    # In[ ]:


    tukey = pairwise_tukeyhsd(endog=salesdf['Sales'],
                            groups=salesdf['Product Container'],
                            alpha=0.05)

    #display results
    print(tukey)


    # ## Chi-Squared Tests

    # In[ ]:


    from scipy.stats import chi2_contingency
    from scipy.stats import chi2

    # count of occurences of all combinations of the 2 columns
    data_crosstab = pd.crosstab(salesdf['Customer Segment'], salesdf['Product Category'], 
    margins = False) 
    print(data_crosstab) 



    # In[ ]:


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


    # In[ ]:


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

    # In[ ]:


    salesdf.dtypes


    # In[ ]:


    #Extracts the data types of each column and stores them in a dictionary called types_map. 
    #Then select data in numeric format to be kept in a num_columns list. 
    # Allows to have the list of all numerical columns

    types_map = salesdf.dtypes.to_dict()
    num_columns = []
    for k,v in types_map.items():
        if np.issubdtype(np.int64, v) or np.issubdtype(np.float64, v):
            num_columns.append(k)

    print(num_columns)




    # In[ ]:


    salesdf.isnull().sum()


    # In[ ]:


    # independent two-sample t-test 
    # The t-test is used to determine whether there is a significant difference between the means of these two samples.

    t_val, p_val = stats.ttest_ind(salesdf[num_columns[3]], salesdf[num_columns[5]])
    print("(Sales,Profit) => t-value=%s, p-value=%s" % (str(t_val), str(p_val)))


    # In[ ]:


    # independent two-sample t-test 
    # The t-test is used to determine whether there is a significant difference between the means of these two samples.

    t_val, p_val = stats.ttest_ind(salesdf[num_columns[3]], salesdf[num_columns[8]])
    print("(Sales,Product Base Margin) => t-value=%s, p-value=%s" % (str(t_val), str(p_val)))


    # Nans? 
    # 
    # Possible that one or both of the samples being compared in the t-test contain missing values (NaNs). As a result, the t-test function (stats.ttest_ind) returns NaN values for the t-value and p-value. Attempt to remove the missing values to see the results. Hence, this highlights the importance of DATA WRANGLING before EDA.

    # In[ ]:


    salesdf[num_columns[3]].fillna(0, inplace=True)  # Fill missing values with 0
    salesdf[num_columns[8]].fillna(0, inplace=True)

    t_val, p_val = stats.ttest_ind(salesdf[num_columns[3]], salesdf[num_columns[8]])
    print("(Sales,Product Base Margin) => t-value=%s, p-value=%s" % (str(t_val), str(p_val)))


    # Comparing 'Sales', 'Profit' or 'Product Base Margin" could be more appropriately approached using correlation analysis, such as Pearson correlation coefficient, which measures the linear relationship between two continuous variables.
    # 
    # Better example here could have been to compare a categorical variable with 2 categories VS Sales. Example, a comparison of gender and sales or if there were 2 categories however, we are limited to the columns available in this dataset. 

    # In[ ]:




