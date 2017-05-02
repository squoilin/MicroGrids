from pyomo.environ import  Constraint

############################################# Objective funtion ######################################################

def Net_Present_Cost(model): # OBJETIVE FUNTION: MINIMIZE THE NPC FOR THE SISTEM
    '''
    This function computes the Net Present Cost for the life time of the project, taking in account that the 
    cost are fix for each year.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
            # This element of the objective function represent the part of the total investment that is Porcentage_Funded with the the resources of the project owners.  
    return sum(model.Scenario_Net_Present_Cost[s]*model.Scenario_Weight[s] for s in model.scenario )
############################################# PV constraints #########################################################

def Solar_Energy(model,s,t): # Energy output of the solar panels
    '''
    This constraint calculates the energy produce by the solar panels taking in account the efficiency 
    of the inverter.  
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Total_Energy_PV[s,t] == model.PV_Energy_Production[s,t]*model.Inverter_Efficiency*model.PV_Units

############################################# Diesel generator constraints ###########################################

def Generator_Bounds_Min_binary(model,s,t): # Maximun energy output of the diesel generator
    ''' 
    This constraint ensure that each segment of the generator does not pass a 
    minimun value.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Generator_Nominal_Capacity*model.Generator_Min_Out_Put*model.Binary_generator_1[s,t] <= model.Last_Energy_Generator[s,t]                                                                                                
                                                                                               
def Generator_Bounds_Max_binary(model,s,t): # Maximun energy output of the diesel generator
    ''' 
    This constraint ensure that each segment of the generator does not pass a 
    minimun value.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Last_Energy_Generator[s,t] <= model.Generator_Nominal_Capacity*model.Binary_generator_1[s,t]                                                                                                 

def Generator_Cost_1_binary(model,s,t):
    ''' 
    This constraint calculate the cost of each generator in the time t.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Period_Total_Cost_Generator[s,t] ==  model.Generator_Energy_Integer[s,t]*model.Generator_Nominal_Capacity*model.Marginal_Cost_Generator_1 + model.Marginal_Cost_Generator*model.Last_Energy_Generator[s,t]  + model.Binary_generator_1[s,t]*model.Start_Cost_Generator

def Energy_Genarator_Energy_Max_binary(model,s,t):
    ''' 
    This constraint ensure that the total energy in the generators does not  pass
    a maximun value.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Generator_Total_Period_Energy[s,t] <= model.Generator_Nominal_Capacity*model.Integer_generator
        
def Total_Cost_Generator_binary(model,s):
    ''' 
    This constraint calculated the total cost of the generator
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    Foo=[]
    for r in range(1,model.Periods+1):
        Foo.append((s,r))
    return model.Total_Cost_Generator[s] == sum(model.Period_Total_Cost_Generator[s,t] for s,t in Foo) 

def Generator_Total_Period_Energy_binary(model,s,t):
   ''' 
   This constraint calculated the energy in the period t of the generator.
   :param model: Pyomo model as defined in the Model_creation library.
   '''   
   return model.Generator_Total_Period_Energy[s,t] == model.Generator_Energy_Integer[s,t]*model.Generator_Nominal_Capacity + model.Last_Energy_Generator[s,t]


############################################# Battery constraints ####################################################

def State_of_Charge(model,s,t): # State of Charge of the battery
    '''
    This constraint calculates the State of charge of the battery (State_Of_Charge) for each period 
    of analysis. The State_Of_Charge is in the period 't' is equal to the State_Of_Charge in period 
    't-1' plus the energy flow into the battery, minus the energy flow out of the battery. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    if t==1: # The state of charge (State_Of_Charge) for the period 0 is equal to the Battery size.
        return model.State_Of_Charge_Battery[s,t] == model.Battery_Nominal_Capacity - model.Energy_Battery_Flow_Out[s,t]/model.Discharge_Battery_Efficiency + model.Energy_Battery_Flow_In[s,t]*model.Charge_Battery_Efficiency
    if t>1:  
        return model.State_Of_Charge_Battery[s,t] == model.State_Of_Charge_Battery[s,t-1] - model.Energy_Battery_Flow_Out[s,t]/model.Discharge_Battery_Efficiency + model.Energy_Battery_Flow_In[s,t]*model.Charge_Battery_Efficiency    

def Maximun_Charge(model,s, t): # Maximun state of charge of the Battery
    '''
    This constraint keeps the state of charge of the battery equal or under the size of the battery.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.State_Of_Charge_Battery[s,t] <= model.Battery_Nominal_Capacity

def Minimun_Charge(model,s, t): # Minimun state of charge
    '''
    This constraint maintains the level of charge of the battery above the deep of discharge.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.State_Of_Charge_Battery[s,t] >= model.Battery_Nominal_Capacity*model.Deep_of_Discharge

def Max_Power_Battery_Charge(model): 
    '''
    This constraint calculates the Maximum power of charge of the battery. Taking in account the 
    capacity of the battery and a time frame in which the battery has to be fully loaded.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Maximun_Charge_Power== model.Battery_Nominal_Capacity/model.Maximun_Battery_Charge_Time

def Max_Power_Battery_Discharge(model):
    '''
    This constraint calculates the Maximum power of discharge of the battery. Taking in account 
    the capacity of the battery and a time frame in which the battery can be fully discharge.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Maximun_Discharge_Power == model.Battery_Nominal_Capacity/model.Maximun_Battery_Discharge_Time

def Max_Bat_in(model,s, t): # Minimun flow of energy for the charge fase
    '''
    This constraint maintains the energy in to the battery, below the maximum power of charge of the battery.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Energy_Battery_Flow_In[s,t] <= model.Maximun_Charge_Power*model.Delta_Time

def Max_Bat_out(model,s, t): #minimun flow of energy for the discharge fase
    '''
    This constraint maintains the energy from the battery, below the maximum power of discharge of the battery.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Energy_Battery_Flow_Out[s,t] <= model.Maximun_Discharge_Power*model.Delta_Time

############################################# Energy Constraints #####################################################

def Energy_balance(model,s, t): # Energy balance
    '''
    This constraint ensures the perfect match between the energy energy demand of the 
    system and the differents sources to meet the energy demand.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Energy_Demand[s,t] == model.Total_Energy_PV[s,t] + model.Generator_Total_Period_Energy[s,t] - model.Energy_Battery_Flow_In[s,t] + model.Energy_Battery_Flow_Out[s,t] + model.Lost_Load[s,t] - model.Energy_Curtailment[s,t]

def Maximun_Lost_Load(model,s): # Maximum permissible lost load
    '''
    This constraint ensures that the ratio between the lost load and the energy Energy_Demand does not 
    exceeds the value of the permisible lost load. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    Foo=[]
    for r in range(1,model.Periods+1):
        Foo.append((s,r))
    return model.Lost_Load_Probability >= (sum(model.Lost_Load[s,t] for t in model.periods)/sum(model.Energy_Demand[s,t] for t in model.periods))


############################################# Economical Constraints #################################################

def Financial_Cost(model): 
    '''
    This constraint calculated the yearly payment for the borrow money.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Cost_Financial == ((model.PV_Units*model.PV_invesment_Cost*model.PV_Nominal_Capacity + model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost + model.Generator_Nominal_Capacity*model.Generator_Invesment_Cost*model.Integer_generator)*model.Porcentage_Funded*model.Interest_Rate_Loan)/(1-((1+model.Interest_Rate_Loan)**(-model.Years)))

def Initial_Inversion(model):    
    return model.Initial_Inversion == (model.PV_Units*model.PV_invesment_Cost*model.PV_Nominal_Capacity + model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost + model.Generator_Invesment_Cost*model.Generator_Nominal_Capacity*model.Integer_generator)*(1-model.Porcentage_Funded) 

def Operation_Maintenance_Cost(model):
    return model.Operation_Maintenance_Cost == sum(((model.PV_Units*model.PV_invesment_Cost*model.PV_Nominal_Capacity*model.Maintenance_Operation_Cost_PV 
                                                     + model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost*model.Maintenance_Operation_Cost_Battery
                                                     + model.Generator_Invesment_Cost*model.Generator_Nominal_Capacity*model.Integer_generator*model.Maintenance_Operation_Cost_Generator)/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years)     

def Total_Finalcial_Cost(model):
    return model.Total_Finalcial_Cost == sum((model.Cost_Financial/((1+model.Discount_Rate)**model.Project_Years[y])) for y  in model.years) 
    
def Battery_Reposition_Cost(model):
    return model.Battery_Reposition_Cost == (model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost)/((1+model.Discount_Rate)**model.Battery_Reposition_Time)
    
def Scenario_Lost_Load_Cost(model, s):
    foo=[]
    for f in range(1,model.Periods+1):
        foo.append((s,f))
        
    return model.Scenario_Lost_Load_Cost[s] == sum(((sum(model.Lost_Load[s,t]*model.Value_Of_Lost_Load for s,t in foo))/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years)

def Sceneario_Generator_Total_Cost(model, s):
    
    return model.Sceneario_Generator_Total_Cost[s] == sum(((model.Total_Cost_Generator[s])/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years)

def Scenario_Net_Present_Cost(model, s): # OBJETIVE FUNTION: MINIMIZE THE NPC FOR THE SISTEM
    '''
    This function computes the Net Present Cost for the life time of the project, taking in account that the 
    cost are fix for each year.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
            
    return model.Scenario_Net_Present_Cost[s] == model.Initial_Inversion + model.Operation_Maintenance_Cost + model.Total_Finalcial_Cost + model.Battery_Reposition_Cost + model.Scenario_Lost_Load_Cost[s] + model.Sceneario_Generator_Total_Cost[s]