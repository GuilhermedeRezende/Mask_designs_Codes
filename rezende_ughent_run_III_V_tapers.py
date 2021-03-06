import os
import numpy
import gdspy
import imecsetup as ims
from numpy import *

print('Using gdspy module version ' + gdspy.__version__)
name = (os.path.abspath(os.path.dirname(os.sys.argv[0]))) + os.sep + 'taper_III_V2'

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


def draw(gap):

    ## ------------------------------------------------------------------ ##
    ##	Define Cells						      ##
    ## ------------------------------------------------------------------ ##
    wg_cell = []
    nofill_cell = []
    cavity_cell = []
    gccell = []

    del (wg_cell,nofill_cell,cavity_cell,gccell)
    
    ## Cell containing the waveguides
    wg_cell = gdspy.Cell('WAVEGUIDES'+ str(2*n*(gap-gap0)/(gap0+gap1)))

    ## Cell containing no fill area
    nofill_cell = gdspy.Cell('NOFILL'+ str(2*n*(gap-gap0)/(gap0+gap1)))

    ## Cell containing microrings
    cavity_cell = gdspy.Cell('CAV'+ str(2*n*(gap-gap0)/(gap0+gap1)))

    ## Cell containing bragg couplings

    gc = gdspy.GdsImport('GC_mod.gds',
                        rename={'q': 'COUPLERGRATING'+ str(2*n*(gap-gap0)/(gap0+gap1))},
                        layers={10158: 1158})

    gccell = gc.extract('COUPLERGRATING'+ str(2*n*(gap-gap0)/(gap0+gap1)))
    

    ## Aligment Cell

    am = gdspy.GdsImport('aligment_mark.gds',
                        rename={'Alignment_Mark': 'Alignment_Mark'+ str(2*n*(gap-gap0)/(gap0+gap1))})

    amcell = am.extract('Alignment_Mark'+ str(2*n*(gap-gap0)/(gap0+gap1)))
    

    

  

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
    waveguide.segment(taper_l,'+x',final_width= taper_w,**spec)

    ## ------------------------------------------------------------------ ##
    ##	Adding Objects into Cells				        	      ##
    ## ------------------------------------------------------------------ ##

    wg_cell.add(waveguide)  
    
    waveguidex=waveguide.x
    waveguidey=waveguide.y

    
    # --------- Taper sections --------------------------- #

    return (wg_cell,waveguidex,waveguidey)


#waveguidex = draw(-1)[4]
#waveguidey = draw(-2)[5]
#
#
combined_cell=gdspy.Cell('COMB1')
#combined_cell2=gdspy.Cell('COMB2')

#(wv,cc,gratc,nfc,wgx,wgy) = draw(gap0+gap_step*(ii))
#combined_cell.add(gdspy.CellReference(wv,origin=(0,-ii*d)))
#combined_cell.add(gdspy.CellReference(wv,origin=(2*wgx + 2*(taper_ii_l)+iii_v_l, wgy-ii*d ),rotation=180, x_reflection=True))
for ii in range(0,n,1):

    (wv,wgx,wgy) = draw(gap0+gap_step*(ii))

    combined_cell.add(gdspy.CellReference(wv,origin=(0,-ii*d)))
    combined_cell.add(gdspy.CellReference(wv,origin=(2*wgx + 2*(taper_ii_l)+iii_v_l, wgy-ii*d ),rotation=180, x_reflection=True))
   

## ------------------------------------------------------------------ ##
##	OUTPUT															  ##
## ------------------------------------------------------------------ ##

## Output the layout to a GDSII file (default to all created cells).
## Set the units we used to micrometers and the precision to nanometers.
gdspy.gds_print(name +  '.gds', unit=1.0e-6, precision=1.0e-9)
print('Sample gds file saved: ' + name + '.gds')


## ------------------------------------------------------------------ ##
##	VIEWER															  ##
## ------------------------------------------------------------------ ##

## View the layout using a GUI.  Full description of the controls can
## be found in the online help at http://gdspy.sourceforge.net/
#gdspy.LayoutViewer()

