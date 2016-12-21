
from pyomo.opt import SolverFactory

from pyomo.environ import Objective, minimize, Constraint
from Constraints import  Net_Present_Cost, Solar_Energy, Maximun_Diesel_Energy, Diesel_Comsuption, State_of_Charge,\
Maximun_Charge, Minimun_Charge, Max_Power_Battery_Charge, Max_Power_Battery_Discharge, Max_Bat_in, Max_Bat_out, \
Financial_Cost, Energy_balance, Maximun_Lost_Load # Import objective funtion and constraints  

def Model_Resolution(model):   
    '''
    This function creates the model and call Pyomo to solve the instance of the proyect 
    
    :param model: Pyomo model as defined in the Model_creation library
    
    :return: The solution inside an object call instance.
    '''
    # OBJETIVE FUNTION:
    model.ObjectiveFuntion = Objective(rule=Net_Present_Cost, sense=minimize)  
    
    # CONSTRAINTS
    #Energy constraints
    model.EnergyBalance = Constraint(model.periods, rule=Energy_balance)  # Energy balance
    model.MaximunLostLoad = Constraint(rule=Maximun_Lost_Load) # Maximum permissible lost load
    # PV constraints
    model.SolarEnergy = Constraint(model.periods, rule=Solar_Energy)  # Energy output of the solar panels
    # Battery constraints
    model.StateOfCharge = Constraint(model.periods, rule=State_of_Charge) # State of Charge of the battery
    model.MaximunCharge = Constraint(model.periods, rule=Maximun_Charge) # Maximun state of charge of the Battery
    model.MinimunCharge = Constraint(model.periods, rule=Minimun_Charge) # Minimun state of charge
    model.MaxPowerBatteryCharge = Constraint(rule=Max_Power_Battery_Charge)  # Max power battery charge constraint
    model.MaxPowerBatteryDischarge = Constraint(rule=Max_Power_Battery_Discharge)    # Max power battery discharge constraint
    model.MaxBatIn = Constraint(model.periods, rule=Max_Bat_in) # Minimun flow of energy for the charge fase
    model.Maxbatout = Constraint(model.periods, rule=Max_Bat_out) #minimun flow of energy for the discharge fase
    # Diesel Generator constraints
    model.MaximunDieselEnergy = Constraint(model.periods, rule=Maximun_Diesel_Energy) # Maximun energy output of the diesel generator
    model.DieselComsuption = Constraint(model.periods, rule=Diesel_Comsuption)    # Diesel comsuption 
    # Financial Constraints
    model.FinancialCost = Constraint(rule=Financial_Cost) # Financial cost
    
    instance = model.create_instance("Example/data.dat") # load parameters       
    opt = SolverFactory('cplex') # Solver use during the optimization    
    results = opt.solve(instance) # Solving a model instance 
    instance.solutions.load_from(results) # Loading solution into instance
    return instance