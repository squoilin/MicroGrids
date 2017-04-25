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
    
    S = instance.PlotScenario.value
    Time_Series = pd.DataFrame(index=range(0,8760))
    Time_Series.index = Scenarios.index
    
    Time_Series['Lost Load'] = Scenarios['Lost_Load '+str(S)]
    Time_Series['Energy PV'] = Scenarios['PV_Energy '+str(S)]
    Time_Series['Discharge energy from the Battery'] = Scenarios['Battery_Flow_Out '+str(S)] 
    Time_Series['Charge energy to the Battery'] = Scenarios['Battery_Flow_in '+str(S)]
    Time_Series['Curtailment'] = Scenarios['Curtailment '+str(S)]
    Time_Series['Energy_Demand'] = Scenarios['Energy_Demand '+str(S)]
    Time_Series['State_Of_Charge_Battery'] = Scenarios['SOC '+str(S)]
    Time_Series['Energy Diesel'] = Scenarios['Gen energy '+str(S)]
    Time_Series['Diesel'] = Scenarios['Diesel '+str(S)]    
    
    return Time_Series,Scenarios
    

    
    
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
   
    
    

def Load_results1_binary(instance):
    '''
    This function loads the results that depend of the periods in to a 
    dataframe and creates a excel file with it.
    
    :param instance: The instance of the project resolution created by PYOMO.
    
    :return: A dataframe called Time_series with the values of the variables 
    that depend of the periods.    
    '''

#      Creation of an index starting in the 'model.StartDate' value with a frequency step equal to 'model.Delta_Time'
   
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
    Gen_Energy_Integer = instance.Generator_Energy_Integer.get_values()
    Gen_Energy_I = {}
    
    for i in range(1,Number_Scenarios+1):
        for j in range(1, Number_Periods+1):
            Gen_Energy_I[i,j]=(Gen_Energy_Integer[i,j]*instance.Generator_Nominal_Capacity.extract_values()[None])        
    
    Last_Generator_Energy = instance.Last_Energy_Generator.get_values()        
    Total_Generator_Energy = instance.Generator_Total_Period_Energy.get_values() 
    Gen_cost = instance.Period_Total_Cost_Generator.get_values()       
    
    Scenarios_Periods = [[] for i in range(Number_Scenarios)]
    
    for i in range(0,Number_Scenarios):
        for j in range(1, Number_Periods+1):
            Scenarios_Periods[i].append((i+1,j))
    foo=0        
    for i in columns:
        Information = [[] for i in range(11)]
        for j in  Scenarios_Periods[foo]:
            Information[0].append(Lost_Load[j])
            Information[1].append(PV_Energy[j]) 
            Information[2].append(Battery_Flow_Out[j]) 
            Information[3].append(Battery_Flow_in[j]) 
            Information[4].append(Curtailment[j]) 
            Information[5].append(Energy_Demand[j]) 
            Information[6].append(SOC[j])
            Information[7].append(Gen_Energy_I[j])
            Information[8].append(Last_Generator_Energy[j])
            Information[9].append(Total_Generator_Energy[j])
            Information[10].append(Gen_cost[j])
        
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
       index.append('Gen energy Integer '+str(j))
       index.append('Last Generator Energy '+str(j))
       index.append('Total Generator Energy '+str(j))
       index.append('Total Cost Generator'+str(j))
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
    Diesel_Cost = instance.Sceneario_Generator_Total_Cost.get_values()
    
    for i in range(1, Number_Scenarios+1):
        Scenario_information[i-1].append(Scenario_NPC[i])
        Scenario_information[i-1].append(LoL_Cost[i])
        Scenario_information[i-1].append(Scenario_Weight[i])
        Scenario_information[i-1].append(Diesel_Cost[i])
    
    
    Scenario_Information = pd.DataFrame(Scenario_information,index=columns)
    Scenario_Information.columns=['Scenario NPC', 'LoL Cost','Scenario Weight', 'Diesel Cost']
    Scenario_Information = Scenario_Information.transpose()
    
    Scenario_Information.to_excel('Results/Scenario_Information.xls')
    
    S = instance.PlotScenario.value
    Time_Series = pd.DataFrame(index=range(0,8760))
    Time_Series.index = Scenarios.index
    
    Time_Series['Lost Load'] = Scenarios['Lost_Load '+str(S)]
    Time_Series['Energy PV'] = Scenarios['PV_Energy '+str(S)]
    Time_Series['Discharge energy from the Battery'] = Scenarios['Battery_Flow_Out '+str(S)] 
    Time_Series['Charge energy to the Battery'] = Scenarios['Battery_Flow_in '+str(S)]
    Time_Series['Curtailment'] = Scenarios['Curtailment '+str(S)]
    Time_Series['Energy_Demand'] = Scenarios['Energy_Demand '+str(S)]
    Time_Series['State_Of_Charge_Battery'] = Scenarios['SOC '+str(S)]
    Time_Series['Gen energy Integer'] = Scenarios['Gen energy Integer '+str(S)]
    Time_Series['Last Generator Energy'] = Scenarios['Last Generator Energy ' +str(j)]    
    Time_Series['Energy Diesel'] = Scenarios['Total Generator Energy '+str(j)]
    
    
    return Time_Series
    
    
    
    
def Load_results2_binary(instance):
    '''
    This function extracts the unidimensional variables into a  data frame 
    and creates a excel file with this data
    
    :param instance: The instance of the project resolution created by PYOMO. 
    
    :return: Data frame called Size_variables with the variables values. 
    '''
    # Load the variables that doesnot depend of the periods in python dyctionarys
    Amortizacion = instance.Cost_Financial.get_values()[None]
    cb = instance.PV_Units.get_values()
    cb = cb.values()
    Size_PV=[list(cb)[0]*instance.PV_Nominal_Capacity.value]
    Size_Bat = instance.Battery_Nominal_Capacity.get_values()[None]
    cd = [instance.Generator_Nominal_Capacity.value] 
    Number_Generators = instance.Integer_generator.get_values()
    Number_Generators = Number_Generators.values()
    Number_Generators=list(Number_Generators)
    cd= Number_Generators[0]*cd[0]
    NPC = instance.ObjectiveFuntion.expr()
    Mge_1 = instance.Marginal_Cost_Generator.value
    Start_Cost = instance.Start_Cost_Generator.value
    Funded= instance.Porcentage_Funded.value
    DiscountRate = instance.Discount_Rate.value
    InterestRate = instance.Interest_Rate_Loan.value
    PricePV = instance.PV_invesment_Cost.value
    PriceBatery= instance.Battery_Invesment_Cost.value
    PriceGenSet= instance.Generator_Invesment_Cost.value
    OM = instance.Maintenance_Operation_Cost_PV.value
    Years=instance.Years.value
    VOLL= instance.Value_Of_Lost_Load.value
    data3 = [Amortizacion, Size_PV[0], Size_Bat, cd ,NPC,Mge_1 , Start_Cost,
            Funded,DiscountRate,InterestRate,PricePV,PriceBatery,
            PriceGenSet,OM,Years,VOLL] # Loading the values to a numpy array  
    Size_variables = pd.DataFrame(data3,index=['Amortization', 'Size of the solar panels', 
                                               'Size of the Battery',
                                               'Nominal Capacity Generator',
                                               'Net Present Cost','Marginal cost', 'Start Cost',
                                               'Funded Porcentage', 
                                               'Discount Rate', 'Interest Rate','Precio PV', 
                                               'Precio Bateria','Precio GenSet','OyM',
                                               'Project years','VOLL'])
    Size_variables.to_excel('Results/Size.xls') # Creating an excel file with the values of the variables that does not depend of the periods
    
    I_Inv = instance.Initial_Inversion.get_values()[None] 
    O_M = instance.Operation_Maintenance_Cost.get_values()[None] 
    Financial_Cost = instance.Total_Finalcial_Cost.get_values()[None] 
    Batt_Reposition = instance.Battery_Reposition_Cost.get_values()[None] 
    
    Data = [I_Inv, O_M, Financial_Cost,Batt_Reposition]
    Value_costs = pd.DataFrame(Data, index=['Initial Inversion', 'O & M',
                                            'Financial Cost', 'Battery reposition'])

    Value_costs.to_excel('Results/Partial Costs.xls')    


    VOLL = instance.Scenario_Lost_Load_Cost.get_values() 
    Scenario_Generator_Cost = instance.Sceneario_Generator_Total_Cost.get_values() 
    NPC_Scenario = instance.Scenario_Net_Present_Cost.get_values() 
    
    columns = ['VOLL', 'Scenario Generator Cost', 'NPC Scenario']
    scenarios= range(1,instance.Scenarios.extract_values()[None]+1)
    Scenario_Costs = pd.DataFrame(columns=columns, index=scenarios)
    
    
    for j in scenarios:
        Scenario_Costs['VOLL'][j]= VOLL[j] 
        Scenario_Costs['Scenario Generator Cost'][j]= Scenario_Generator_Cost[j]
        Scenario_Costs['NPC Scenario'][j]= NPC_Scenario[j]
    Scenario_Costs.to_excel('Results/Scenario Cost.xls')    
    
    return Size_variables

    
def Results_Analysis_3(instance):
    
    data_4 = instance.Generator_Nominal_Capacity.values()
    foo=instance.Binary_generator.get_values()
    for i in range(1,(len(instance.Generator_Nominal_Capacity.values()))+1):
        data_4.append(foo[i])
    data_5 = np.array(data_4)
    
    Generator_info = pd.DataFrame(data_5, index=['Cap 1', 'Cap 2', 'Cap 3', 'Bin 1', 'Bin 2', 'Bin 3'])
    Generator_info.to_excel('Results/Generator.xls')
    
    
def Plot_Energy_Total(instance, Time_Series):  
    '''
    This function creates a plot of the dispatch of energy of a defined number of days.
    
    :param instance: The instance of the project resolution created by PYOMO. 
    :param Time_series: The results of the optimization model that depend of the periods.
    
    
    '''
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
    ax5= Vec4.plot(style='m', linewidth=0.5) # Plot the line of the energy flowing into the battery
    ax5.fill_between(Plot_Data.index, 0, Vec4, alpha=0.3, color='m') # Fill the area of the energy flowing into the battery
    ax6= Plot_Data['State_Of_Charge_Battery'].plot(style='k--', secondary_y=True, linewidth=2, alpha=0.7 ) # Plot the line of the State of charge of the battery
    ax7= Vec2.plot(style='b-', linewidth=0.5) # Plot the line of PV energy that exceeds the demand
    ax7.fill_between(Plot_Data.index, Plot_Data['Energy_Demand'].values, Vec2.values,  alpha=0.3, color = 'b') # Fill the area between the demand and the curtailment energy
    ax3.fill_between(Plot_Data.index, Vec5 , Plot_Data['Energy_Demand'].values, alpha=0.3, color='y') 
    
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
    plt.savefig('Results/Energy_Dispatch.png', bbox_inches='tight')    
    plt.show()    
    
def Percentage_Of_Use(Time_Series):
    '''
    This model creates a plot with the percentage of the time that each technologies is activate during the analized 
    time.
    :param Time_series: The results of the optimization model that depend of the periods.
    '''    
    
    # Creation of the technolgy dictonary    
    PercentageOfUse= {'Lost Load':0, 'Energy PV':0,'Curtailment':0, 'Energy Diesel':0, 'Discharge energy from the Battery':0, 'Charge energy to the Battery':0}
    
    # Count the quantity of times each technology has energy production
    for v in PercentageOfUse.keys():
        foo = 0
        for i in range(len(Time_Series)):
            if Time_Series[v][i]>0: 
                foo = foo + 1      
            PercentageOfUse[v] = (round((foo/float(len(Time_Series))), 3))*100 
    
    # Create the names in the plot
    c = ['From Generator', 'Curtailment', 'To Battery', 'From PV', 'From Battery', 'Lost Load']       
    
#     Create the bar plot  
    plt.figure()
    plt.bar((1,2,3,4,5,6), PercentageOfUse.values(), color= 'b', alpha=0.5, align='center')
   
    plt.xticks((1.2,2.2,3.2,4.2,5.2,6.2), c) # Put the names and position for the ticks in the x axis 
    plt.xticks(rotation=-30) # Rotate the ticks
    plt.xlabel('Technology') # Create a label for the x axis
    plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='on')
    plt.ylabel('Percentage of use (%)') # Create a label for the y axis
    plt.savefig('Results/Percentge_of_Use.png', bbox_inches='tight') # Save the plot 
    plt.show() 
    
    return PercentageOfUse
    
def Energy_Flow(Time_Series):


    Energy_Flow = {'Energy_Demand':0, 'Lost Load':0, 'Energy PV':0,'Curtailment':0, 'Energy Diesel':0, 'Discharge energy from the Battery':0, 'Charge energy to the Battery':0}

    for v in Energy_Flow.keys():
        if v == 'Energy PV':
            Energy_Flow[v] = round((Time_Series[v].sum() - Time_Series['Curtailment'].sum()- Time_Series['Charge energy to the Battery'].sum())/1000000, 2)
        else:
            Energy_Flow[v] = round((Time_Series[v].sum())/1000000, 2)
          
    
    c = ['From Generator', 'To Battery', 'Demand', 'From PV', 'From Battery', 'Curtailment', 'Lost Load']       
    plt.figure()    
    plt.bar((1,2,3,4,5,6,7), Energy_Flow.values(), color= 'b', alpha=0.3, align='center')
    
    plt.xticks((1.2,2.2,3.2,4.2,5.2,6.2,7.2), c)
    plt.xlabel('Technology')
    plt.ylabel('Energy Flow (MWh)')
    plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='on')
    plt.xticks(rotation=-30)
    plt.savefig('Results/Energy_Flow.png', bbox_inches='tight')
    plt.show()    
    
    return Energy_Flow

def Energy_Participation(Energy_Flow):
    
    Energy_Participation = {'Energy PV':0, 'Energy Diesel':0, 'Discharge energy from the Battery':0, 'Lost Load':0}
    c = {'Energy Diesel':'Diesel Generator', 'Discharge energy from the Battery':'Battery', 'Energy PV':'From PV', 'Lost Load':'Lost Load'}       
    labels=[]
    
    for v in Energy_Participation.keys():
        if Energy_Flow[v]/Energy_Flow['Energy_Demand'] >= 0.001:
            Energy_Participation[v] = Energy_Flow[v]/Energy_Flow['Energy_Demand']
            labels.append(c[v])
        else:
            del Energy_Participation[v]
    Colors=['r','c','b','k']
    
    plt.figure()                     
    plt.pie(Energy_Participation.values(), autopct='%1.1f%%', colors=Colors)
    
    Handles = []
    for t in range(len(labels)):
        Handles.append(mpatches.Patch(color=Colors[t], alpha=1, label=labels[t]))
    
    plt.legend(handles=Handles, bbox_to_anchor=(1.4, 1))   
    plt.savefig('Results/Energy_Participation.png', bbox_inches='tight')
    plt.show()
    
    return Energy_Participation

def LDR(Time_Series):

    columns=['Consume diesel', 'Lost Load', 'Energy PV','Curtailment','Energy Diesel', 
             'Discharge energy from the Battery', 'Charge energy to the Battery', 
             'Energy_Demand',  'State_Of_Charge_Battery'  ]
    Sort_Values = Time_Series.sort('Energy_Demand', ascending=False)
    
    index_values = []
    
    for i in range(len(Time_Series)):
        index_values.append((i+1)/float(len(Time_Series))*100)
    
    Sort_Values = pd.DataFrame(Sort_Values.values/1000, columns=columns, index=index_values)
    
    plt.figure() 
    ax = Sort_Values['Energy_Demand'].plot(style='k-',linewidth=1)
    
    fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
    xticks = mtick.FormatStrFormatter(fmt)
    ax.xaxis.set_major_formatter(xticks)
    ax.set_ylabel('Load (kWh)')
    ax.set_xlabel('Percentage (%)')
    
    plt.savefig('Results/LDR.png', bbox_inches='tight')
    plt.show()    
    


