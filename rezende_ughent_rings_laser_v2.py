import os
import numpy
import gdspy
import imecsetup as ims
from numpy import *

print('Using gdspy module version ' + gdspy.__version__)
name = (os.path.abspath(os.path.dirname(os.sys.argv[0]))) + os.sep + 'rezende_ughent_crings_test'

print('Creating layout')

## ------------------------------------------------------------------ ##
##  DEFINITIONS                                                       ##
## ------------------------------------------------------------------ ##

# Define boolean operations
subtraction = lambda p1, p2: p1 and not p2
sum = lambda p1, p2: p1 or p2
intersection = lambda p1, p2: p1 and p2

##-------------------------------------------------------------##
##        PARAMETERS
##-------------------------------------------------------------##

wg_w = 0.65         # waveguide width  [um]
r1 = 150
r2 = 100
wg_w2m = .3
wg_w2M = .65
gap = .2


## ------------------------------------------------------------------ ##
##  DRAWING                                                           ##
## ------------------------------------------------------------------ ##

def coupled_ring(layer_num,center,r1,r2,gap,wg2M,wg2m):
    ring1=gdspy.Round(center,r1,r1-wg_w,max_points=4094,number_of_points=0.1,layer=layer_num)

    pr2 = -(r1-wg_w-gap-r2) #inner ring position
    ring2=gdspy.Round((center[0],center[1]+pr2),r2,max_points=4094,number_of_points=0.1,layer=layer_num)

    rsub= r2-(wg2M+wg2m)/2.0
    ring3=gdspy.Round((center[0],center[1]+pr2-r2+wg2M+rsub),rsub,max_points=4094,number_of_points=0.1,layer=layer_num)
    
    bool = gdspy.boolean([ring2,ring3],subtraction,max_points=4094,layer=layer_num)
    bool = gdspy.boolean([bool,ring1],sum,max_points=4094,layer=layer_num)
    
    return bool


## ------------------------------------------------------------------ ##
##  DRAWING                                                           ##
## ------------------------------------------------------------------ ##

# Layers
layer_vector = [1,20,21,7,11,6] # order: disks, bullseye mod a, bullseye mod wRing, idmarks, working area, align marks

# Create a cell for the unit element
unit_cell1 = gdspy.Cell('double_ring') #double ring


dev1 = coupled_ring(1,(0,0),r1,r2,gap,wg_w2M,wg_w2m)

unit_cell1.add(dev1)



## ------------------------------------------------------------------ ##
##	OUTPUT															  ##
## ------------------------------------------------------------------ ##

## Output the layout to a GDSII file (default to all created cells).
## Set the units we used to micrometers and the precision to nanometers.
gdspy.gds_print(name +  '.gds', unit=1.0e-6, precision=1.0e-9)
print('Sample gds file saved: ' + name + '.gds')



