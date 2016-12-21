

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines


def Load_results1(instance):
    '''
    This function loads the results that depend of the periods in to a dataframe and creates a excel file with it.
    
    :param instance: The instance of the project resolution created by PYOMO.
    
    :return: A dataframe called Time_series with the values of the variables that depend of the periods.    
    '''
    
    # Load the variables that depend of the periods in python dyctionarys a
    ab = instance.Diesel_Consume.get_values()
    ac = instance.Lost_Load.get_values()
    ad = instance.Total_Energy_PV.get_values()
    ae = instance.Generator_Energy.get_values()
    af = instance.Energy_Battery_Flow_Out.get_values() 
    ag = instance.Energy_Battery_Flow_In.get_values()
    ai = instance.Energy_Curtailment.get_values()
    aj = instance.Energy_Demand.values()
    ak = instance.State_Of_Charge_Battery.get_values()
    # Trasform Wh to kwh
    #foo = len(ac) + 1
    #for x in range(1,foo):ac[x]/=1000.0
    #for x in range(1,foo):ad[x]/=1000.0
    #for x in range(1,foo):ae[x]/=1000.0
    #for x in range(1,foo):af[x]/=1000.0
    #for x in range(1,foo):ag[x]/=1000.0
    #for x in range(1,foo):ai[x]/=1000.0
    #aj[:] = [x/1000 for x in aj]
    #for x in range(1,foo):ak[x]/=1000.0
    
     # Creation of an index starting in the 'model.StartDate' value with a frequency step equal to 'model.Delta_Time'
    if instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1.0) : # if the step is in hours and minutes
        foo = str(instance.Delta_Time()) # trasform the number into a string
        hour = foo[0] # Extract the first character
        minutes = str(int(float(foo[1:3])*60)) # Extrac the last two character
        index_values = pd.DatetimeIndex(start=instance.StartDate(), periods=instance.t(), freq=(hour + 'h'+ minutes + 'min')) # Creation of an index with a start date and a frequency
    elif instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1): # if the step is in hours
        index_values = pd.DatetimeIndex(start=instance.StartDate(), periods=instance.Periods(), freq=(str(instance.Delta_Time()) + 'h')) # Creation of an index with a start date and a frequency
    else: # if the step is in minutes
        index_values = pd.DatetimeIndex(start=instance.StartDate(), periods=instance.t(), freq=(str(int(instance.Delta_Time()*60)) + 'min'))# Creation of an index with a start date and a frequency
    
    data = np.array([ab.values(), ac.values(), ad.values(), ai.values(), ae.values(), af.values(), ag.values(), aj, ak.values()]) # Loading the values to a numpy array
    Time_Series = pd.DataFrame(data.transpose(),columns=['Consume diesel', 'Lost Load', 'Energy PV','Curtailment ','Energy Diesel', 'Discharge energy from the Battery', 'Charge energy to the Battery', 'Energy_Demand',  'State_Of_Charge_Battery'  ],index=index_values)
    Time_Series.to_excel('Results/Time_Series.xls') # Creating an excel file with the values of the variables that are in function of the periods
    return Time_Series
    
    
    
def Load_results2(instance):
    '''
    This function extracts the unidimensional variables into a  data frame and creates a excel file with it.
    this data
    
    :param instance: The instance of the project resolution created by PYOMO. 
    
    :return: Data frame called Size_variables with the variables values. 
    '''
    # Load the variables that doesnot depend of the periods in python dyctionarys
    ca = instance.Cost_Financial.get_values()
    cb = instance.PV_Units.get_values()
    cc = instance.Battery_Nominal_Capacity.get_values()
    cd = instance.Generator_Nominal_Capacity.get_values() 
    NPC = [instance.ObjectiveFuntion.expr()]
    data3 = np.array([ca.values(), cb.values(), cc.values(), cd.values(), NPC]) # Loading the values to a numpy array
    # Create a data frame for the variable that don't depend of the periods of analisys 
    Size_variables = pd.DataFrame(data3.transpose(),columns=['Amortization', 'Size of the solar panels', 'Size of the Battery', 'Size of the diesel generator', 'Net Present Cost'])
    Size_variables.to_excel('Results/Size.xls') # Creating an excel file with the values of the variables that does not depend of the periods
    return Size_variables
   
    
    
    
def Plot_Energy_Total(instance, Time_Series):  
    '''
    This function creates a plot of the dispatch of energy of a defined number of days.
    
    :param instance: The instance of the project resolution created by PYOMO. 
    :param Time_series: The results of the optimization model that depend of the periods.
    
    
    '''
    Periods_Day = 24/instance.Delta_Time() # periods in a day
    for x in range(1, instance.Periods()): # Find the position form wich the plot will start in the Time_Series dataframe
        foo = pd.DatetimeIndex(start=instance.PlotDay(),periods=1,freq='1h') # Asign the start date of the graphic to a dumb variable
        if foo == Time_Series.index[x]: 
           Start_Plot = x # asign the value of x to the position where the plot will start 
    End_Plot = Start_Plot + instance.PlotTime()*Periods_Day # Create the end of the plot position inside the time_series
    Plot_Data = Time_Series[Start_Plot:End_Plot] # Extract the data between the start and end position from the Time_Series
    
    Vec = pd.Series(Plot_Data['Energy PV'].values + Plot_Data['Energy Diesel'].values - Plot_Data['Curtailment '].values - Plot_Data['Charge energy to the Battery'].values , index=Plot_Data.index) # Create a vector with the sum of the diesel and solar energy
    Vec2 = pd.Series(Plot_Data['Energy_Demand'].values + Plot_Data['Curtailment '].values + Plot_Data['Charge energy to the Battery'].values, index=Plot_Data.index ) # Solar super plus of energy
    
    Vec3 = pd.Series(Vec.values + Plot_Data['Discharge energy from the Battery'].values, index=Plot_Data.index) # Substracction between the demand and energy discharge from the battery 
    Vec4 = -Plot_Data['Charge energy to the Battery'] # Creating a vector with the negative values of the energy going to the battery 
    Vec5 = pd.Series(Plot_Data['Energy_Demand'].values - Plot_Data['Lost Load'].values, index=Plot_Data.index)    
    
    ax1= Vec.plot(style='b-', linewidth=0.5) # Plot the line of the diesel energy plus the PV energy
    ax1.fill_between(Plot_Data.index.values, Plot_Data['Energy Diesel'].values, Vec.values,   alpha=0.3, color = 'b') # Fill the are of the energy produce by the energy of the PV
    ax2= Plot_Data['Energy Diesel'].plot(style='r', linewidth=0.5) # Plot the line of the diesel energy
    ax2.fill_between(Plot_Data.index.values, Plot_Data['Energy Diesel'].min(), Plot_Data['Energy Diesel'].values, alpha=0.2, color='r') # Fill the area of the energy produce by the diesel generator
    ax3= Plot_Data.Energy_Demand.plot(style='k-',linewidth=1) # Plot the line of the Energy_Demand
    ax3.fill_between(Plot_Data.index.values, Vec.values , Vec3.values, alpha=0.3, color='g') # Fill the area of the energy flowing out the battery
    ax5= Vec4.plot(style='m', linewidth=0.5) # Plot the line of the energy flowing into the battery
    ax5.fill_between(Plot_Data.index.values, 0, Vec4, alpha=0.3, color='m') # Fill the area of the energy flowing into the battery
    ax6= Plot_Data['State_Of_Charge_Battery'].plot(style='k--', secondary_y=True, linewidth=2, alpha=0.7 ) # Plot the line of the State of charge of the battery
    ax7= Vec2.plot(style='b-', linewidth=0.5) # Plot the line of PV energy that exceeds the demand
    ax7.fill_between(Plot_Data.index.values, Plot_Data['Energy_Demand'].values, Vec2.values,  alpha=0.3, color = 'b') # Fill the area between the demand and the curtailment energy
    ax3.fill_between(Plot_Data.index.values, Vec5 , Plot_Data['Energy_Demand'].values, alpha=0.3, color='y') 
    
    # Define name  and units of the axis
    ax1.set_ylabel('Power (W)')
    ax1.set_xlabel('Time (Hours)')
    ax6.set_ylabel('Battery State of charge (Wh)')
    
    # Define the legends of the plot
    From_PV = mpatches.Patch(color='blue',alpha=0.3, label='From PV')
    From_Generator = mpatches.Patch(color='red',alpha=0.3, label='From Generator')
    From_Battery = mpatches.Patch(color='green',alpha=0.5, label='From Battery')
    To_Battery = mpatches.Patch(color='magenta',alpha=0.5, label='To Battery')
    Lost_Load = mpatches.Patch(color='yellow', alpha= 0.3, label= 'Lost Load')
    Energy_Demand = mlines.Line2D([], [], color='black',label='Energy_Demand')
    State_Of_Charge_Battery = mlines.Line2D([], [], color='black',label='State_Of_Charge_Battery', linestyle='--',alpha=0.7)
    plt.legend(handles=[From_Generator, From_PV, From_Battery, To_Battery, Lost_Load, Energy_Demand, State_Of_Charge_Battery], bbox_to_anchor=(1.83, 1))
        
    plt.savefig('Results/Energy_Flow.png')
    
    
    