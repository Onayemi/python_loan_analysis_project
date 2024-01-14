# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 09:47:53 2024

@author: REMLEX
"""

# Import Libraries
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

loan_data = pd.read_excel('loandataset.xlsx')
customer_data = pd.read_csv('customer_data.csv', sep=';')

# Display the first few rows of our dataset
print(loan_data.head())
print(customer_data.head())

# =============================================================================
# Joining the two dataset
# =============================================================================

# Merging two DataFrame on id
# Merging to dataframe on id
complete_data = pd.merge(loan_data, customer_data, left_on='customerid', right_on='id')

# Check for missing data
complete_data.isnull().sum()

# Remove the rows with missing data
complete_data = complete_data.dropna()
complete_data.isnull().sum()

# Check for duplicated data
complete_data.duplicated().sum()

# Dropping Duplicates
complete_data = complete_data.drop_duplicates()

# =============================================================================
# Introduction to Function in Python
# =============================================================================

def add_number(number1, number2):
    # Operation 
    sum = number1 + number2
    return sum

result = add_number(10, 15)
print(result)

# Creating function on loan dataset
# Define a function to categorize purpose into broader categories
def categorize_purpose(purpose):
    if purpose in ['credit_card', 'debt_consolidation']:
        return 'Financial'
    elif purpose in ['educational', 'small_business']:
        return 'Educational/Business'
    else:
        return 'Others'
    
categorize_purpose('credit_card')

# =============================================================================
# Apply the function to dataset
# =============================================================================
complete_data['purpose_category'] = complete_data['purpose'].apply(categorize_purpose)

# =============================================================================
# Conditional Statement in Python
# =============================================================================
def check_number(number):
    if number > 0:
        return 'Positive'
    elif number < 0:
        return 'Negative'
    else:
        return 'Zero'
    
result = check_number(0)
print(result)


# =============================================================================
# Create a function based on criteria
# =============================================================================
# Create a function based on criteria
# if the dt1 ratio is more than 20 and the dalinq.2years is greater than 2 and the revol.util > 60 the the borrower is high risk
# use row to determine which column to identify
def assess_risk(row):
    if row['dti'] > 20 and row['delinq.2yrs'] > 2 and row['revol.util'] > 60:
        return 'High Risk'
    else:
        return 'Low Risk'

# apply to each column axis=1 is column
complete_data['Risk'] = complete_data.apply(assess_risk, axis=1)


# Create a new function to categorize FICO scores
# Use column name because of handling only one column
def categorize_fico(fico_score):
    if fico_score >= 800 and fico_score <= 850:
        return 'Excellent'
    elif fico_score >= 740 and fico_score < 800:
        return 'Very Good'
    elif fico_score >= 670 and fico_score < 740:
        return 'Good'
    elif fico_score >= 580 and fico_score < 670:
        return 'Fair'
    else:
        return 'Poor'

complete_data['Fico_category'] = complete_data['fico'].apply(categorize_fico)


# Identity customers with more than average inquiries and deregatory records with a function

# use row to determine which column to identify
def identify_high_inq_derog(row):
    average_inq = complete_data['inq.last.6mths'].mean()
    average_derog = complete_data['pub.rec'].mean()
    if row['inq.last.6mths'] > average_inq and row['pub.rec'] > average_derog:
       return True
    else:
       return False

# Run data in whole dataframe
complete_data['High_Inquiries_and_Public_Records'] = complete_data.apply(identify_high_inq_derog, axis=1)


# =============================================================================
# An Introduction to classes
# =============================================================================

class Person:
        
    # Constructor    
    def __init__(self, name, age):
        # name and age as attribute and self is represent the name store in our class
        self.name = name
        self.age = age
         
    def greet(self):
        return f"Hello, my name is {self.name} and i am {self.age} years old."
    
    def adult(self):
        if self.age >= 18:
            return "I'm an adult."
        else:
            return "I'm not an adult."

# Create an instance of a class
person1 = Person("Samuel", 32)
person1.greet()
person1.adult()

# =============================================================================
# Data analysis class
# =============================================================================
# Creating a data analysis class to calculate summary statistics
class DataAnalysis:
    def __init__(self, df, column_name):
        self.df = df
        self.column_name = column_name
        
    def calculate_mean(self):
        return self.df[self.column_name].mean()
    
    def calculate_sum(self):
        return self.df[self.column_name].sum()

    def calculate_median(self):
        return self.df[self.column_name].median()


analysis = DataAnalysis(complete_data, 'fico')
mean_fico = analysis.calculate_mean()
median_fico = analysis.calculate_median()
sum_fico = analysis.calculate_sum()


# =============================================================================
# Data Visualization in Python
# =============================================================================

# Set the style of our visualization (darkgrid, whitegrid, dark, white) 
sns.set_style('darkgrid')

# Bar plot to show distribution of loans by purpose
# Seaborn palette = 'deep','pastel','dark','muted','bright','colorblind'

plt.figure(figsize=(10,6))
sns.countplot(x = 'purpose', data = complete_data, palette='dark')
# sns.countplot(x = 'purpose', data = complete_data)
plt.title('Loan Purpose Distribution')
plt.xlabel('Purpose of Loans')
plt.ylabel('Number of Loans')
plt.xticks(rotation=45)
plt.show()



# Create a scatterplot for 'dti' vs 'Income'
plt.figure(figsize=(10,6))
sns.scatterplot(x = 'log.annual.inc', y= 'dti', data = complete_data, palette='dark')
plt.title('Debt-to-Income Ratio vs Annual Income')
plt.show()


# Distribution of FICO Scores
plt.figure(figsize=(10,6))
sns.histplot(complete_data['fico'], bins=30, kde=True) # kde=True is drawing line on chart
plt.title('Distribution of FICO Scores')
plt.show()


# Box plot to determine risk vs interest rate
plt.figure(figsize=(10,6))
sns.boxplot(x = 'Risk', y = 'int.rate', data = complete_data)
plt.title('Interest Rate vs Risk')
plt.show()


# Subplot
# Initialize the subplot figure
fig, axs = plt.subplots(2, 2, figsize=(20, 20))

# 1. Loan Purpose Distribution
sns.countplot(x='purpose', data=complete_data, ax=axs[0,0])
axs[0,0].set_title('Loan Purpose Distribution')
plt.setp(axs[0,0].xaxis.get_majorticklabels(), rotation=45)

# 2. Debt-to-Income Ratio vs FICO score
sns.scatterplot(x='fico', y='dti', data=complete_data, ax=axs[0,1])
axs[0,1].set_title('Debt-to-Income Ratio vs FICO score')

# 3. Distribution of FICO Scores
sns.histplot(complete_data['fico'], bins=30, kde=True, ax=axs[1,0])
axs[1,0].set_title('Distribution Rate vs Risk Category')

# 4. Risk category vs Interest Rate
sns.boxplot(x = 'Risk', y = 'int.rate', data=complete_data, ax=axs[1,1])
axs[1,1].set_title('Interest Rate vs. Risk Category')

# Adjust layout for readability
plt.tight_layout()
plt.show()

# =============================================================================
# Exporting Data
# =============================================================================
# Exporting Data
complete_data.to_excel('merge_load_and_customer_vis.xlsx', index=False)

























