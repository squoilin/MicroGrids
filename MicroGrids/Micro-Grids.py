# -*- coding: utf-8 -*-

import pandas as pd
from pyomo.environ import  AbstractModel

from Results import Plot_Energy_Total, Load_results1, Load_results2
from Model_Creation import Model_Creation
from Model_Resolution import Model_Resolution
from Economical_Analisis import Levelized_Cost_Of_Energy


# Optimization model
model = AbstractModel() # define type of optimization problem
Model_Creation(model) # Creation of the Sets, parameters and variables.
instance = Model_Resolution(model) # Resolution of the instance

# Post procesing tools

## Upload the resulst from the instance and saving it in excel files
Time_Serie = Load_results1(instance) # Extract the results of energy from the instance and save it in a excel file 
Results = Load_results2(instance) # Save results into a excel file

Plot_Energy_Total(instance, Time_Serie)

### messages
print('Net present cost of the project is ' + str(round((instance.ObjectiveFuntion.expr()/1000000),2)) + ' millons of USD') # Print net present cost of the project 
