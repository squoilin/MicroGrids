Model Description
=================

Sets
----

==========  ==========  =====================================
Name	    Symbol      Description                       
==========  ==========  =====================================
Years	    n		Year of the project	        
Periods     t		Period that are divided the years 
==========  ==========  =====================================

Parameters
----------

Data analysis parameters 
~~~~~~~~~~~~~~~~~~~~~~~~

==========  =====  ======================================================
Name	    Unit   Description                       
==========  =====  ======================================================
Startdate   Day    Start date of the analysis
PlotTime    Days   Number of days for the plot of energy dispatch
PlotDay	    Day    Start date for the dispatch plot	
==========  =====  ======================================================

PV parameters
~~~~~~~~~~~~~

==========================   ========  ======================================================
Name	                     Unit      Description                       
==========================   ========  ======================================================
PVNominalCapacity	     W/unit    Nominal capacity of one PV unit
InverterEfficiency	     %         efficiency of the inverter to transform DC energy to AC
PVinvesmentCost              USD/W     Investment Cost to install PV panels
PVEnergyProduction (t)       Wh        The yield of energy of one PV unit in the period t
==========================   ========  ======================================================

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
EnergyDemand (t)		  W         The total energy demand of the system
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
=====================================  =======  =======================================================================================

Variables
---------

PV variables
~~~~~~~~~~~~

===============================  ========  =====================================================
Name	                         Unit      Description                       
===============================  ========  =====================================================
PVUnits                          unit      Number of installed PV 
TotalEnergyPV (t)		 Wh        Energy generated for all the PVs in the system
===============================  ========  =====================================================

Battery variables
~~~~~~~~~~~~~~~~~

===============================  ========  =====================================================
Name	                         Unit      Description                       
===============================  ========  =====================================================
BatteryNominalCapacity           Wh	   Nominal capacity of the battery bank
EnergyBatteryDischarge (t)       Wh        Energy that flows out of the battery
EnergyBatteryCharge (t)          Wh        Energy that flows in to the battery
StateOfChargeBattery (t)         Wh        Energy inside the battery
MaximunChargePower               W         Maximum charge power
MaximunDischargePower            W         Maximum discharge power
===============================  ========  =====================================================

Diesel generator variables
~~~~~~~~~~~~~~~~~~~~~~~~~~

===============================  ========  =====================================================
Name	                         Unit      Description                       
===============================  ========  =====================================================
GeneratorNominal_Capacit         W 	   Nominal capacity of the diesel generator
DieselConsumed (t)               L         Diesel consumed to produce energy
GeneratorEnergy (t)              Wh        Energy produced by the diesel generator
===============================  ========  =====================================================

Energy balance variables
~~~~~~~~~~~~~~~~~~~~~~~~

===============================  ========  =====================================================
Name	                         Unit      Description                       
===============================  ========  =====================================================
LostLoad (t)			 Wh        Energy not supply by the system
EnergyCurtailment (t)            Wh	   Curtailment of solar energy
===============================  ========  =====================================================

Project variables
~~~~~~~~~~~~~~~~~~~

===============================  ========  =====================================================
Name	                         Unit      Description                       
===============================  ========  =====================================================
FinancialCost		         USD       Financial cost 
===============================  ========  =====================================================


Modeling of the system
-----------------------

Objective function
------------------

The objective function will be to minimize the Net Present Cost (NPC) for n years. With the INV being the total investment, TCP as the total cost of the period.

.. math::


	NPC = INV + \sum _n\frac{\mathit{TCP}_n} {(1+ DiscountRate)^n}

The total investment equation is:

.. math:: 

	INV = (PVinvestmentCost \cdot PVNominalCapacity \cdot PVUnits + BatteryNominalCapacity \cdot BatteryInvestmentCost  
	
	+ GeneratorInvestmentCost \cdot GeneratorNominalCapacity  ) \cdot (1 - PorcentageFunded)

The Total cost of the period is composed by operation and maintenance cost (OM), the financial cost, the replacement cost (ReplacementCost)and the total cost of the diesel in the periods (DieselCost):

.. math::

	\mathit{TCP}_n = OM + FinancialCost + \mathit{ReplacementCost}_n + \mathit{DieselCost}_n

The OM is stated by:

.. math:: 

	OM = PVinvesmentCost \cdot PVNominalCapacity \cdot PVUnits \cdot MaintenanceOperationCostPV 
	
	+ BatteryNominalCapacity \cdot BatteryInvesmentCost  \cdot MaintenanceOperationCostBattery

	+ GeneratorInvesmentCost \cdot GeneratorNominalCapacity  \cdot MaintenanceOperationCostGenerator

The financial cost is a fix amount, that is payed each period to pay the loan acquire to finance a percentage of the initial investment and is calculated with the following equation:

.. math::

	FinancialCost = \frac{INV \cdot PorcentageFunded \cdot InterestRate} {1 - (1 + InterestRate)^{-Years}}

The replacement cost is given by the fallowing equation:

.. math::

	\mathit{ReplacementCost}_{10} = \frac{BatteryNominalCapacity \cdot BatteryInvesmentCost} {(1+ DiscountRate)^{10}}

Finally the Diesel cost is calculated by:

.. math::

	\mathit{DieselCost}_n = \sum _t\mathit{DieselConsumed}_t \cdot DieselCost

PV model
~~~~~~~~

The equation that model the PV array energy yield is given by:


.. math::	

	\mathit{TotalEnergyPV}_t = \mathit{PVEnergyProduction}_t \cdot \mathit{InverterEfficiency} \cdot \mathit{PVUnits}

Diesel generator
~~~~~~~~~~~~~~~~

The fuel consumption is modeled by:

.. math::

	\mathit{DieselConsumed}_t = \mathit{GeneratorEnergy}_t / (\mathit{GeneratorEfficiency} \cdot \mathit{LowHeatingValue})

In order to ensure that the generator will not exceed his capacity the fallowing constraint is added to the model:

.. math::

	\mathit{GeneratorNominalCapacity} \cdot \mathit{DeltaTime} \geq \mathit{GeneratorEnergy}_t

Battery bank
~~~~~~~~~~~~

The state of charge of the battery is modeled by:

.. math::
	
	t=1:

	\mathit{StateOfChargeBattery}_1 = BatteryNominalCapacity - \mathit{EnergyBatteryCharge}_1 \cdot  \mathit{ChargeBatteryEfficiency} 

	- \mathit{EnergyBatteryDischarge}_1 \cdot  \mathit{DischargeBatteryEfficiency}        
	
.. math::

	t>1:

	\mathit{StateOfChargeBattery}_t = BatteryNominalCapacity - \mathit{EnergyBatteryCharge}_t \cdot  \mathit{ChargeBatteryEfficiency} 
   
	- \mathit{EnergyBatteryDischarge}_t \cdot  \mathit{DischargeBatteryEfficiency}

In this equations is important to highlight that in the period 1 the stated of charge of the batterie is equal to the total capacity of the battery.

In order to ensure the durability of the battery a minimum depth of discharge (%) and maximum charge are establish as a constraint:
	
.. math::
		
	
	BatteryNominalCapacity \cdot DeepOfDischarge \leq \mathit{StateOfChargeBattery}_t \leq BatteryNominalCapacity

The maximum power of charge and discharge are modeled as follow:

.. math::

	MaximunChargePower = BatteryNominalCapacity/MaximunBatteryChargeTime

	MaximunDischargePower = BatteryNominalCapacity/MaximunBatteryDischargeTime

The flow of energy is into and out of the battery is restricted by:

.. math::

	\mathit{EnergyBatteryCharge}_t \geq - MaximunChargePower \cdot DeltaTime

	\mathit{EnergyBatteryDischarge}_t \leq MaximunDischargePower \cdot DeltaTime

Energy constraints
~~~~~~~~~~~~~~~~~~

In order to ensure a perfect match between generation and demand, an energy balance is created as a constraint.

.. math::
	
	\mathit{EnergyDemand}_t = \mathit{TotalEnergyPV}_t + \mathit{DieselConsumed}_t + \mathit{EnergyBatteryCharge}_t 

	+ \mathit{EnergyBatteryDischarge}_t + \mathit{EnergyCurtailment}_t + \mathit{LostLoad}_t
		
This constraint is used to ensure that a percentage of the demand will always be supply and is express as follow:

.. math:: 

	LostLoadProbability =  \frac{\sum _t\mathit{LostLoad}_t} {\sum _t\mathit{EnergyDemand}_t}  


