# -*- coding: utf-8 -*-


from pyomo.environ import  AbstractModel

from Results import Plot_Energy_Total, Load_results1, Load_results2, Percentage_Of_Use, Energy_Flow, Energy_Participation, LDR 
from Model_Creation import Model_Creation
from Model_Resolution import Model_Resolution
from Economical_Analisis import Levelized_Cost_Of_Energy
import os
#os.environ['PATH']=os.environ['PATH']+':/home/usuario/x86-64_linux'
                                       
# Optimization model
model = AbstractModel() # define type of optimization problem
Model_Creation(model) # Creation of the Sets, parameters and variables.
instance = Model_Resolution(model) # Resolution of the instance

# Post procesing tools

# Upload the resulst from the instance and saving it in excel files
Time_Series = Load_results1(instance) # Extract the results of energy from the instance and save it in a excel file 
Results = Load_results2(instance) # Save results into a excel file

# Plots
Plot_Energy_Total(instance, Time_Series) # Plot the total dispatch of energy
#PercentageOfUse = Percentage_Of_Use(Time_Series) # Plot the percentage of use 
#Energy_Flow = Energy_Flow(Time_Series) # Plot the quantity of energy of each technology analized
#Energy_Participation = Energy_Participation(Energy_Flow)
#LDR(Time_Series)


# Calculation of the Levelized cost of energy
#LCOE = Levelized_Cost_Of_Energy(Time_Series, Results, instance) # Calculate the Levelized Cost of energy for the system analysis

# messages
#print 'Net present cost of the project is ' + str(round((instance.ObjectiveFuntion.expr()/1000000),2)) + ' millons of USD' # Print net present cost of the project 
#print 'The levelized cost of energy of the project is ' + str(round(LCOE, 3)) + ' USD/kWh' # Print the levilez cost of energy

