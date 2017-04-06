.. Micro-Grids documentation master file, created by
   sphinx-quickstart on Thu Apr 14 14:59:11 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Micro-Grids's documentation!
=======================================
:Organization 1:  `University Of Liege`_,
		   `Energy Systems Research unit`_
:Organization 2:  `University Mayor of San Simon`_, Energy Center
               
		
:Version: |version|
:Date: |today|


The world is currently undergoing a drastic change of the energy matrix from conventional sources of energy to renewable and alternative ones. This trend is particularly relevant in the challenge of rural electrification in developing countries because in some cases the levelized cost of electricity (LCOE) of hybrid or renewable systems can be competitive with the extension of the main grid in order to supply the energy demand of isolated communities [1].  However, exploiting solar energy for off-grid rural electrification faces some major challenges, especially due to the stochastic nature of the solar resource and eventual electricity demand (viz.load profile). These can have a serious impact on the sizing of the micro-grid, and the stability and reliability of the energy supply. In addition, as analysed in [2-3], an insightful analysis on how the electrification process impacts the electricity-user’s behaviour is generally lacking when planning a
micro-grid, as well as a generalized underestimation of the social aspect during the design phase.To this aim, optimization techniques fulfill a key role in differents aspects of micro-grid planning and operating procedure in order to reduce the LCOE for a determined micro-grid [4].  

The Micro-Grid library main objective is to provide an open source alternative to the problem of sizing and dispatch of energy in micro-grids in isolated places. It's written in python(pyomo) and use excel and text files as input and output data handling and visualization.

Main features:

* Robust optimization
* Optimal sizing of Lion-Ion batteries, diesel generators and PV panels in order to supply a demand with the lowest cost possible.
* Optimal dispatch from different energy sources.
* Calculation of the net present cost of the system for the project lifetime.
* Determination of the LCOE for the optimal system1.

Contents
========
.. toctree::
   :maxdepth: 2

   Overview
   Model Description
   API	
   Tutorial

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

License
=======

Copyright 2016 Sergio Balderrama, Sylvain Quoilin
  
Licensed under the EUPL, Version 1.1 or – as soon they will be approved by the European Commission - subsequent versions of the EUPL (the "Licence"); You may not use this work except in compliance with the Licence. 
You may obtain a copy of the Licence at: 

http://ec.europa.eu/idabc/eupl
 
Unless required by applicable law or agreed to in writing, software distributed under the Licence is distributed on an "AS IS" basis, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the Licence for the specific language governing permissions and limitations under the Licence. 

References
----------
.. [1] Nguyen K., Alternatives to grid extension for rural electrification: Decentralized renewable energy technologies in Vietnam. Energy Policy 2007; 35:2579-2589.
.. [2] Murphy T., Making the energy transition in rural East Africa: Is leapfrogging an alternative? Technological Forecasting & Social Change 2001; 68: 173-193.
.. [3] Madubansi M, Shackleton C.M., Changing energy profiles and consumption patterns following electrification in five rural villages, South Africa. Energy Policy 2006; 34: 4081-4092.
.. [4] Gamarra C., Guerrero J., Computational optimization techniques applied to microgrids planning: A review. Renewable and Sustainable Energy Reviews 2015; 48:413-424.

.. _matplotlib: http://matplotlib.org
.. _pandas: http://pandas.pydata.org
.. _pyomo: http://www.pyomo.org/
.. _University Of Liege: https: https://www.ulg.ac.be/cms/c_5000/en/home
.. _Energy Systems Research unit: http://www.labothap.ulg.ac.be/cmsms/index.php?page=energy-systems
.. _University Mayor of San Simon: http://www.umss.edu.bo/

