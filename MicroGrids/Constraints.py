# Objective funtion

def Net_Present_Cost(model): # OBJETIVE FUNTION: MINIMIZE THE NPC FOR THE SISTEM
    '''
    This function computes the sum of the multiplication of the net present cost 
    NPC (USD) of each scenario and their probability of occurrence.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
      
    return sum(model.Scenario_Net_Present_Cost[i]*model.Scenario_Weight[i] for i in model.scenario )
           
##################################################### PV constraints##################################################

def Solar_Energy(model,i, t): # Energy output of the solar panels
    '''
    This constraint calculates the energy produce by the solar panels taking in 
    account the efficiency of the inverter for each scenario.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Total_Energy_PV[i,t] == model.PV_Energy_Production[i,t]*model.Inverter_Efficiency*model.PV_Units


#################################################### Battery constraints #############################################

def State_of_Charge(model,i, t): # State of Charge of the battery
    '''
    This constraint calculates the State of charge of the battery (State_Of_Charge) 
    for each period of analysis. The State_Of_Charge is in the period 't' is equal to
    the State_Of_Charge in period 't-1' plus the energy flow into the battery, 
    minus the energy flow out of the battery. This is done for each scenario i.
    In time t=1 the State_Of_Charge_Battery is equal to a fully charged battery.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    if t==1: # The state of charge (State_Of_Charge) for the period 0 is equal to the Battery size.
        return model.State_Of_Charge_Battery[i,t] == model.Battery_Nominal_Capacity*1 - model.Energy_Battery_Flow_Out[i,t]/model.Discharge_Battery_Efficiency + model.Energy_Battery_Flow_In[i,t]*model.Charge_Battery_Efficiency
    if t>1:  
        return model.State_Of_Charge_Battery[i,t] == model.State_Of_Charge_Battery[i,t-1] - model.Energy_Battery_Flow_Out[i,t]/model.Discharge_Battery_Efficiency + model.Energy_Battery_Flow_In[i,t]*model.Charge_Battery_Efficiency    

def Maximun_Charge(model, i, t): # Maximun state of charge of the Battery
    '''
    This constraint keeps the state of charge of the battery equal or under the 
    size of the battery for each scenario i.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.State_Of_Charge_Battery[i,t] <= model.Battery_Nominal_Capacity

def Minimun_Charge(model,i, t): # Minimun state of charge
    '''
    This constraint maintains the level of charge of the battery above the deep 
    of discharge in each scenario i.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.State_Of_Charge_Battery[i,t] >= model.Battery_Nominal_Capacity*model.Deep_of_Discharge

def Max_Power_Battery_Charge(model): 
    '''
    This constraint calculates the Maximum power of charge of the battery. Taking in account the 
    capacity of the battery and a time frame in which the battery has to be fully loaded for 
    each scenario.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Maximun_Charge_Power== model.Battery_Nominal_Capacity/model.Maximun_Battery_Charge_Time

def Max_Power_Battery_Discharge(model):
    '''
    This constraint calculates the Maximum power of discharge of the battery. for 
    each scenario i.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Maximun_Discharge_Power == model.Battery_Nominal_Capacity/model.Maximun_Battery_Discharge_Time

def Max_Bat_in(model, i, t): # Minimun flow of energy for the charge fase
    '''
    This constraint maintains the energy in to the battery, below the maximum power 
    of charge of the battery for each scenario i.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Energy_Battery_Flow_In[i,t] <= model.Maximun_Charge_Power*model.Delta_Time

def Max_Bat_out(model,i, t): #minimun flow of energy for the discharge fase
    '''
    This constraint maintains the energy from the battery, below the maximum power of 
    discharge of the battery for each scenario i.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Energy_Battery_Flow_Out[i,t] <= model.Maximun_Discharge_Power*model.Delta_Time



############################################## Energy Constraints ##################################################

def Energy_balance(model, i, t): # Energy balance
    '''
    This constraint ensures the perfect match between the energy energy demand of the 
    system and the differents sources to meet the energy demand each scenario i.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Energy_Demand[i,t] == model.Total_Energy_PV[i,t] + model.Generator_Energy[i,t] - model.Energy_Battery_Flow_In[i,t] + model.Energy_Battery_Flow_Out[i,t] + model.Lost_Load[i,t] - model.Energy_Curtailment[i,t]

def Maximun_Lost_Load(model,i): # Maximum permissible lost load
    '''
    This constraint ensures that the ratio between the lost load and the energy 
    Demand does not exceeds the value of the permisible lost load each scenario i. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Lost_Load_Probability >= (sum(model.Lost_Load[i,t] for t in model.periods)/sum(model.Energy_Demand[i,t] for t in model.periods))


######################################## Diesel generator constraints ############################

def Maximun_Diesel_Energy(model,i, t): # Maximun energy output of the diesel generator
    '''
    This constraint ensures that the generator will not exceed his nominal capacity 
    in each period in each scenario i.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Generator_Energy[i,t] <= model.Generator_Nominal_Capacity*model.Delta_Time

def Diesel_Comsuption(model,i, t): # Diesel comsuption 
    '''
    This constraint transforms the energy produce by the diesel generator in to 
    liters of diesel in each scenario i.This is done using the low heating value
    of the diesel and the efficiency of the diesel generator.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Diesel_Consume[i,t] == model.Generator_Energy[i,t]/(model.Generator_Efficiency*model.Low_Heating_Value)


   
    
########################################### Economical Constraints ###################################################

def Financial_Cost(model): 
    '''
    This constraint calculate the yearly payment for the borrow money.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Cost_Financial == ((model.PV_Units*model.PV_invesment_Cost*model.PV_Nominal_Capacity + model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost)*model.Porcentage_Funded*model.Interest_Rate_Loan)/(1-((1+model.Interest_Rate_Loan)**(-model.Years)))

def Diesel_Cost_Total(model,i):
    '''
    This constraint calculate the total cost due to the used of diesel to generate 
    electricity in the generator in each scenario i. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    foo=[]
    for f in range(1,model.Periods+1):
        foo.append((i,f))
    return model.Diesel_Cost_Total[i] == sum(((sum(model.Diesel_Consume[i,t]*model.Diesel_Unitary_Cost for i,t in foo))/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years) 
    
def Scenario_Lost_Load_Cost(model, i):
    '''
    This constraint calculate the cost due to the lost load in each scenario i. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    foo=[]
    for f in range(1,model.Periods+1):
        foo.append((i,f))
        
    return  model.Scenario_Lost_Load_Cost[i] == sum(((sum(model.Lost_Load[i,t]*model.Value_Of_Lost_Load for i,t in foo))/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years) 
 
      
def Initial_Inversion(model):
    '''
    This constraint calculate the initial inversion for the system. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    return model.Initial_Inversion == (model.PV_Units*model.PV_invesment_Cost*model.PV_Nominal_Capacity + model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost + model.Generator_Nominal_Capacity*model.Generator_Invesment_Cost )*(1-model.Porcentage_Funded) 

def Operation_Maintenance_Cost(model):
    '''
    This funtion calculate the operation and maintenance for the system. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    return model.Operation_Maintenance_Cost == sum(((model.PV_Units*model.PV_invesment_Cost*model.PV_Nominal_Capacity*model.Maintenance_Operation_Cost_PV + model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost*model.Maintenance_Operation_Cost_Battery+model.Generator_Nominal_Capacity*model.Generator_Invesment_Cost*model.Maintenance_Operation_Cost_Generator)/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years) 

def Total_Finalcial_Cost(model):
    '''
    This funtion calculate the total financial cost of the system. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    return model.Total_Finalcial_Cost == sum((model.Cost_Financial/((1+model.Discount_Rate)**model.Project_Years[y])) for y  in model.years) 
    
def Battery_Reposition_Cost(model):
    '''
    This funtion calculate the reposition of the battery after a stated time of use. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    ''' 
    return model.Battery_Reposition_Cost == (model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost)/((1+model.Discount_Rate)**model.Battery_Reposition_Time)

def Scenario_Net_Present_Cost(model, i): 
    '''
    This function computes the Net Present Cost for the life time of the project, taking in account that the 
    cost are fix for each year.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''            
    return model.Scenario_Net_Present_Cost[i] == model.Initial_Inversion + model.Operation_Maintenance_Cost + model.Total_Finalcial_Cost + model.Battery_Reposition_Cost + model.Scenario_Lost_Load_Cost[i] + model.Diesel_Cost_Total[i]
                
    
    
