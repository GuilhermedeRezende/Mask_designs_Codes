import os
import numpy
import gdspy
import imecsetup as ims
from numpy import *

print('Using gdspy module version ' + gdspy.__version__)
name = (os.path.abspath(os.path.dirname(os.sys.argv[0]))) + os.sep + 'rezende_ughent_crings_v_final'

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

gap0 = 0.2           #initial gaps between wv and ring [um]
gap1 = 0.6           #initial gaps between wv and ring [um]



sec_gap = 0        # security gap between rings and iii-v stack       [um]
taper_l = 0       # taper length                                     [um]

wg_w2 = 6.65        # waveguide cladding width                         [um]
c_w2 = 3.3          # cavity cladding width                             [um]


d = 400          # space between devices                             [um]

n = 6            # loop counter                             
gap_step=(gap1-gap0)/(n-1)      #sweep gap parameter

## ------------------------------------------------------------------ ##
##  DRAWING                                                           ##
## ------------------------------------------------------------------ ##

def coupled_ring(center,r1,r2,gap,wg2M,wg2m,layer_num,data_type):
    ring1=gdspy.Round(center,r1,r1-wg_w,max_points=4094,number_of_points=0.1,layer=layer_num,datatype=data_type)

    pr2 = -(r1-wg_w-gap-r2) #inner ring position
    ring2=gdspy.Round((center[0],center[1]+pr2),r2,max_points=4094,number_of_points=0.1,layer=layer_num,datatype=data_type)

    rsub= r2-(wg2M+wg2m)/2.0
    ring3=gdspy.Round((center[0],center[1]+pr2-r2+wg2M+rsub),rsub,max_points=4094,number_of_points=0.1,layer=layer_num,datatype=data_type)
    
    bool = gdspy.boolean([ring2,ring3],subtraction,max_points=4094,layer=layer_num,datatype=data_type)
    bool = gdspy.boolean([bool,ring1],sum,max_points=4094,layer=layer_num,datatype=data_type)
    
    return bool

def draw(gap):

    ## ------------------------------------------------------------------ ##
    ##	Define Cells						      ##
    ## ------------------------------------------------------------------ ##
    wg_cell = []
    cavity_cell = []
    gccell = []

    del (wg_cell,cavity_cell,gccell)
    
    ## Cell containing the waveguides
    wg_cell = gdspy.Cell('WV'+ str((n-1)*(gap-gap0)/(gap1-gap0)))

    ## Cell containing microrings
    cavity_cell = gdspy.Cell('DRING'+ str((n-1)*(gap-gap0)/(gap1-gap0)))

    ## Cell containing bragg couplings

    gc = gdspy.GdsImport('GC_mod.gds',
                        rename={'q': 'CPGRAT'+ str((n-1)*(gap-gap0)/(gap1-gap0))},
                        layers={10158: 1158})

    gccell = gc.extract('CPGRAT'+ str((n-1)*(gap-gap0)/(gap1-gap0)))
    

    ## ------------------------------------------------------------------ ##
    ##	Layer Specification					      ##
    ## ------------------------------------------------------------------ ##

    spec = {'layer': 37, 'datatype': 4}  # Fully etched SOI: waveguide core
    spec2 = {'layer': 37, 'datatype': 5}  # Fully etched SOI: waveguide cladding (trench around core)
    spec3 = {'layer': 1158, 'datatype': 0}  # Area not to be filled with dummies (SOI,Poly or metal)

   
## ------------------------------------------------------------------ ##
##	Objects Design				        	      ##
## ------------------------------------------------------------------ ##

    #------ Waveguide+taper   -----------------------------------------------#

    waveguide = gdspy.Path(wg_w, (-sec_gap,0))
    waveguide.segment(sec_gap,'+x',**spec)
    waveguide.segment(r1*(1-2*sin(pi/8.0)),'+x',**spec)
    waveguide.turn(r1, -pi/8.0,max_points=4094,number_of_points=0.1, **spec)
    waveguide.turn(r1, pi/8.0,max_points=4094,number_of_points=0.1, **spec)
    waveguide.turn(r1, pi/8.0,max_points=4094,number_of_points=0.1, **spec)
    waveguide.turn(r1, -pi/8.0,max_points=4094,number_of_points=0.1, **spec)
    waveguide.segment(r1*(1-2*sin(pi/8.0)),'+x',**spec)
    waveguide.segment(sec_gap,'+x',**spec)    

     #------ Coupled DRing   -----------------------------------------------#
    
    pcavc = (waveguide.x-sec_gap-r1,waveguide.y-gap-0.5*wg_w-r1*2*(1.5-cos(pi/8.0)))
    cav = coupled_ring(pcavc,r1,r2,gap,wg_w2M,wg_w2m,spec["layer"],spec["datatype"])
   

    #------ Trench Arond waveguides   -----------------------------------------------#

    waveguide2 = gdspy.Path(wg_w2, (-sec_gap,0))
    waveguide2.segment(sec_gap,'+x',**spec2)
    waveguide2.segment(r1*(1-2*sin(pi/8.0)),'+x',**spec2)
    waveguide2.turn(r1, -pi/8.0,max_points=4094,number_of_points=0.1, **spec2)
    waveguide2.turn(r1, pi/8.0,max_points=4094,number_of_points=0.1, **spec2)
    waveguide2.turn(r1, pi/8.0,max_points=4094,number_of_points=0.1, **spec2)
    waveguide2.turn(r1, -pi/8.0,max_points=4094,number_of_points=0.1, **spec2)
    waveguide2.segment(r1*(1-2*sin(pi/8.0)),'+x',**spec2)
    waveguide2.segment(sec_gap,'+x',**spec2)
    
    #------ Trench Arond coupled rings   -----------------------------------------------#

    cav12= gdspy.Rectangle( (pcavc[0]-r1-c_w2,pcavc[1]-r1-c_w2),(pcavc[0]+r1+c_w2,pcavc[1]+r1),**spec2)

    #+c_w2+2*c_w2

    #nofillc=gdspy.Rectangle( (waveguide.x-sec_gap-r1-taper_l-r1-wg_w2,waveguide.y-gap-0.5*wg_w-r1*2*(1.5-cos(pi/8.0))-r1-wg_w2),(waveguide.x-sec_gap-r1-taper_l+r1+wg_w2,waveguide.y-gap-0.5*wg_w-r1*2*(1.5-cos(pi/8.0))+r1+wg_w2),**spec3)
    #nofillw=gdspy.Rectangle( (-bragg_offset,-bragg_nofill/2.0-bragg_nfoffset),(waveguide.x,waveguide.y+bragg_nofill/2.0-bragg_nfoffset),**spec3)

    ## ------------------------------------------------------------------ ##
    ##	Adding Objects into Cells				        	      ##
    ## ------------------------------------------------------------------ ##

    wg_cell.add(waveguide)  
    wg_cell.add(waveguide2) # Cell: Waveguide; Objects: waveguide+taper, waveguide trenching

    cavity_cell.add(cav)
    cavity_cell.add(cav12)  # Cell: Cavity; Objects: coupled rings, ring trenching

    waveguidex=waveguide.x
    waveguidey=waveguide.y

    
    # --------- Taper sections --------------------------- #

    return (wg_cell,cavity_cell,gccell,waveguidex,waveguidey)


combined_cell=gdspy.Cell('COMB2')

for ii in range(0,n,1):

    (wv,cc,gratc,wgx,wgy) = draw(gap0+gap_step*(ii))

    combined_cell.add(gdspy.CellReference(wv,origin=(0,-ii*d)))
    combined_cell.add(gdspy.CellReference(cc,origin=(0,-ii*d)))
    combined_cell.add(gdspy.CellReference(gratc,origin=(-sec_gap,-ii*d)))
    combined_cell.add(gdspy.CellReference(gratc,origin=(wgx, wgy-ii*d ),rotation=180, x_reflection=True))
    



## ------------------------------------------------------------------ ##
##	OUTPUT															  ##
## ------------------------------------------------------------------ ##

## Output the layout to a GDSII file (default to all created cells).
## Set the units we used to micrometers and the precision to nanometers.
gdspy.gds_print(name + 'mod_.gds', unit=1.0e-6, precision=1.0e-9)
print('Sample gds file saved: ' + name + 'mod_.gds')


## ------------------------------------------------------------------ ##
##	VIEWER															  ##
## ------------------------------------------------------------------ ##

## View the layout using a GUI.  Full description of the controls can
## be found in the online help at http://gdspy.sourceforge.net/
#gdspy.LayoutViewer()
