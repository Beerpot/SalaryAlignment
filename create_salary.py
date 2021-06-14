import random
import numpy as np
import pandas as pd
import csv

# creates salaries randomly between defined values size defines the number of people
random_salary = np.random.randint(55000,85000,size=100)
random_salary_range = np.random.randint(75000,85000,size=100)
years_of_experience = np.random.randint(2,15,size=100)

df = pd.DataFrame()

df["Salary"] = random_salary
df["Salary Range"] = random_salary_range
df["yrs of experience"] = years_of_experience
df.to_csv('Salary.csv' , index=False)

