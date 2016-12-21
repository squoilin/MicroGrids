from pyomo.environ import  AbstractModel

from Results import Plot_Energy_Total, Load_results1, Load_results2
from Model_Creation import Model_Creation
from Model_Resolution import Model_Resolution
from Economical_Analisis import Levelizes_Cost_Of_Energy


model = AbstractModel() # define type of optimization problem
Model_Creation(model) # Creation of the Sets, parameters and variables.
instance = Model_Resolution(model) # Resolution of the instance

Time_Series = Load_results1(instance) # Extract the results of energy from the instance and save it in a excel file 
Results = Load_results2(instance) # Save results into a excel file
Plot_Energy_Total(instance, Time_Series) # Plot the total dispatch of energy
LCOE = Levelizes_Cost_Of_Energy(Time_Series, Results, instance) # Calculate the Levelized Cost of energy for the system analysis
print 'Net present cost of the project is ' + str(round((instance.ObjectiveFuntion.expr()/1000000),2)) + ' millons of USD' # Print net present cost of the project 
print 'The levelized cost of energy of the project is ' + str(round(LCOE, 3)) + ' USD/kWh' # Print the levilez cost of energy