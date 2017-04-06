# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.ticker as mtick
import matplotlib.pylab as pylab



def Load_results1(instance):
    '''
    This function loads the results that depend of the periods in to a dataframe and creates a excel file with it.
    
    :param instance: The instance of the project resolution created by PYOMO.
    
    :return: A dataframe called Time_series with the values of the variables that depend of the periods.    
    '''
    
    # Load the variables that depend of the periods in python dyctionarys a
    
    
    Number_Scenarios = int(instance.Scenarios.extract_values()[None])
    Number_Periods = int(instance.Periods.extract_values()[None])
    
    #Scenarios = [[] for i in range(Number_Scenarios)]
    
    columns = []
    for i in range(1, Number_Scenarios+1):
        columns.append('Scenario_'+str(i))

#    columns=columns
    Scenarios = pd.DataFrame()
    
     
    Lost_Load = instance.Lost_Load.get_values()
    PV_Energy = instance.Total_Energy_PV.get_values()
    Battery_Flow_Out = instance.Energy_Battery_Flow_Out.get_values()
    Battery_Flow_in = instance.Energy_Battery_Flow_In.get_values()
    Curtailment = instance.Energy_Curtailment.get_values()
    Energy_Demand = instance.Energy_Demand.extract_values()
    SOC = instance.State_Of_Charge_Battery.get_values()
    Gen_Energy = instance.Generator_Energy.get_values()
    Diesel = instance.Diesel_Consume.get_values()
   
    
    Scenarios_Periods = [[] for i in range(Number_Scenarios)]
    
    for i in range(0,Number_Scenarios):
        for j in range(1, Number_Periods+1):
            Scenarios_Periods[i].append((i+1,j))
    foo=0        
    for i in columns:
        Information = [[] for i in range(9)]
        for j in  Scenarios_Periods[foo]:
            Information[0].append(Lost_Load[j])
            Information[1].append(PV_Energy[j]) 
            Information[2].append(Battery_Flow_Out[j]) 
            Information[3].append(Battery_Flow_in[j]) 
            Information[4].append(Curtailment[j]) 
            Information[5].append(Energy_Demand[j]) 
            Information[6].append(SOC[j])
            Information[7].append(Gen_Energy[j])
            Information[8].append(Diesel[j])
        
        Scenarios=Scenarios.append(Information)
        foo+=1
    
    index=[]  
    for j in range(1, Number_Scenarios+1):   
       index.append('Lost_Load '+str(j))
       index.append('PV_Energy '+str(j))
       index.append('Battery_Flow_Out '+str(j)) 
       index.append('Battery_Flow_in '+str(j))
       index.append('Curtailment '+str(j))
       index.append('Energy_Demand '+str(j))
       index.append('SOC '+str(j))
       index.append('Gen energy '+str(j))
       index.append('Diesel '+str(j))
    Scenarios.index= index
     
    
   
   
     # Creation of an index starting in the 'model.StartDate' value with a frequency step equal to 'model.Delta_Time'
    if instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1.0) : # if the step is in hours and minutes
        foo = str(instance.Delta_Time()) # trasform the number into a string
        hour = foo[0] # Extract the first character
        minutes = str(int(float(foo[1:3])*60)) # Extrac the last two character
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(hour + 'h'+ minutes + 'min')) # Creation of an index with a start date and a frequency
    elif instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1): # if the step is in hours
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(str(instance.Delta_Time()) + 'h')) # Creation of an index with a start date and a frequency
    else: # if the step is in minutes
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(str(int(instance.Delta_Time()*60)) + 'min'))# Creation of an index with a start date and a frequency
    
    Scenarios.columns = columns
    Scenarios = Scenarios.transpose()
    
    Scenarios.to_excel('Results/Time_Series.xls') # Creating an excel file with the values of the variables that are in function of the periods
    
    columns = [] # arreglar varios columns
    for i in range(1, Number_Scenarios+1):
        columns.append('Scenario_'+str(i))
        
    Scenario_information =[[] for i in range(Number_Scenarios)]
    Scenario_NPC = instance.Scenario_Net_Present_Cost.get_values()
    LoL_Cost = instance.Scenario_Lost_Load_Cost.get_values() 
    Scenario_Weight = instance.Scenario_Weight.extract_values()
    Diesel_Cost = instance.Diesel_Cost_Total.get_values()
    
    for i in range(1, Number_Scenarios+1):
        Scenario_information[i-1].append(Scenario_NPC[i])
        Scenario_information[i-1].append(LoL_Cost[i])
        Scenario_information[i-1].append(Scenario_Weight[i])
        Scenario_information[i-1].append(Diesel_Cost[i])
    
    
    Scenario_Information = pd.DataFrame(Scenario_information,index=columns)
    Scenario_Information.columns=['Scenario NPC', 'LoL Cost','Scenario Weight', 'Diesel Cost']
    Scenario_Information = Scenario_Information.transpose()
    
    Scenario_Information.to_excel('Results/Scenario_Information.xls')
    
    return Scenarios
    
    
    
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
    cb=instance.PV_Nominal_Capacity.value*cb[None]
    cc = instance.Battery_Nominal_Capacity.get_values()
    NPC = instance.ObjectiveFuntion.expr()
    Funded= instance.Porcentage_Funded.value
    DiscountRate = instance.Discount_Rate.value
    InterestRate = instance.Interest_Rate_Loan.value
    PricePV = instance.PV_invesment_Cost.value
    PriceBattery= instance.Battery_Invesment_Cost.value
    OM = instance.Maintenance_Operation_Cost_PV.value
    Years=instance.Years.value
    Gen_cap = instance.Generator_Nominal_Capacity.get_values()[None]
    Diesel_Cost = instance.Diesel_Unitary_Cost.value
    Pricegen = instance.Generator_Invesment_Cost.value
    
    Initial_Inversion = instance.Initial_Inversion.get_values()[None]
    O_M_Cost = instance.Operation_Maintenance_Cost.get_values()[None]
    Total_Finalcial_Cost = instance.Total_Finalcial_Cost.get_values()[None]
    Battery_Reposition_Cost = instance.Battery_Reposition_Cost.get_values()[None]
    VOLL = instance.Value_Of_Lost_Load.value
    
    
    
    data3 = np.array([ca[None],cb,cc[None],NPC,Funded, DiscountRate, InterestRate,
                      PricePV, PriceBattery, OM, Years, Initial_Inversion,
                      O_M_Cost, Total_Finalcial_Cost, Battery_Reposition_Cost, VOLL,
                      Gen_cap, Diesel_Cost, Pricegen]) # Loading the values to a numpy array
    index_values = ['Amortization', 'Size of the solar panels', 'Size of the Battery',
                    'NPC','% Financimiento', 'Discount Rate', 'Interest Rate', 
                    'Price PV', 'Price Battery', 'OyM', 'Years', 'Initial Inversion', 
                    'O&M', 'Total Financial Cost','Battery Reposition Cost','VOLL', 
                    'Size Generator', 'Diesel Cost','Price Generator']
    # Create a data frame for the variable that don't depend of the periods of analisys 
    Size_variables = pd.DataFrame(data3,index=index_values)
    Size_variables.to_excel('Results/Size.xls') # Creating an excel file with the values of the variables that does not depend of the periods
    
   
    
    
    
    return Size_variables
   
    
    
    
def Plot_Energy_Total(instance, Time_Serie):  
    '''
    This function creates a plot of the dispatch of energy of a defined number of days.
    
    :param instance: The instance of the project resolution created by PYOMO. 
    :param Time_series: The results of the optimization model that depend of the periods.
    '''
    
    S = instance.PlotScenario.value
    Time_Series = pd.DataFrame(index=range(0,8760))
    Time_Series.index = Time_Serie.index
    
    Time_Series['Lost Load'] = Time_Serie['Lost_Load '+str(S)]
    Time_Series['Energy PV'] = Time_Serie['PV_Energy '+str(S)]
    Time_Series['Discharge energy from the Battery'] = Time_Serie['Battery_Flow_Out '+str(S)] 
    Time_Series['Charge energy to the Battery'] = Time_Serie['Battery_Flow_in '+str(S)]
    Time_Series['Curtailment'] = Time_Serie['Curtailment '+str(S)]
    Time_Series['Energy_Demand'] = Time_Serie['Energy_Demand '+str(S)]
    Time_Series['State_Of_Charge_Battery'] = Time_Serie['SOC '+str(S)]
    Time_Series['Energy Diesel'] = Time_Serie['Gen energy '+str(S)]
    Time_Series['Diesel'] = Time_Serie['Diesel '+str(S)]
    
    
    
    Periods_Day = 24/instance.Delta_Time() # periods in a day
    for x in range(0, instance.Periods()): # Find the position form wich the plot will start in the Time_Series dataframe
        foo = pd.DatetimeIndex(start=instance.PlotDay(),periods=1,freq='1h') # Asign the start date of the graphic to a dumb variable
        if foo == Time_Series.index[x]: 
           Start_Plot = x # asign the value of x to the position where the plot will start 
    End_Plot = Start_Plot + instance.PlotTime()*Periods_Day # Create the end of the plot position inside the time_series
    Time_Series.index=range(1,8761)
    Plot_Data = Time_Series[Start_Plot:int(End_Plot)] # Extract the data between the start and end position from the Time_Series
    columns = pd.DatetimeIndex(start=instance.PlotDay(), periods=instance.PlotTime()*Periods_Day, freq=('1h'))    
    Plot_Data.index=columns

    Vec = pd.Series(Plot_Data['Energy PV'].values + Plot_Data['Energy Diesel'].values - Plot_Data['Curtailment'].values - Plot_Data['Charge energy to the Battery'].values , index=Plot_Data.index) # Create a vector with the sum of the diesel and solar energy
    Vec2 = pd.Series(Plot_Data['Energy_Demand'].values + Plot_Data['Curtailment'].values + Plot_Data['Charge energy to the Battery'].values, index=Plot_Data.index ) # Solar super plus of energy
    
    Vec3 = pd.Series(Vec.values + Plot_Data['Discharge energy from the Battery'].values, index=Plot_Data.index) # Substracction between the demand and energy discharge from the battery 
    Vec4 = -Plot_Data['Charge energy to the Battery'] # Creating a vector with the negative values of the energy going to the battery 
    Vec5 = pd.Series(Plot_Data['Energy_Demand'].values - Plot_Data['Lost Load'].values, index=Plot_Data.index)    
    
    ax1= Vec.plot(style='b-', linewidth=0.5) # Plot the line of the diesel energy plus the PV energy
    ax1.fill_between(Plot_Data.index, Plot_Data['Energy Diesel'].values, Vec.values,   alpha=0.3, color = 'b') # Fill the are of the energy produce by the energy of the PV
    ax2= Plot_Data['Energy Diesel'].plot(style='r', linewidth=0.5) # Plot the line of the diesel energy
    ax2.fill_between(Plot_Data.index, 0, Plot_Data['Energy Diesel'].values, alpha=0.2, color='r') # Fill the area of the energy produce by the diesel generator
    ax3= Plot_Data.Energy_Demand.plot(style='k-',linewidth=1) # Plot the line of the Energy_Demand
    ax3.fill_between(Plot_Data.index, Vec.values , Vec3.values, alpha=0.3, color='g') # Fill the area of the energy flowing out the battery
    ax3.fill_between(Plot_Data.index, Vec5 , Plot_Data['Energy_Demand'].values, alpha=0.3, color='y') 
    ax5= Vec4.plot(style='m', linewidth=0.5) # Plot the line of the energy flowing into the battery
    ax5.fill_between(Plot_Data.index, 0, Vec4, alpha=0.3, color='m') # Fill the area of the energy flowing into the battery
    ax6= Plot_Data['State_Of_Charge_Battery'].plot(style='k--', secondary_y=True, linewidth=2, alpha=0.7 ) # Plot the line of the State of charge of the battery
    ax7= Vec2.plot(style='b-', linewidth=0.5) # Plot the line of PV energy that exceeds the demand
    ax7.fill_between(Plot_Data.index, Plot_Data['Energy_Demand'].values, Vec2.values,  alpha=0.3, color = 'b') # Fill the area between the demand and the curtailment energy
    
    # Define name  and units of the axis
    ax2.set_ylabel('Power (W)')
    ax2.set_xlabel('Time (Hours)')
    ax6.set_ylabel('Battery State of charge (Wh)')
    
    # Define the legends of the plot
    From_PV = mpatches.Patch(color='blue',alpha=0.3, label='From PV')
    
    From_Battery = mpatches.Patch(color='green',alpha=0.5, label='From Battery')
    To_Battery = mpatches.Patch(color='magenta',alpha=0.5, label='To Battery')
    Lost_Load = mpatches.Patch(color='yellow', alpha= 0.3, label= 'Lost Load')
    Energy_Demand = mlines.Line2D([], [], color='black',label='Energy_Demand')
    State_Of_Charge_Battery = mlines.Line2D([], [], color='black',label='State_Of_Charge_Battery', linestyle='--',alpha=0.7)
    plt.legend(handles=[From_PV, From_Battery, To_Battery, Lost_Load, Energy_Demand, State_Of_Charge_Battery], bbox_to_anchor=(1.83, 1))
    plt.savefig('Results/Energy_Dispatch.png', bbox_inches='tight')    
    plt.show()    
    
