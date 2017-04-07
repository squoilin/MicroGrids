
import pandas as pd

def Initialize_years(model, i):
    '''
    This function returns the value of each year of the project. 
    
    :param model: Pyomo model as defined in the Model_Creation script.
    
    :return: The year i.
    '''    
    return i

Energy_Demand = pd.read_excel('Example/Demand.xls') # open the energy demand file

def Initialize_Demand(model, i, t):
    '''
    This function returns the value of the energy demand from a system for each period of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
        
    :return: The energy demand for the period t.            
    '''
    return float(Energy_Demand[i][t])

PV_Energy = pd.read_excel('Example/PV_Energy.xls') # open the PV energy yield file

def Initialize_PV_Energy(model, i, t):
    '''
    This function returns the value of the energy yield by one PV under the characteristics of the system 
    analysis for each period of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
    
    :return: The energy yield of one PV for the period t.
    '''
    return float(PV_Energy[i][t])
    

def Marginal_Cost_Generator(model,i):
    '''
    Only used in the binary formulation of the problem
    '''
    if i==1:
        if model.Diesel_Generator_Efficiency_1== 0:
            return ((model.Percentage_Load_2/model.Diesel_Generator_Efficiency_2)*(model.Diesel_Cost/model.Low_Heating_Value))/(model.Percentage_Load_2)
        else:    
            return ((model.Percentage_Load_2/model.Diesel_Generator_Efficiency_2 - model.Percentage_Load_1/model.Diesel_Generator_Efficiency_1)*(model.Diesel_Cost/model.Low_Heating_Value))/(model.Percentage_Load_2 - model.Percentage_Load_1)                                                                    
    else:
        return ((model.Percentage_Load_3/model.Diesel_Generator_Efficiency_3 - model.Percentage_Load_2/model.Diesel_Generator_Efficiency_2)*(model.Diesel_Cost/model.Low_Heating_Value))/(model.Percentage_Load_3 - model.Percentage_Load_2)                                                                    

def initialize_Bound_Min(model, i, j):
    '''
    Only used in the binary formulation of the problem
    '''
    if j==1:
        return (model.Generator_Nominal_Capacity)*(i-1)
    
    else:
        return (model.Generator_Nominal_Capacity)*(i-1)+model.Generator_Nominal_Capacity*model.Percentage_Load_2        

def initialize_Bound_Max(model, i, j):
    '''
    Only used in the binary formulation of the problem
    '''
    if j==1:
        return (model.Generator_Nominal_Capacity)*(i-1)+model.Generator_Nominal_Capacity*model.Percentage_Load_2
    
    else:
        return (model.Generator_Nominal_Capacity)*(i)
    

def initialize_Origins(model,i,j):
    '''
    Only used in the binary formulation of the problem
    '''
    if j==1:
        r=i-1
        s=j+1
    elif j==2:
        r=i
        s=j-1
    
       
    if i==1 and j==1:
        return  model.Start_Cost
    elif j==1:
        Power_1=(i-1)*model.Generator_Nominal_Capacity
        return (model.Marginal_Cost_Generator[2]-model.Marginal_Cost_Generator[1])*Power_1 + model.Cost_Origins[r,s] 
    elif j==2: 
        Power_2=(i-1+model.Analysis_Percentage)*model.Generator_Nominal_Capacity
        return (model.Marginal_Cost_Generator[1]-model.Marginal_Cost_Generator[2])*Power_2 + model.Cost_Origins[r,s]