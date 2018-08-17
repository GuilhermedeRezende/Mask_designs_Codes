import os
import numpy
import gdspy
import imecsetup as ims
from numpy import *

print('Using gdspy module version ' + gdspy.__version__)
name = (os.path.abspath(os.path.dirname(os.sys.argv[0]))) + os.sep + 'rezende_full_final'

##-------------------------------------------------------------##
##        PARAMETERS
##-------------------------------------------------------------##

d= 2200         # distance btw layouts [um]

gdsii1 = gdspy.GdsImport('rezende_ughent_ribs_final_2.gds')
c1=gdsii1.extract('COMB1')
gdsii2 = gdspy.GdsImport('rezende_ughent_crings_v_final.gds')
c2=gdsii2.extract('COMB2')

tog =gdspy.Cell('REZENDE_FULL')

tog.add(gdspy.CellReference(c1,origin=(0,0)))
tog.add(gdspy.CellReference(c2,origin=(d,0)))

## ------------------------------------------------------------------ ##
##	OUTPUT															  ##
## ------------------------------------------------------------------ ##

## Output the layout to a GDSII file (default to all created cells).
## Set the units we used to micrometers and the precision to nanometers.
gdspy.gds_print(name +  '.gds', unit=1.0e-6, precision=1.0e-9)
print('Sample gds file saved: ' + name + '.gds')
