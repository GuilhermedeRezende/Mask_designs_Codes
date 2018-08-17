import os
import numpy
import gdspy
from numpy import *
import bib_geom_func 

print('Using gdspy module version ' + gdspy.__version__)

name = (os.path.abspath(os.path.dirname(os.sys.argv[0]))) + os.sep + 'devices'

print('Creating layout')

    	
## ------------------------------------------------------------------ ##
##  DRAWING                                                           ##
## ------------------------------------------------------------------ ##

# Layers
layer_vector = [1] # order: disks, bullseye mod a, bullseye mod wRing, idmarks, working area, align marks

# Create a cell for the unit element
unit_cell1 = gdspy.Cell('testcell')

for x in range(0,19):
    unit_cell1.add(draw_waveguide(1,(0,0.01*x),x,19))
	
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
