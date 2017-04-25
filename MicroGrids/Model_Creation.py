
from pyomo.environ import  Param, RangeSet, NonNegativeReals, Var
from Initialize import Initialize_years, Initialize_Demand, Initialize_PV_Energy # Import library with initialitation funtions for the parameters


def Model_Creation(model):
    
    '''
    This function creates the instance for the resolution of the optimization in Pyomo.
    
    :param model: Pyomo model as defined in the Micro-Grids library.
    
    '''
    
    # Time parameters
    model.Periods = Param(within=NonNegativeReals) # Number of periods of analysis of the energy variables
    model.Years = Param() # Number of years of the project
    model.StartDate = Param() # Start date of the analisis
    model.PlotTime = Param() # Quantity of days that are going to be plot
    model.PlotDay = Param() # Start day for the plot
    model.PlotScenario = Param()
    model.Scenarios = Param() 
    
    
    #SETS
    model.periods = RangeSet(1, model.Periods) # Creation of a set from 1 to the number of periods in each year
    model.years = RangeSet(1, model.Years) # Creation of a set from 1 to the number of years of the project
    model.scenario = RangeSet(1, model.Scenarios) # Creation of a set from 1 to the numbero scenarios to analized
    
    # PARAMETERS
    
    # Parameters of the PV 
    model.PV_Nominal_Capacity = Param(within=NonNegativeReals) # Nominal capacity of the PV in W/unit
    model.Inverter_Efficiency = Param() # Efficiency of the inverter in %
    model.PV_invesment_Cost = Param(within=NonNegativeReals) # Cost of solar panel in USD/W
    model.PV_Energy_Production = Param(model.scenario, model.periods, within=NonNegativeReals, initialize=Initialize_PV_Energy) # Energy produccion of a solar panel in W
    
    # Parameters of the battery bank
    model.Charge_Battery_Efficiency = Param() # Efficiency of the charge of the battery in  %
    model.Discharge_Battery_Efficiency = Param() # Efficiency of the discharge of the battery in %
    model.Deep_of_Discharge = Param() # Deep of discharge of the battery (Deep_of_Discharge) in %
    model.Maximun_Battery_Charge_Time = Param(within=NonNegativeReals) # Minimun time of charge of the battery in hours
    model.Maximun_Battery_Discharge_Time = Param(within=NonNegativeReals) # Maximun time of discharge of the battery  in hours                     
    model.Battery_Reposition_Time = Param(within=NonNegativeReals) # Period of repocition of the battery in years
    model.Battery_Invesment_Cost = Param(within=NonNegativeReals) # Cost of battery 
    # Parametes of the diesel generator
    model.Generator_Efficiency = Param() # Generator efficiency to trasform heat into electricity %
    model.Low_Heating_Value = Param() # Low heating value of the diesel in W/L
    model.Diesel_Unitary_Cost = Param(within=NonNegativeReals) # Cost of diesel in USD/L
    model.Generator_Invesment_Cost = Param(within=NonNegativeReals) # Cost of the diesel generator
    
        
    # Parameters of the Energy balance                  
    model.Energy_Demand = Param(model.scenario, model.periods, initialize=Initialize_Demand) # Energy Energy_Demand in W 
    model.Lost_Load_Probability = Param(within=NonNegativeReals) # Lost load probability in %
    model.Value_Of_Lost_Load = Param(within=NonNegativeReals) # Value of lost load in USD/W
    
    # Parameters of the proyect
    model.Delta_Time = Param(within=NonNegativeReals) # Time step in hours
    model.Porcentage_Funded = Param(within=NonNegativeReals) # Porcentaje of the total investment that is Porcentage_Porcentage_Funded by a bank or another entity in %
    model.Project_Years = Param(model.years, initialize= Initialize_years) # Years of the project
    model.Maintenance_Operation_Cost_PV = Param(within=NonNegativeReals) # Percentage of the total investment spend in operation and management of solar panels in each period in %                                             
    model.Maintenance_Operation_Cost_Battery = Param(within=NonNegativeReals) # Percentage of the total investment spend in operation and management of solar panels in each period in %
    model.Maintenance_Operation_Cost_Generator = Param(within=NonNegativeReals) # Percentage of the total investment spend in operation and management of solar panels in each period in %
    model.Discount_Rate = Param() # Discount rate of the project in %
    model.Interest_Rate_Loan = Param() # Interest rate of the loan in %
    model.Scenario_Weight = Param(model.scenario, within=NonNegativeReals) #########
    
    # VARIABLES
    
    # Variables associated to the solar panels
    model.PV_Units = Var(within=NonNegativeReals) # Number of units of solar panels
    model.Total_Energy_PV = Var(model.scenario,model.periods, within=NonNegativeReals) # Energy generated for the Pv sistem in Wh
    
    # Variables associated to the battery bank
    model.Battery_Nominal_Capacity = Var(within=NonNegativeReals) # Capacity of the battery bank in Wh
    model.Energy_Battery_Flow_Out = Var(model.scenario, model.periods, within=NonNegativeReals) # Battery discharge energy in wh
    model.Energy_Battery_Flow_In = Var(model.scenario, model.periods, within=NonNegativeReals) # Battery charge energy in wh
    model.State_Of_Charge_Battery = Var(model.scenario, model.periods, within=NonNegativeReals) # State of Charge of the Battery in wh
    model.Maximun_Charge_Power= Var() # Maximun charge power in w
    model.Maximun_Discharge_Power = Var() #Maximun discharge power in w
    
    # Variables associated to the diesel generator
    model.Generator_Nominal_Capacity = Var(within=NonNegativeReals) # Capacity  of the diesel generator in Wh
    model.Diesel_Consume = Var(model.scenario,model.periods, within=NonNegativeReals) # Diesel consumed to produce electric energy in L
    model.Generator_Energy = Var(model.scenario, model.periods, within=NonNegativeReals) # Energy generated for the Diesel generator
    model.Diesel_Cost_Total = Var(model.scenario, within=NonNegativeReals)
    
    
    
    # Varialbles associated to the energy balance
    model.Lost_Load = Var(model.scenario, model.periods, within=NonNegativeReals) # Energy not suply by the system kWh
    model.Energy_Curtailment = Var(model.scenario, model.periods, within=NonNegativeReals) # Curtailment of solar energy in kWh
    model.Scenario_Lost_Load_Cost = Var(model.scenario, within=NonNegativeReals) ####    

    # Variables associated to the project
    model.Cost_Financial = Var(within=NonNegativeReals) # Financial cost of each period in USD
    model.Scenario_Net_Present_Cost = Var(model.scenario, within=NonNegativeReals) ####
    model.Initial_Inversion = Var(within=NonNegativeReals)
    model.Operation_Maintenance_Cost = Var(within=NonNegativeReals)
    model.Total_Finalcial_Cost = Var(within=NonNegativeReals)
    model.Battery_Reposition_Cost = Var(within=NonNegativeReals)
#    model.Lost_Load_Total_Cost = Var(model.scenario, within=NonNegativeReals)
#    




def Model_Creation_binary(model):
    
    '''
    This function creates the instance for the resolution of the optimization in Pyomo.
    The problem is solved by discretizing the efficiency curve of the generators and uses binary variables
    
    :param model: Pyomo model as defined in the Micro-Grids library.
    
    '''
    from pyomo.environ import  Param, RangeSet, NonNegativeReals, Var, Binary, PositiveIntegers
    from Initialize import Initialize_years, Initialize_Demand, Initialize_PV_Energy, Marginal_Cost_Generator, Start_Cost # Import library with initialitation funtions for the parameters
   
    # Time parameters
    model.Periods = Param(within=NonNegativeReals) # Number of periods of analysis of the energy variables
    model.Years = Param() # Number of years of the project
    model.StartDate = Param() # Start date of the analisis
    model.PlotTime = Param() # Quantity of days that are going to be plot
    model.PlotDay = Param() # Start day for the plot
    model.Scenarios = Param()  
    model.PlotScenario = Param()
    #SETS
    model.periods = RangeSet(1, model.Periods) # Creation of a set from 1 to the number of periods in each year
    model.years = RangeSet(1, model.Years) # Creation of a set from 1 to the number of years of the project
    model.Slops = RangeSet(1,2)
    model.scenario = RangeSet(1, model.Scenarios) # Creation of a set from 1 to the numbero scenarios to analized
    
    # PARAMETERS
    
    # Parameters of the PV 
    model.PV_Nominal_Capacity = Param(within=NonNegativeReals) # Nominal capacity of the PV in W/unit
    model.Inverter_Efficiency = Param() # Efficiency of the inverter in %
    model.PV_invesment_Cost = Param(within=NonNegativeReals) # Cost of solar panel in USD/W
    model.PV_Energy_Production = Param(model.scenario, model.periods, within=NonNegativeReals, initialize=Initialize_PV_Energy) # Energy produccion of a solar panel in W
    
    # Parameters of the battery bank
    model.Charge_Battery_Efficiency = Param() # Efficiency of the charge of the battery in  %
    model.Discharge_Battery_Efficiency = Param() # Efficiency of the discharge of the battery in %
    model.Deep_of_Discharge = Param() # Deep of discharge of the battery (Deep_of_Discharge) in %
    model.Maximun_Battery_Charge_Time = Param(within=NonNegativeReals) # Minimun time of charge of the battery in hours
    model.Maximun_Battery_Discharge_Time = Param(within=NonNegativeReals) # Maximun time of discharge of the battery  in hours                     
    model.Battery_Reposition_Time = Param(within=NonNegativeReals) # Period of repocition of the battery in years
    model.Battery_Invesment_Cost = Param(within=NonNegativeReals) # Cost of battery 
    
    # Parametes of the diesel generator
    model.Generator_Effiency = Param(within=NonNegativeReals)
    model.Generator_Min_Out_Put = Param(within=NonNegativeReals)
    model.Generator_Efficiency = Param() # Generator efficiency to trasform heat into electricity %
    model.Low_Heating_Value = Param() # Low heating value of the diesel in W/L
    model.Diesel_Cost = Param(within=NonNegativeReals) # Cost of diesel in USD/L
    model.Generator_Invesment_Cost = Param(within=NonNegativeReals) # Cost of the diesel generator  
    model.Marginal_Cost_Generator = Param(initialize=Marginal_Cost_Generator )
    model.Generator_Nominal_Capacity = Param(within=NonNegativeReals)
    model.Start_Cost_Generator = Param(within=NonNegativeReals, initialize=Start_Cost)
    
    # Parameters of the Energy balance                  
    model.Energy_Demand = Param(model.scenario,model.periods, initialize=Initialize_Demand) # Energy Energy_Demand in W 
    model.Lost_Load_Probability = Param() # Lost load probability in %
    model.Value_Of_Lost_Load = Param(within=NonNegativeReals) # Value of lost load in USD/W
    
    # Parameters of the proyect
    model.Delta_Time = Param(within=NonNegativeReals) # Time step in hours
    model.Porcentage_Funded = Param(within=NonNegativeReals) # Porcentaje of the total investment that is Porcentage_Porcentage_Funded by a bank or another entity in %
    model.Project_Years = Param(model.years, initialize= Initialize_years) # Years of the project
    model.Maintenance_Operation_Cost_PV = Param(within=NonNegativeReals) # Percentage of the total investment spend in operation and management of solar panels in each period in %                                             
    model.Maintenance_Operation_Cost_Battery = Param(within=NonNegativeReals) # Percentage of the total investment spend in operation and management of solar panels in each period in %
    model.Maintenance_Operation_Cost_Generator = Param(within=NonNegativeReals) # Percentage of the total investment spend in operation and management of solar panels in each period in %
    model.Discount_Rate = Param() # Discount rate of the project in %
    model.Interest_Rate_Loan = Param() # Interest rate of the loan in %
    model.Scenario_Weight = Param(model.scenario, within=NonNegativeReals)
    
    # VARIABLES
    
    # Variables associated to the solar panels
    model.PV_Units = Var(within=NonNegativeReals) # Number of units of solar panels
    model.Total_Energy_PV = Var(model.scenario,model.periods, within=NonNegativeReals) # Energy generated for the Pv sistem in Wh
    
    # Variables associated to the battery bank
    model.Battery_Nominal_Capacity = Var(within=NonNegativeReals) # Capacity of the battery bank in Wh
    model.Energy_Battery_Flow_Out = Var(model.scenario,model.periods, within=NonNegativeReals) # Battery discharge energy in wh
    model.Energy_Battery_Flow_In = Var(model.scenario,model.periods, within=NonNegativeReals) # Battery charge energy in wh
    model.State_Of_Charge_Battery = Var(model.scenario,model.periods, within=NonNegativeReals) # State of Charge of the Battery in wh
    model.Maximun_Charge_Power= Var() # Maximun charge power in w
    model.Maximun_Discharge_Power = Var() #Maximun discharge power in w
    
     # Variables associated to the diesel generator
    
    model.Period_Total_Cost_Generator = Var(model.scenario,model.periods, within=NonNegativeReals)    
    model.Period_Cost_Generator_1 = Var(model.scenario,model.periods, within=NonNegativeReals)
    model.Energy_Generator_Total = Var(model.scenario, model.periods, within=NonNegativeReals)
    model.Generator_Energy_1 = Var(model.scenario,model.periods, within=NonNegativeReals)
    model.Binary_generator_1 = Var(model.scenario,model.periods, within=Binary)
    model.Integer_generator = Var(within=PositiveIntegers)
    model.Total_Cost_Generator = Var(model.scenario,within=NonNegativeReals)  
    model.Generator_Total_Period_Energy = Var(model.scenario,model.periods, within=NonNegativeReals)   
    model.Generator_Energy_Integer = Var(model.scenario, model.periods, within=PositiveIntegers)
    model.Last_Energy_Generator = Var(model.scenario, model.periods, within=NonNegativeReals)
    
    # Varialbles associated to the energy balance
    model.Lost_Load = Var(model.scenario,model.periods, within=NonNegativeReals) # Energy not suply by the system kWh
    model.Energy_Curtailment = Var(model.scenario,model.periods, within=NonNegativeReals) # Curtailment of solar energy in kWh
    
    # Variables associated to the project
    model.Cost_Financial = Var(within=NonNegativeReals) # Financial cost of each period in USD
    model.Initial_Inversion = Var(within=NonNegativeReals)
    model.Operation_Maintenance_Cost = Var(within=NonNegativeReals)
    model.Total_Finalcial_Cost = Var(within=NonNegativeReals)
    model.Battery_Reposition_Cost = Var(within=NonNegativeReals)
    model.Scenario_Lost_Load_Cost = Var(model.scenario, within=NonNegativeReals) ####  
    model.Sceneario_Generator_Total_Cost = Var(model.scenario, within=NonNegativeReals)
    model.Scenario_Net_Present_Cost = Var(model.scenario, within=NonNegativeReals)


