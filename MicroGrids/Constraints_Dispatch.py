############################################# Objective funtion ######################################################

def Net_Present_Cost(model): # OBJETIVE FUNTION: MINIMIZE THE NPC FOR THE SISTEM
    '''
    This function computes the Net Present Cost for the life time of the project, taking in account that the 
    cost are fix for each year.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
            # This element of the objective function represent the part of the total investment that is Porcentage_Funded with the the resources of the project owners.  
    return model.Scenario_Lost_Load_Cost + model.Total_Cost_Generator

############################################# Diesel generator constraints ###########################################

def Generator_Bounds_Min_Integer(model,t): # Maximun energy output of the diesel generator
    ''' 
    This constraint ensure that each segment of the generator does not pass a 
    minimun value.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Generator_Nominal_Capacity*model.Generator_Min_Out_Put + (model.Generator_Energy_Integer[t]-1)*model.Generator_Nominal_Capacity <= model.Generator_Total_Period_Energy[t]                                                                                                
                                                                                               
def Generator_Bounds_Max_Integer(model,t): # Maximun energy output of the diesel generator
    ''' 
    This constraint ensure that each segment of the generator does not pass a 
    minimun value.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Generator_Total_Period_Energy[t] <= model.Generator_Nominal_Capacity*model.Generator_Energy_Integer[t]                                                                                                

def Generator_Cost_1_Integer(model,t):
    ''' 
    This constraint calculate the cost of each generator in the time t.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Period_Total_Cost_Generator[t] ==  model.Generator_Energy_Integer[t]*model.Start_Cost_Generator + model.Marginal_Cost_Generator*model.Generator_Total_Period_Energy[t]  

def Energy_Genarator_Energy_Max_Integer(model,t):
    ''' 
    This constraint ensure that the total energy in the generators does not  pass
    a maximun value.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Generator_Total_Period_Energy[t] <= model.Generator_Nominal_Capacity*model.Integer_generator
        
def Total_Cost_Generator_Integer(model):
    ''' 
    This constraint calculated the total cost of the generator
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Total_Cost_Generator == sum(model.Period_Total_Cost_Generator[t] for t in model.periods) 


############################################# Battery constraints ####################################################

def State_of_Charge(model,t): # State of Charge of the battery
    '''
    This constraint calculates the State of charge of the battery (State_Of_Charge) for each period 
    of analysis. The State_Of_Charge is in the period 't' is equal to the State_Of_Charge in period 
    't-1' plus the energy flow into the battery, minus the energy flow out of the battery. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    if t==1: # The state of charge (State_Of_Charge) for the period 0 is equal to the Battery size.
        return model.State_Of_Charge_Battery[t] == model.Battery_Nominal_Capacity*model.Battery_Initial_SOC - model.Energy_Battery_Flow_Out[t]/model.Discharge_Battery_Efficiency + model.Energy_Battery_Flow_In[t]*model.Charge_Battery_Efficiency
    if t>1:  
        return model.State_Of_Charge_Battery[t] == model.State_Of_Charge_Battery[t-1] - model.Energy_Battery_Flow_Out[t]/model.Discharge_Battery_Efficiency + model.Energy_Battery_Flow_In[t]*model.Charge_Battery_Efficiency    

def Maximun_Charge(model, t): # Maximun state of charge of the Battery
    '''
    This constraint keeps the state of charge of the battery equal or under the size of the battery.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.State_Of_Charge_Battery[t] <= model.Battery_Nominal_Capacity

def Minimun_Charge(model, t): # Minimun state of charge
    '''
    This constraint maintains the level of charge of the battery above the deep of discharge.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.State_Of_Charge_Battery[t] >= model.Battery_Nominal_Capacity*model.Deep_of_Discharge

def Max_Bat_in(model, t): # Minimun flow of energy for the charge fase
    '''
    This constraint maintains the energy in to the battery, below the maximum power of charge of the battery.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Energy_Battery_Flow_In[t] <= model.Maximun_Charge_Power*model.Delta_Time

def Max_Bat_out(model, t): #minimun flow of energy for the discharge fase
    '''
    This constraint maintains the energy from the battery, below the maximum power of discharge of the battery.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Energy_Battery_Flow_Out[t] <= model.Maximun_Discharge_Power*model.Delta_Time

############################################# Energy Constraints #####################################################

def Energy_balance(model, t): # Energy balance
    '''
    This constraint ensures the perfect match between the energy energy demand of the 
    system and the differents sources to meet the energy demand.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Energy_Demand[t] == model.Total_Energy_PV[t] + model.Generator_Total_Period_Energy[t] - model.Energy_Battery_Flow_In[t] + model.Energy_Battery_Flow_Out[t] + model.Lost_Load[t] - model.Energy_Curtailment[t]

def Maximun_Lost_Load(model): # Maximum permissible lost load
    '''
    This constraint ensures that the ratio between the lost load and the energy Energy_Demand does not 
    exceeds the value of the permisible lost load. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
   
       
    return model.Lost_Load_Probability >= (sum(model.Lost_Load[t] for t in model.periods)/sum(model.Energy_Demand[t] for t in model.periods))


############################################# Economical Constraints #################################################
  
def Scenario_Lost_Load_Cost(model):
      
    return model.Scenario_Lost_Load_Cost == (sum(model.Lost_Load[t]*model.Value_Of_Lost_Load for t in model.periods))


