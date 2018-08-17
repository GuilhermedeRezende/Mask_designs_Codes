# -*- coding: cp1252 -*-
import os
import numpy
import gdspy
import imecsetup as ims
from numpy import *

print('Using gdspy module version ' + gdspy.__version__)
name = (os.path.abspath(os.path.dirname(os.sys.argv[0]))) + os.sep + 'rezende_heaters_test'

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

nofill_w = 70       #no tilling region width [um]

gap0 = 0.2           #initial gaps between wv and ring [um]
gap1 = 0.6           #initial gaps between wv and ring [um]

r1 = 40           #outer ring radius [um]
r2 = (r1-wg_w-3.0*gap0/2.0)/2.0       #inner ring radius [um]

sec_gap = 150        # security gap between rings and iii-v stack       [um]
taper_l = 150       # taper length                                     [um]
taper_w = 0.300     # taper final width                                [um]
taper_ii_l = 30     # III-V taper length                               [um]
iii_v_l = 500       # III-V length                                     [um]

wg_w2 = 6.65        # waveguide cladding width                         [um]
c_w2 = 3.3          # cavity cladding width                             [um]

bragg_offset = 6    # waveguide at bragg grating without nofill        [um]
bragg_nfoffset = .143   # nofill at bragg grating offset      [um]
bragg_nofill= 39.152    # waveguide at bragg grating without nofill        [um]

d = 125           # space between devices                             [um]
nofill_w = 50      #no tilling region width [um]

n = 20            # loop counter                             
gap_step=(gap1-gap0)/(n-1)      #sweep gap parameter

alL = 350 #aligment distance to device

final_pos = numpy.array([(2*r1+sec_gap+taper_l+taper_ii_l)*2+iii_v_l,(n*d)])

hw= 3.0 #nicr heater width
hh= 30.0 #nicr heater height
ang = pi/12.0 # 30° heater
sqr = 10.0

spec4=1
pcavc=(1,1)
nccell = gdspy.Cell('Heater_Ni_Cr')
combined_cell=gdspy.Cell('COMB1')

def nicrheat(layer_num,center,radius,hw,hh,ang,sqr):
    pos1 = (center[0]-radius*sin(2.0*ang),center[1]-radius*cos(2.0*ang))
    pos2 = (center[0]+radius*sin(2.0*ang),center[1]-radius*cos(2.0*ang))
                                
                                                             
    nch1=gdspy.Round(center,radius+hw/2,radius-hw/2,initial_angle=-ang-pi/2.0, final_angle=ang-pi/2.0,layer=layer_num,number_of_points=2000,max_points=199)
    nch2=gdspy.Rectangle(pos1,(pos1[0]-hw,pos1[1]-hh),layer=layer_num)
    nch3=gdspy.Rectangle(pos2,(pos2[0]-hw,pos2[1]-hh),layer=layer_num)

    nch4=gdspy.Rectangle((pos1[0]-hw/2.0+sqr/2.0,pos1[1]-hh),(pos1[0]-hw/2.0-sqr/2.0,pos1[1]-hh-sqr),layer=layer_num)
    nch5=gdspy.Rectangle((pos2[0]-hw/2.0+sqr/2.0,pos2[1]-hh),(pos2[0]-hw/2.0-sqr/2.0,pos2[1]-hh-sqr),layer=layer_num)

    bool = gdspy.boolean([nch1,nch2],sum,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,nch3],sum,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,nch4],sum,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,nch5],sum,max_points=199,layer=layer_num)
    return bool

nch =  nicrheat(spec4,pcavc,r1,hw,hh,ang,sqr)
nccell.add(nch)
combined_cell.add(gdspy.CellReference(nccell,origin=(0,-d)))

gdspy.gds_print(name +  '.gds', unit=1.0e-6, precision=1.0e-9)
print('Sample gds file saved: ' + name + '.gds')
