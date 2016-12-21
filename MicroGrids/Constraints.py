# Objective funtion

def Net_Present_Cost(model): # OBJETIVE FUNTION: MINIMIZE THE NPC FOR THE SISTEM
    '''
    This function computes the Net Present Cost for the life time of the project, taking in account that the 
    cost are fix for each year.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
            # This element of the objective function represent the part of the total investment that is Porcentage_Funded with the the resources of the project owners.  
    return ((model.PV_Units*model.PV_invesment_Cost*model.PV_Nominal_Capacity + model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost + model.Generator_Nominal_Capacity*model.Generator_Invesment_Cost)*(1-model.Porcentage_Funded) 
            # This element of the objective function represent the cost for the operation and maintement of the equipment for each period of the life of the project.
            + sum(((model.PV_Units*model.PV_invesment_Cost*model.PV_Nominal_Capacity*model.Maintenance_Operation_Cost_PV + model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost*model.Maintenance_Operation_Cost_Battery + model.Generator_Nominal_Capacity*model.Generator_Invesment_Cost*model.Maintenance_Operation_Cost_Generator)/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years) 
            # This element of the objective function represent the value of the periodical payments for the loan acquired in order to finance part of the total inversion.
            + sum((model.Cost_Financial/((1+model.Discount_Rate)**model.Project_Years[y])) for y  in model.years) 
            # This element of the objective function represent the cost of the replacement of the battery bank after their life time.
            + (model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost)/((1+model.Discount_Rate)**model.Battery_Reposition_Time) 
            # This element of the objective function represent the cost of diesel that is used to generate energy in the diesel generator
            + sum(((sum(model.Diesel_Consume[t]*model.Diesel_Cost for t in model.periods))/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years) 
            # This element of the objective function represent the cost for the Energy_Demand that is not meet during a period.
            + sum(((sum(model.Lost_Load[t]*model.Value_Of_Lost_Load for t in model.periods))/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years)) 

# PV constraints

def Solar_Energy(model, t): # Energy output of the solar panels
    '''
    This constraint calculates the energy produce by the solar panels taking in account the efficiency 
    of the inverter.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Total_Energy_PV[t] == model.PV_Energy_Production[t]*model.Inverter_Efficiency*model.PV_Units

# Diesel generator constraints

def Maximun_Diesel_Energy(model, t): # Maximun energy output of the diesel generator
    '''
    This constraint ensures that the generator will not exceed his nominal capacity in each period.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Generator_Energy[t] <= model.Generator_Nominal_Capacity*model.Delta_Time

def Diesel_Comsuption(model, t): # Diesel comsuption 
    '''
    This constraint transforms the energy produce by the diesel generator in to liters of diesel.This  
    is done using the low heating value of the diesel and the efficiency of the diesel generator.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Diesel_Consume[t] == model.Generator_Energy[t]/(model.Generator_Efficiency*model.Low_Heating_Value)

# Battery constraints

def State_of_Charge(model, t): # State of Charge of the battery
    '''
    This constraint calculates the State of charge of the battery (State_Of_Charge) for each period 
    of analysis. The State_Of_Charge is in the period 't' is equal to the State_Of_Charge in period 
    't-1' plus the energy flow into the battery, minus the energy flow out of the battery. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    if t==1: # The state of charge (State_Of_Charge) for the period 0 is equal to the Battery size.
        return model.State_Of_Charge_Battery[t] == model.Battery_Nominal_Capacity - model.Energy_Battery_Flow_Out[t]/model.Discharge_Battery_Efficiency + model.Energy_Battery_Flow_In[t]*model.Charge_Battery_Efficiency
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

# Energy Constraints

def Energy_balance(model, t): # Energy balance
    '''
    This constraint ensures the perfect match between the energy energy demand of the 
    system and the differents sources to meet the energy demand.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Energy_Demand[t] == model.Total_Energy_PV[t] + model.Generator_Energy[t] - model.Energy_Battery_Flow_In[t] + model.Energy_Battery_Flow_Out[t] + model.Lost_Load[t] - model.Energy_Curtailment[t]

def Maximun_Lost_Load(model): # Maximum permissible lost load
    '''
    This constraint ensures that the ratio between the lost load and the energy Energy_Demand does not 
    exceeds the value of the permisible lost load. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Lost_Load_Probability >= (sum(model.Lost_Load[t] for t in model.periods)/sum(model.Energy_Demand[t] for t in model.periods))

# Economical Constraints

def Financial_Cost(model): 
    '''
    This constraint calculated the yearly payment for the borrow money.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Cost_Financial == ((model.PV_Units*model.PV_invesment_Cost*model.PV_Nominal_Capacity + model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost + model.Generator_Nominal_Capacity*model.Generator_Invesment_Cost)*model.Porcentage_Funded*model.Interest_Rate_Loan)/(1-((1+model.Interest_Rate_Loan)**(-model.Years)))
    
