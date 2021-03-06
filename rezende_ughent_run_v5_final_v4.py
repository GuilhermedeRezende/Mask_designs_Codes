import os
import numpy
import gdspy
import imecsetup as ims
from numpy import *

print('Using gdspy module version ' + gdspy.__version__)
name = (os.path.abspath(os.path.dirname(os.sys.argv[0]))) + os.sep + 'rezende_ughent_ribs_final_3'

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

D = 50 #distance between copies 


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
    wg_cell = gdspy.Cell('WAVEGUIDES'+ str((n-1)*(gap-gap0)/(gap1-gap0)))

    ## Cell containing no fill area
    nofill_cell = gdspy.Cell('NOFILL'+ str((n-1)*(gap-gap0)/(gap1-gap0)))

    ## Cell containing microrings
    cavity_cell = gdspy.Cell('CAV'+ str((n-1)*(gap-gap0)/(gap1-gap0)))

    ## Cell containing bragg couplings

    gc = gdspy.GdsImport('GC_mod.gds',
                        rename={'q': 'COUPLERGRATING'+ str((n-1)*(gap-gap0)/(gap1-gap0))},
                        layers={10158: 1158})

    gccell = gc.extract('COUPLERGRATING'+ str((n-1)*(gap-gap0)/(gap1-gap0)))
    

    ## Aligment Cell

    am = gdspy.GdsImport('markerx1_jing_ghent_mod.gds',
                        rename={'markerx': 'Alignment_Mark'+ str((n-1)*(gap-gap0)/(gap1-gap0))})

    amcell = am.extract('Alignment_Mark'+ str((n-1)*(gap-gap0)/(gap1-gap0)))
    

    

  

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

    

    #------ No tilling region   -----------------------------------------------#
    nofill = gdspy.Path(nofill_w,(waveguide.x-taper_l,waveguide.y))
    nofill.segment(taper_l+taper_ii_l+iii_v_l/2.0,'+x',**spec3)
    

    #------ Coupled Microrings   -----------------------------------------------#
    r2 = (r1-wg_w-3.0*gap/2.0)/2.0 
    pcavc = (waveguide.x-sec_gap-r1-taper_l,waveguide.y-gap-0.5*wg_w-r1*2*(1.5-cos(pi/8.0)))
    cav1=gdspy.Round( (pcavc[0],pcavc[1]),r1,r1-wg_w,max_points=4094,number_of_points=0.1,**spec)
    cav2=gdspy.Round( (pcavc[0]+r2+0.5*gap,pcavc[1]),r2,r2-wg_w,max_points=4094,number_of_points=0.1,**spec)
    cav3=gdspy.Round( (pcavc[0]-r2-0.5*gap,pcavc[1]),r2,r2-wg_w,max_points=4094,number_of_points=0.1,**spec)

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
    waveguide2.segment(taper_l,'+x',**spec2)

    #------ Trench Arond coupled rings   -----------------------------------------------#

    cav12= gdspy.Rectangle( (pcavc[0]-r1-c_w2,pcavc[1]-r1-c_w2),(pcavc[0]+r1+c_w2,pcavc[1]+r1+2*r1*(1-cos(pi/8.0))+gap+(wg_w+wg_w2)/2.0),**spec2)

    #r1+2*r1*(1-cos(pi/8.0))+gap+(wg_w+wg_w2)/2.0

    #nofillc=gdspy.Rectangle( (waveguide.x-sec_gap-r1-taper_l-r1-wg_w2,waveguide.y-gap-0.5*wg_w-r1*2*(1.5-cos(pi/8.0))-r1-wg_w2),(waveguide.x-sec_gap-r1-taper_l+r1+wg_w2,waveguide.y-gap-0.5*wg_w-r1*2*(1.5-cos(pi/8.0))+r1+wg_w2),**spec3)
    #nofillw=gdspy.Rectangle( (-bragg_offset,-bragg_nofill/2.0-bragg_nfoffset),(waveguide.x,waveguide.y+bragg_nofill/2.0-bragg_nfoffset),**spec3)

    ## ------------------------------------------------------------------ ##
    ##	Adding Objects into Cells				        	      ##
    ## ------------------------------------------------------------------ ##

    wg_cell.add(waveguide)  
    wg_cell.add(waveguide2) # Cell: Waveguide; Objects: waveguide+taper, waveguide trenching

    nofill_cell.add(nofill) #Cell: No fill; Objects: No tilling region
    #wg_cell.add(nofillw)

    cavity_cell.add(cav1)
    cavity_cell.add(cav2)
    cavity_cell.add(cav3)
    cavity_cell.add(cav12)  # Cell: Cavity; Objects: coupled rings, ring trenching

    waveguidex=waveguide.x
    waveguidey=waveguide.y

    
    # --------- Taper sections --------------------------- #

    return (wg_cell,cavity_cell,gccell,nofill_cell,waveguidex,waveguidey,amcell)


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

    (wv,cc,gratc,nfc,wgx,wgy,amc) = draw(gap0+gap_step*(ii))

    combined_cell.add(gdspy.CellReference(wv,origin=(0,-ii*d)))
    combined_cell.add(gdspy.CellReference(wv,origin=(2*wgx + 2*(taper_ii_l)+iii_v_l, wgy-ii*d ),rotation=180, x_reflection=True))
    combined_cell.add(gdspy.CellReference(cc,origin=(0,-ii*d)))
    combined_cell.add(gdspy.CellReference(cc,origin=(2*wgx + 2*(taper_ii_l)+iii_v_l, wgy-ii*d ),rotation=180, x_reflection=True))
    combined_cell.add(gdspy.CellReference(gratc,origin=(-sec_gap,-ii*d)))
    combined_cell.add(gdspy.CellReference(gratc,origin=(sec_gap+2*wgx + 2*(taper_ii_l)+iii_v_l, wgy-ii*d ),rotation=180, x_reflection=True))
    combined_cell.add(gdspy.CellReference(nfc,origin=(0,-ii*d))) 
    combined_cell.add(gdspy.CellReference(nfc,origin=(2*wgx + 2*(taper_ii_l)+iii_v_l, wgy-ii*d ),rotation=180, x_reflection=True))


combined_cell.add(gdspy.CellReference(amc,origin=(-alL,alL)))
combined_cell.add(gdspy.CellReference(amc,origin=(+alL+final_pos[0],-final_pos[1]-alL)))



## ------------------------------------------------------------------ ##
##	OUTPUT															  ##
## ------------------------------------------------------------------ ##

## Output the layout to a GDSII file (default to all created cells).
## Set the units we used to micrometers and the precision to nanometers.
gdspy.gds_print(name +  '_mod.gds', unit=1.0e-6, precision=1.0e-9)
print('Sample gds file saved: ' + name + '_mod.gds')


## ------------------------------------------------------------------ ##
##	VIEWER															  ##
## ------------------------------------------------------------------ ##

## View the layout using a GUI.  Full description of the controls can
## be found in the online help at http://gdspy.sourceforge.net/
#gdspy.LayoutViewer()

