Model Description
=================

Sets
----

==========  ==========  =====================================
Name	    Symbol      Description                       
==========  ==========  =====================================
Years	    n		Year of the project	        
Periods     t		Period that are divided the years 
Scenarios   s           Scenarios analalized
==========  ==========  =====================================

Parameters
----------

Data analysis parameters 
~~~~~~~~~~~~~~~~~~~~~~~~

============  =====  ======================================================
Name	      Unit   Description                       
============  =====  ======================================================
Startdate     Day    Start date of the analysis
PlotTime      Days   Number of days for the plot of energy dispatch
PlotDay	      Day    Start date for the dispatch plot
PlotScenario	     Scenario to be plot 
============  =====  ======================================================

PV parameters
~~~~~~~~~~~~~

==========================   ========  =======================================================
Name	                     Unit      Description                       
==========================   ========  =======================================================
PVNominalCapacity	     W/unit    Nominal capacity of one PV unit
InverterEfficiency	     %         efficiency of the inverter to transform DC energy to AC
PVinvesmentCost              USD/W     Investment Cost to install PV panels
PVEnergyProduction           Wh        The yield of energy of one PV unit in the period (i,t)
==========================   ========  =======================================================

Battery bank parameters
~~~~~~~~~~~~~~~~~~~~~~~~

===============================   ========  ======================================================================
Name	                          Unit      Description                       
===============================   ========  ======================================================================
ChargeBatteryEfficiency           %	    The efficiency of the battery to charge energy
DischargeBatteryEfficiency        %         The efficiency of the battery to discharge energy  
DeepOfDischarge		          %	    Minimum percentage of energy of the nominal capacity of the battery
MaximunBatteryChargeTime          hour      Maximum time to charge from 0 % to a 100 % of energy in the battery
MaximunBatteryDischargeTime       hour      Maximum time to discharge from 100 % to a 0 % of energy in the battery
BatteryInvesmentCost              USD/Wh    Investment cost to install a Wh of batteries
BatteryRepostionTime              Years     Time for the remplacement of the battery
===============================   ========  ======================================================================

Diesel generator parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~

===============================   ========  ======================================================================
Name	                          Unit      Description                       
===============================   ========  ======================================================================
GeneratorEfficiency               %         Generator efficiency to transform heat into electricity
LowHeatingValue                   W/L       Low heating value of the diesel
DieselCost			  USD/L     Diesel cost
GeneratorInvesmentCost            USD/W     Investment cost to install a diesel generator
===============================   ========  ======================================================================

Energy balance parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~

===============================   ========  ======================================================================
Name	                          Unit      Description                       
===============================   ========  ======================================================================
EnergyDemand (s,t)		  W         The total energy demand of the system for each scenario.
LostLoadProbability               %         The percentage of the demand that the micro-grid has to provide
ValueOfLostLoad		          USD/W     The price of the load that is not supply to the system
===============================   ========  ======================================================================

Project parameters
~~~~~~~~~~~~~~~~~~

=====================================  =======  =======================================================================================
Name	                               Unit     Description                       
=====================================  =======  =======================================================================================
Periods	                               Hours    Number of periods of the year
Years	                               Years    Number of years in the project
DeltaTime			       Hours    Time step of the analysis of the energy flow
PorcentageFunded		       %        Percentage of the total investment that is Funded by a bank or another entity
MaintenanceOperationCostPV             %        Percentage of the total investment spend in operation and management of PV 
MaintenanceOperationCostBattery        %        Percentage of the total investment spend in operation and management of the battery 
MaintenanceOperationCostGenerator      %        Percentage of the total investment spend in operation and management of the genset 
DiscountRate                           %        Discount rate of the project
InterestRate                           %        Interest rate of the loan
ProbalityOccurrence	(s)	       %        Probability of occurrence of each scenario	
N				       Years    Years of duration of the project
=====================================  =======  =======================================================================================

Variables
---------

PV variables
~~~~~~~~~~~~

===============================  ========  ================================================================
Name	                         Unit      Description                       
===============================  ========  ================================================================
PVUnits                          unit      Number of installed PV 
TotalEnergyPV (s,t)		 Wh        Energy generated for all the PVs in the system in each scenario
OyMCostPV			 USD	   Cost of the OyM of the PV during the life time of the proyect
===============================  ========  ================================================================

Battery variables
~~~~~~~~~~~~~~~~~

===============================  ========  =====================================================
Name	                         Unit      Description                       
===============================  ========  =====================================================
BatteryNominalCapacity           Wh	   Nominal capacity of the battery bank
EnergyBatteryDischarge (s,t)     Wh        Energy that flows out of the battery in each scenario
EnergyBatteryCharge (s,t)        Wh        Energy that flows in to the battery in each scenario
StateOfChargeBattery (s,t)       Wh        Energy inside the battery in each scenario
MaximunChargePower               W         Maximum charge power
MaximunDischargePower            W         Maximum discharge power
===============================  ========  =====================================================

Diesel generator variables
~~~~~~~~~~~~~~~~~~~~~~~~~~

===============================  ========  ======================================================
Name	                         Unit      Description                       
===============================  ========  ======================================================
GeneratorNominalCapacity         W 	   Nominal capacity of the diesel generator
DieselConsumed (s,t)             L         Diesel consumed to produce energy
GeneratorEnergy (s,t)            Wh        Energy produced by the diesel generator
DieselCostTotal	(s)		 USD       Cost of the diesel during the life time of the project
===============================  ========  ======================================================

Energy balance variables
~~~~~~~~~~~~~~~~~~~~~~~~

===============================  ========  =========================================================
Name	                         Unit      Description                       
===============================  ========  =========================================================
LostLoad (s,t)			 Wh        Energy not supply by the system in each scenario
EnergyCurtailment (s,t)          Wh	   Curtailment of solar energy in each scenario
LostLoadCostTotal (s)		 USD       Cost of the Lost load during the life time of the project
===============================  ========  =========================================================

Project variables
~~~~~~~~~~~~~~~~~~~

===============================  ========  ===============================================================================
Name	                         Unit      Description                       
===============================  ========  ===============================================================================
FinancialCost		         USD       Annual constant payment for the loan adquire to finance the project
ScenarioNetPresentCost		 USD	   Net present cost of each scenario
InitialInversion		 USD       Value of the inital inversion of the project
OyMCost				 USD       Total cost of the Operation and maintenence during the life time of the project
FinancialCostTotal		 USD	   Total cost of the payment for the loan during the life time of the project
BatteryRepositionCost		 USD       Cost for the reposition of the battery
===============================  ========  ===============================================================================


Modeling of the system
-----------------------

Objective function
------------------

The objective function will minimize the sum of the multiplication of the net present cost of each scenario and their probability of occurrence.

.. math::


	Objective Funtion = \sum _s\mathit{ScenarioNetPresentCost}_s  \cdot \mathit{ProbalityOccurrence}_s 	 

The net present cost of each scenario is computed with the following equation:

.. math::

	\mathit{ScenarioNetPresentCost}_s = InitialInversion + OyMCost + FinancialCostTotal 
				
		+ BatteryRepositionCost + \mathit{DieselCostTotal}_s + \mathit{LostLoadCostTotal}_s


The total investment equation is:

.. math:: 

	InitialInversion = (PVinvestmentCost \cdot PVNominalCapacity \cdot PVUnits +BatteryNominalCapacity \cdot BatteryInvestmentCost 
	
	+ GeneratorInvestmentCost \cdot GeneratorNominalCapacity  ) \cdot (1 - PorcentageFunded)


The OyMCost is calculated by the following equation:

.. math::

	OyMCostPV = PVinvesmentCost \cdot PVNominalCapacity \cdot PVUnits \cdot MaintenanceOperationCostPV

.. math::

	OyMCostBattery = BatteryNominalCapacity \cdot BatteryInvesmentCost  \cdot MaintenanceOperationCostBattery

.. math::

	OyMCostGenerator = GeneratorInvesmentCost \cdot GeneratorNominalCapacity  \cdot MaintenanceOperationCostGenerator

.. math:: 

	OyMCost = \sum _n\frac{ OyMCostPV + OyMCostBattery + OyMCostGenerator} {(1 + DiscountRate)^{n}}

The financial cost is a fix amount, that is payed each period to pay the loan acquire to finance a percentage of the initial investment and is calculated with the following equation:

.. math::

	FinancialCost = \frac{INV \cdot PorcentageFunded \cdot InterestRate} {1 - (1 +InterestRate)^{-N}}

The total cost incurred in the lifetime of the project for the financial cost is calculated with equation:

.. math::

	FinancialCostTotal = \sum _n\frac{FinancialCost} {(1+ DiscountRate)^{n}}

The replacement cost is given by the fallowing equation:

.. math::

	\mathit{ReplacementCost}_{10} = \frac{BatteryNominalCapacity \cdot BatteryInvesmentCost} {(1+ DiscountRate)^{N}}

The Diesel cost is calculated by:

.. math::

	\mathit{DieselCostTotal}_s = \sum _n\frac{\sum _t\mathit{DieselConsumed}_{s,t} \cdot DieselCost} {(1+ DiscountRate)^{n}}

Finally the cost for the unmment load is calculated with the following equation:

.. math::

	\mathit{LostLoadCostTotal}_s = \sum _n\frac{\sum _t\mathit{LostLoad}_{s,t} \cdot ValueOfLostLoad} {(1+ DiscountRate)^{n}}


PV model
~~~~~~~~

The equation that model the PV array energy yield is given by:


.. math::	

	\mathit{TotalEnergyPV}_{s,t} = \mathit{PVEnergyProduction}_{s,t} \cdot \mathit{InverterEfficiency} \cdot \mathit{PVUnits}

Diesel generator
~~~~~~~~~~~~~~~~

The fuel consumption is modeled by:

.. math::

	\mathit{DieselConsumed}_{s,t} = \mathit{GeneratorEnergy}_{s,t} / (\mathit{GeneratorEfficiency} \cdot \mathit{LowHeatingValue})

In order to ensure that the generator will not exceed his capacity the fallowing constraint is added to the model:

.. math::

	\mathit{GeneratorNominalCapacity} \cdot \mathit{DeltaTime} \geq \mathit{GeneratorEnergy}_{s,t}

Battery bank
~~~~~~~~~~~~

The state of charge of the battery is modeled by:

.. math::
	
	t=1:

	\mathit{StateOfChargeBattery}_{s,1} = BatteryNominalCapacity - \mathit{EnergyBatteryCharge}_{s,1} \cdot  \mathit{ChargeBatteryEfficiency} - \mathit{EnergyBatteryDischarge}_{s,1} \cdot  \mathit{DischargeBatteryEfficiency}        
	
.. math::

	t>1:

	\mathit{StateOfChargeBattery}_{s,t} = BatteryNominalCapacity - \mathit{EnergyBatteryCharge}_{s,t} \cdot  \mathit{ChargeBatteryEfficiency} - \mathit{EnergyBatteryDischarge}_{s,t} \cdot  \mathit{DischargeBatteryEfficiency}

In this equations is important to highlight that in the period 1 the stated of charge of the batterie is equal to the total capacity of the battery.

In order to ensure the durability of the battery a minimum depth of discharge (%) and maximum charge are establish as a constraint:
	
.. math::
		
	
	BatteryNominalCapacity \cdot DeepOfDischarge \leq \mathit{StateOfChargeBattery}_{s,t} \leq BatteryNominalCapacity

The maximum power of charge and discharge are modeled as follow:

.. math::

	MaximunChargePower = BatteryNominalCapacity/MaximunBatteryChargeTime

	MaximunDischargePower = BatteryNominalCapacity/MaximunBatteryDischargeTime

The flow of energy is into and out of the battery is restricted by:

.. math::

	\mathit{EnergyBatteryCharge}_{s,t} \geq - MaximunChargePower \cdot DeltaTime

	\mathit{EnergyBatteryDischarge}_{s,t} \leq MaximunDischargePower \cdot DeltaTime

Energy constraints
~~~~~~~~~~~~~~~~~~

In order to ensure a perfect match between generation and demand, an energy balance is created as a constraint.

.. math::
	
	\mathit{EnergyDemand}_{s,t} = \mathit{TotalEnergyPV}_{s,t} + \mathit{DieselConsumed}_{s,t} + \mathit{EnergyBatteryCharge}_{s,t} 

	+ \mathit{EnergyBatteryDischarge}_{s,t} + \mathit{EnergyCurtailment}_{s,t} + \mathit{LostLoad}_{s,t}
		
This constraint is used to ensure that a percentage of the demand will always be supply and is express as follow:

.. math:: 

	LostLoadProbability =  \frac{\sum _t\mathit{LostLoad}_{s,t}} {\sum _t\mathit{EnergyDemand}_{s,t}}  


