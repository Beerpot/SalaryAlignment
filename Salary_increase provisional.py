import random
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import csv
import matplotlib.pyplot as plt 

People = pd.read_csv('Salary.csv')

Salary = pd.DataFrame()
YearsOfExperience = pd.DataFrame()
SalaryRange = pd.DataFrame()
Temp_ = People
Temp_['Available_Budget_Salary_Alignment'] = pd.DataFrame(np.zeros(len(Temp_.iloc[:,0])))
Temp_['Available_Budget_Salary_increase'] = pd.DataFrame(np.zeros(len(Temp_.iloc[:,0])))

StartingYear = 2021

Salary[str(StartingYear)] = People['Salary']
YearsOfExperience[str(StartingYear)] = People['yrs of experience']
SalaryRange[str(StartingYear)] = People['Salary Range']

#print(SalaryRange)
# number of provisional years is chose : 5
for i in range(5):
    Temp_["err"] = Temp_["Salary Range"] - Temp_["Salary"]

    # err_YOE is implementing the years of experience into the equation integrating the err with years of experience.
    Temp_["err_YOE"] = Temp_["err"] * Temp_["yrs of experience"]

    Norm_factor = max(abs(min(Temp_["err"])), abs(max(Temp_["err"])))
    Norm_factor_YOE = max(abs(min(Temp_["err_YOE"])), abs(max(Temp_["err_YOE"])))
    # Both err and err_YOE normalized based on the maximum value
    Temp_["Normalize Err"] = Temp_["err"]/Norm_factor
    Temp_["Normalize Err_YOE"] = Temp_["err_YOE"]/Norm_factor_YOE

    # People with actual salaries larger/ equal than the set value are named as overcompansated 
    # People with actual salaries lower / equal than the set value are named as undercompansated 

    OverCompansated = Temp_.loc[Temp_["Normalize Err_YOE"]<=0.1]
    UnderCompansated = Temp_.loc[Temp_["Normalize Err_YOE"]>0.1]
    SumError = sum(UnderCompansated["Normalize Err_YOE"])
    UnderCompansated["%increase"] = UnderCompansated["Normalize Err_YOE"]/SumError*100

    print(sum(UnderCompansated["%increase"]))

    # Available Budget 200kEuro
    Available_Budget = 200000
    Available_Budget_Salary_Alignment = Available_Budget * len(UnderCompansated) / len(Temp_["Normalize Err_YOE"])
    Available_Budget_Salary_increase = Available_Budget - Available_Budget_Salary_Alignment

    print('Available_Budget_Salary_Alignment :', Available_Budget_Salary_Alignment, ' Available_Budget_Salary_increase :', Available_Budget_Salary_increase)

    # This year increase by Salary Alignment
    UnderCompansated["Increase Amount"] = UnderCompansated["%increase"] * Available_Budget_Salary_Alignment /100
    print(sum(UnderCompansated["Increase Amount"]))

    # This year increase by the rest
    Increase_Temp = Available_Budget_Salary_increase / len(Temp_["Normalize Err_YOE"])


    # add Salary increase by alignment
    Temp_.loc[UnderCompansated.index, 'Available_Budget_Salary_Alignment'] = UnderCompansated["Increase Amount"]

    # add Salary increase yearly    
    Temp_['Available_Budget_Salary_increase'] = Increase_Temp

    # add Salary increase total

    Temp_['Total Salary increase'] = Temp_['Available_Budget_Salary_increase'] + Temp_['Available_Budget_Salary_Alignment']

    Temp_['new Salary'] = Temp_['Total Salary increase'] + Temp_['Salary']
    

    # Save Data
    file = str(StartingYear)+".csv"
    Temp_.to_csv(file , index=False)
    
    # Reset Temp for the new calculation
    Temp_['Salary'] = Temp_['new Salary']
    Temp_["yrs of experience"] = Temp_["yrs of experience"] + 1 

    for col in Temp_.columns:
        if col in ['Salary', 'yrs of experience', 'Salary Range']:
            pass
        else:
            Temp_[col].values[:] = 0
    
    StartingYear += 1
    Salary[str(StartingYear)] = Temp_['Salary'] 
    #print(Temp_.head())

Salary.to_csv("ProvisionalSalary.csv" , index=False)

print(Salary.head())