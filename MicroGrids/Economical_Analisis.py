
def Levelized_Cost_Of_Energy(Time_Series, Results, instance):
    '''
    This function load the results that depend of the periods in to a dataframe
    
    :param instance: The instance of the project resolution created by the PYOMO 
    :param Time_Series: Data frame as define in the Results library
    :param Results: Data frame as define in the Results library
    
    :return: The Levelized cost of energy (LCOE) for the system
    '''
    Total_Year_Demand = sum (Time_Series['Energy_Demand 1'][i] for i in range(0,len(Time_Series))) # Sum all the periods demands
    Net_Present_Energy_Demand = sum (Total_Year_Demand/(1+instance.Discount_Rate())**i for i in range(1,(instance.Years()+1))) # Obtein the Total present demand
    LCOE = (float(Results[0]['NPC'])/Net_Present_Energy_Demand)*1000  # Calculate de levelized cost of energy   
    return LCOE
