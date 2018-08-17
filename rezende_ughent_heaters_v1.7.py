# -*- coding: cp1252 -*-
import os
import numpy
import gdspy
import imecsetup as ims
from numpy import *

print('Using gdspy module version ' + gdspy.__version__)
name = (os.path.abspath(os.path.dirname(os.sys.argv[0]))) + os.sep + 'rezende_heaters_v1'

## ------------------------------------------------------------------ ##
##	IMPORT															  ##
## ------------------------------------------------------------------ ##

gdsii = gdspy.GdsImport('rezende_heaters_pad_TiAu.gds')
tiau_cell = gdsii.extract('Ti_Au')

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
hh= 20.0 #nicr heater height
ang = pi/6.0 # 30° heater
sqr = 10.0




def nicrheat(layer_num,center,radius,hw,hh,ang,sqr):
    pos1 = (center[0]-radius*sin(ang),center[1]-radius*cos(ang))
    pos2 = (center[0]+radius*sin(ang),center[1]-radius*cos(ang))
                                
                                                             
    nch1=gdspy.Round(center,radius+hw/2,radius-hw/2,initial_angle=-ang-pi/2.0, final_angle=ang-pi/2.0,layer=layer_num,max_points=4094,number_of_points=0.1)
    nch2=gdspy.Rectangle((pos1[0]+hw,pos1[1]),(pos1[0],pos1[1]-hh),layer=layer_num)
    nch3=gdspy.Rectangle((pos2[0]-hw,pos2[1]),(pos2[0],pos2[1]-hh),layer=layer_num)

    nch4=gdspy.Rectangle((pos1[0]+hw/2.0+sqr/2.0,pos1[1]-hh),(pos1[0]+hw/2.0-sqr/2.0,pos1[1]-hh-sqr),layer=layer_num)
    nch5=gdspy.Rectangle((pos2[0]-hw/2.0+sqr/2.0,pos2[1]-hh),(pos2[0]-hw/2.0-sqr/2.0,pos2[1]-hh-sqr),layer=layer_num)

    bool = gdspy.boolean([nch1,nch2],sum,max_points=4094,layer=layer_num)
    bool = gdspy.boolean([bool,nch3],sum,max_points=4094,layer=layer_num)
    bool = gdspy.boolean([bool,nch4],sum,max_points=4094,layer=layer_num)
    bool = gdspy.boolean([bool,nch5],sum,max_points=4094,layer=layer_num)

    return bool

def nicrheat2(layer_num,center,radius,hw,ang):
    pos1 = (center[0]-radius*sin(ang),center[1]-radius*cos(ang))
    pos2 = (center[0]+radius*sin(ang),center[1]-radius*cos(ang))
                                
                                                             
    nch1=gdspy.Round(center,radius+hw/2,radius-hw/2,initial_angle=-ang-pi/2.0, final_angle=ang-pi/2.0,layer=layer_num,max_points=4094,number_of_points=0.1)
    
    return nch1
	

def draw(gap):

    ## ------------------------------------------------------------------ ##
    ##	Define Cells						      ##
    ## ------------------------------------------------------------------ ##
    wg_cell = []
    nofill_cell = []
    cavity_cell = []
    gccell = []
    httiaucell = []
    htnicrcell = []

    del (wg_cell,nofill_cell,cavity_cell,gccell,httiaucell,htnicrcell)
    
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

       

    ## NiCr Heater Cell

    nccell = gdspy.Cell('Heater_Ni_Cr'+ str(2*n*(gap-gap0)/(gap0+gap1)))

    

  

    ## ------------------------------------------------------------------ ##
    ##	Layer Specification					      ##
    ## ------------------------------------------------------------------ ##

    spec = {'layer': 37, 'datatype': 4}  # Fully etched SOI: waveguide core
    spec2 = {'layer': 37, 'datatype': 5}  # Fully etched SOI: waveguide cladding (trench around core)
    spec3 = {'layer': 1158, 'datatype': 0}  # Area not to be filled with dummies (SOI,Poly or metal)
    spec4 = {'layer': 1, 'datatype': 0}  # NiCr mask
   
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

    cav12= gdspy.Rectangle( (pcavc[0]-r1-c_w2,pcavc[1]-r1-c_w2),(pcavc[0]+r1+c_w2,pcavc[1]+r1+c_w2),**spec2)

    #nofillc=gdspy.Rectangle( (waveguide.x-sec_gap-r1-taper_l-r1-wg_w2,waveguide.y-gap-0.5*wg_w-r1*2*(1.5-cos(pi/8.0))-r1-wg_w2),(waveguide.x-sec_gap-r1-taper_l+r1+wg_w2,waveguide.y-gap-0.5*wg_w-r1*2*(1.5-cos(pi/8.0))+r1+wg_w2),**spec3)
    #nofillw=gdspy.Rectangle( (-bragg_offset,-bragg_nofill/2.0-bragg_nfoffset),(waveguide.x,waveguide.y+bragg_nofill/2.0-bragg_nfoffset),**spec3)


#------ NiCr Heater  -----------------------------------------------#
    nch =  nicrheat(spec4['layer'],pcavc,r1,hw,hh,ang,sqr)
    nch2 =  nicrheat2(spec4['layer'],(pcavc[0]+r2+0.5*gap,pcavc[1]),r2,hw,ang)
    nch3 =  nicrheat2(spec4['layer'],(pcavc[0]-r2-0.5*gap,pcavc[1]),r2,hw,ang)
    #nch = gdspy.Rectangle( (pcavc[0]-r1-c_w2,pcavc[1]-r1-c_w2),(pcavc[0]+r1+c_w2,pcavc[1]+r1+c_w2),**spec4)
    

    ## ------------------------------------------------------------------ ##
    ##	Adding Objects into Cells				        	      ##
    ## ------------------------------------------------------------------ ##

    wg_cell.add(waveguide)  
    wg_cell.add(waveguide2) # Cell: Waveguide; Objects: waveguide+taper, waveguide trenching

    nofill_cell.add(nofill) #Cell: No fill; Objects: No tilling region
    

    cavity_cell.add(cav1)
    cavity_cell.add(cav2)
    cavity_cell.add(cav3)
    cavity_cell.add(cav12)  # Cell: Cavity; Objects: coupled rings, ring trenching

    nccell.add(nch)
    nccell.add(nch2)
    nccell.add(nch3)

    waveguidex=waveguide.x
    waveguidey=waveguide.y

    
    # --------- Taper sections --------------------------- #

    return (wg_cell,cavity_cell,gccell,nofill_cell,waveguidex,waveguidey,amcell,nccell)



combined_cell=gdspy.Cell('COMB1')

for ii in range(0,n,1):

    (wv,cc,gratc,nfc,wgx,wgy,amc,nc) = draw(gap0+gap_step*(ii))

    combined_cell.add(gdspy.CellReference(wv,origin=(0,-ii*d)))
    combined_cell.add(gdspy.CellReference(wv,origin=(2*wgx + 2*(taper_ii_l)+iii_v_l, wgy-ii*d ),rotation=180, x_reflection=True))
    combined_cell.add(gdspy.CellReference(cc,origin=(0,-ii*d)))
    combined_cell.add(gdspy.CellReference(cc,origin=(2*wgx + 2*(taper_ii_l)+iii_v_l, wgy-ii*d ),rotation=180, x_reflection=True))
    combined_cell.add(gdspy.CellReference(gratc,origin=(-sec_gap,-ii*d)))
    combined_cell.add(gdspy.CellReference(gratc,origin=(sec_gap+2*wgx + 2*(taper_ii_l)+iii_v_l, wgy-ii*d ),rotation=180, x_reflection=True))
    combined_cell.add(gdspy.CellReference(nfc,origin=(0,-ii*d))) 
    combined_cell.add(gdspy.CellReference(nfc,origin=(2*wgx + 2*(taper_ii_l)+iii_v_l, wgy-ii*d ),rotation=180, x_reflection=True))
    combined_cell.add(gdspy.CellReference(nc,origin=(0,-ii*d)))
    combined_cell.add(gdspy.CellReference(nc,origin=(2*wgx + 2*(taper_ii_l)+iii_v_l, wgy-ii*d ),rotation=180, x_reflection=True))
    
    combined_cell.add(gdspy.CellReference(tiau_cell,origin=(0,-ii*d)))
    combined_cell.add(gdspy.CellReference(tiau_cell,origin=(2*wgx + 2*(taper_ii_l)+iii_v_l, wgy-ii*d ),rotation=180, x_reflection=True))
    

combined_cell.add(gdspy.CellReference(amc,origin=(-alL,alL)))
combined_cell.add(gdspy.CellReference(amc,origin=(+alL+final_pos[0],-final_pos[1]-alL)))









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

