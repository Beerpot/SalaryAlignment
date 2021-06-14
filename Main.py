import random
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import csv
import matplotlib.pyplot as plt 

People = pd.read_csv('Salary.csv')
df = People
df['Available_Budget_Salary_Alignment'] = pd.DataFrame(np.zeros(100))
df['Available_Budget_Salary_increase'] = pd.DataFrame(np.zeros(100))

print(df)
# err defines the delta between the actual salary and the expected reach value. 
# Expected reach value can be overall reach value or the maximum. 
# for the sake of this analysis the value has been taken fixed and maximum.

df["err"] = df["Salary Range"] - df["Salary"]

# err_YOE is implementing the years of experience into the equation integrating the err with years of experience.
df["err_YOE"] = df["err"] * df["yrs of experience"]

Norm_factor = max(abs(min(df["err"])), abs(max(df["err"])))
Norm_factor_YOE = max(abs(min(df["err_YOE"])), abs(max(df["err_YOE"])))

# Both err and err_YOE normalized based on the maximum value
df["Normalize Err"] = df["err"]/Norm_factor
df["Normalize Err_YOE"] = df["err_YOE"]/Norm_factor_YOE



# People with actual salaries larger/ equal than the set value are named as overcompansated 
# People with actual salaries lower / equal than the set value are named as undercompansated 

OverCompansated = df.loc[df["Normalize Err_YOE"]<=0.1]
UnderCompansated = df.loc[df["Normalize Err_YOE"]>0.1]

print('UnderCompansated :', len(UnderCompansated),'OverCompansated :', len(OverCompansated))

SumError = sum(UnderCompansated["Normalize Err_YOE"])
UnderCompansated["%increase"] = UnderCompansated["Normalize Err_YOE"]/SumError*100

print(sum(UnderCompansated["%increase"]))

# Available Budget 200kEuro
Available_Budget = 200000
Available_Budget_Salary_Alignment = Available_Budget * len(UnderCompansated) / len(df["Normalize Err_YOE"])
Available_Budget_Salary_increase = Available_Budget - Available_Budget_Salary_Alignment

print('Available_Budget_Salary_Alignment :', Available_Budget_Salary_Alignment, ' Available_Budget_Salary_increase :', Available_Budget_Salary_increase)

# This year increase by Salary Alignment
UnderCompansated["Increase Amount"] = UnderCompansated["%increase"] * Available_Budget_Salary_Alignment /100
print(sum(UnderCompansated["Increase Amount"]))

# This year increase by the rest
Increase_Temp = Available_Budget_Salary_increase / len(df["Normalize Err_YOE"])


# add Salary increase by alignment
df.loc[UnderCompansated.index, 'Available_Budget_Salary_Alignment'] = UnderCompansated["Increase Amount"]

# add Salary increase yearly    
df['Available_Budget_Salary_increase'] = Increase_Temp

# add Salary increase total

df['Total Salary increase'] = df['Available_Budget_Salary_increase'] + df['Available_Budget_Salary_Alignment']

df['new Salary'] = df['Total Salary increase'] + df['Salary']

df.to_csv('new Salary.csv' , index=False)