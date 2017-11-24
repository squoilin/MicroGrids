# -*- coding: utf-8 -*-

import pandas as pd
from pyomo.environ import  AbstractModel

from Results import Plot_Energy_Total, Load_results1, Load_results2, Load_results1_binary, Load_results2_binary, Percentage_Of_Use, Energy_Flow, Energy_Participation, LDR, Load_results1_Integer, Load_results2_Integer, Load_results1_Dispatch, Load_results2_Dispatch 
from Model_Creation import Model_Creation, Model_Creation_binary, Model_Creation_Integer, Model_Creation_Dispatch
from Model_Resolution import Model_Resolution, Model_Resolution_binary, Model_Resolution_Integer, Model_Resolution_Dispatch
from Economical_Analysis import Levelized_Cost_Of_Energy


# Type of problem formulation:
formulation = 'Dispatch'

model = AbstractModel() # define type of optimization problem

if formulation == 'LP':
    # Optimization model
    Model_Creation(model) # Creation of the Sets, parameters and variables.
    instance = Model_Resolution(model) # Resolution of the instance
    ## Upload the resulst from the instance and saving it in excel files
    Time_Series,Scenarios = Load_results1(instance) # Extract the results of energy from the instance and save it in a excel file 
    Results = Load_results2(instance) # Save results into a excel file
elif formulation == 'Binary':
    Model_Creation_binary(model) # Creation of the Sets, parameters and variables.
    instance = Model_Resolution_binary(model) # Resolution of the instance    
    Time_Series = Load_results1_binary(instance) # Extract the results of energy from the instance and save it in a excel file 
    Results = Load_results2_binary(instance) # Save results into a excel file
elif formulation =='Integer':
    Model_Creation_Integer(model)
    instance = Model_Resolution_Integer(model)
    Time_Series = Load_results1_Integer(instance) # Extract the results of energy from the instance and save it in a excel file 
    Results = Load_results2_Integer(instance)
elif formulation =='Dispatch':
    Model_Creation_Dispatch(model)
    instance = Model_Resolution_Dispatch(model)
    Time_Series = Load_results1_Dispatch(instance) # Extract the results of energy from the instance and save it in a excel file 
    Results = Load_results2_Dispatch(instance)

    
    
# Post procesing tools

#Plot_Energy_Total(instance, Time_Series)

#PercentageOfUse = Percentage_Of_Use(Time_Series) # Plot the percentage of use 
#Energy_Flow = Energy_Flow(Time_Series) # Plot the quantity of energy of each technology analized
#Energy_Participation = Energy_Participation(Energy_Flow)
#LDR(Time_Series)


# Calculation of the Levelized cost of energy
#LCOE = Levelized_Cost_Of_Energy(Time_Series, Results, instance) # Calculate the Levelized Cost of energy for the system analysis

# messages
#print 'Net present cost of the project is ' + str(round((instance.ObjectiveFuntion.expr()/1000000),2)) + ' millons of USD' # Print net present cost of the project 
#print 'The levelized cost of energy of the project is ' + str(round(LCOE, 3)) + ' USD/kWh' # Print the levilez cost of energy
