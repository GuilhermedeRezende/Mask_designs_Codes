import os
import numpy
import gdspy
from numpy import *
import bib_geom_func 

print('Using gdspy module version ' + gdspy.__version__)

name = (os.path.abspath(os.path.dirname(os.sys.argv[0]))) + os.sep + 'devices'

print('Creating layout')

##-------------------------------------------------------------##
##        PARAMETERS
##-------------------------------------------------------------##
wg_w = 0.5          # waveguide width                   [um]
taper_l = 50        # taper length                      [um]
taper_w = 0.15      # taper final width                 [um]

    	
## ------------------------------------------------------------------ ##
##  DRAWING                                                           ##
## ------------------------------------------------------------------ ##


## ------------------------------------------------------------------ ##
##	Rib Waveguides - Coupled Microring Resonators														  ##
## ------------------------------------------------------------------ ##

## Cell containing the waveguides
cmrrib_cell = gdspy.Cell('MICRORINGS')
spec = {'layer': 1, 'datatype': 1}  # layer 1, datatype 1

cmrrib_cell.add(gdspy.Path(1, initial_point=(0, 0), number_of_paths=1, distance=0, **spec)


	
## ------------------------------------------------------------------ ##
##  OUTPUT                                                            ##
## ------------------------------------------------------------------ ##

## Output the layout to a GDSII file (default to all created cells).
## Set the units we used to micrometers and the precision to nanometers.
gdspy.gds_print(name + '.gds', unit=1.0e-6, precision=1.0e-9)
print('Sample gds file saved: ' + name + '.gds')


## ------------------------------------------------------------------ ##
##  VIEWER                                                            ##
## ------------------------------------------------------------------ ##

## View the layout using a GUI.  Full description of the controls can
## be found in the online help at http://gdspy.sourceforge.net/
print('Opening viewer')
gdspy.LayoutViewer()

