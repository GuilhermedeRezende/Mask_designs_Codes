
import os
import numpy
import gdspy
from numpy import *

print('Using gdspy module version ' + gdspy.__version__)


name = (os.path.abspath(os.path.dirname(os.sys.argv[0]))) + os.sep + 'teste_racetracks'

print('Creating layout')


## ------------------------------------------------------------------ ##
##  DEFINITIONS                                                       ##
## ------------------------------------------------------------------ ##

# Define boolean operations
subtraction = lambda p1, p2: p1 and not p2
summ = lambda p1, p2: p1 or p2
intersection = lambda p1, p2: p1 and p2

##-------------------------------------------------------------##
##        PARAMETERS
##-------------------------------------------------------------##
l           = 1.0                   # square side                           [um]
radius      = 16.0                  # racetrack radius                      [um]
wth_race    = 0.45                  # racetrack width                       [um]
ratio_race  = 1.0                   # racetrack ratio distance/radius       [um]
gap_ring    = 0.2                   # gap btw racetrack and rings           [um]
disp_ratio  = 0.0                   # displacemente of rings centers (0,1)  [um]
gap_mol     = 0.2                   # gap btw wvguide and resonators        [um]
wth_tap     = 0.15                  # taper width                           [um]
lth_lin     = 50.0                  # linear end part length                [um]
lth_tap     = 50.0                  # taper length                          [um]
lth_wv     = 370.0                  # waveguide length vert - part          [um]
wth_wv      = 0.45                  # waveguide width                       [um]
r_wv        = 30.0                  # waveguide bend radius                 [um]
lth_wvh     = 370.0                 # waveguide length horizontal           [um]

dspl_wavh   = 5.0                   # displacement btween devices           [um]



##-------------------------------------------------------------##
##        FUNCTIONS
##-------------------------------------------------------------##

def draw_racetrack(layer_num,center,mean_radius,w, l_ratio):
    rectangle1 = gdspy.Rectangle((mean_radius*l_ratio,-mean_radius-w/2.0)+center,(-mean_radius*l_ratio,-mean_radius+w/2.0)+center,layer=layer_num)
    arcsec1 = gdspy.Round((-l_ratio*mean_radius,0)+center,mean_radius+w/2.0,mean_radius-w/2.0, initial_angle=numpy.pi/2.0, final_angle=3.0*numpy.pi/2.0,number_of_points=2000,max_points=199,layer=layer_num)
    rectangle2 = gdspy.Rectangle((-mean_radius*l_ratio,mean_radius+w/2.0)+center,(mean_radius*l_ratio,mean_radius-w/2.0,radius-w/2.0)+center,layer=layer_num)
    arcsec2 = gdspy.Round((l_ratio*mean_radius,0)+center,mean_radius+w/2.0,mean_radius-w/2.0, initial_angle=-numpy.pi/2.0, final_angle=numpy.pi/2.0,number_of_points=2000,max_points=199,layer=layer_num)
    bool = gdspy.boolean([rectangle1,arcsec1],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,rectangle2],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,arcsec2],summ,max_points=199,layer=layer_num)
    return bool

def draw_racedring(layer_num,center,mean_radius,w, l_ratio,gap,displ_ratio):
    race1 = draw_racetrack(layer_num,center,mean_radius,w, l_ratio)
    ring1 = gdspy.Round((-displ_ratio*mean_radius/2.0,mean_radius/2.0 - w - gap)+center,mean_radius/2.0+w/2.0,mean_radius/2.0-w/2.0, initial_angle=0, final_angle=2.0*numpy.pi,number_of_points=2000,max_points=199,layer=layer_num)
    ring2 = gdspy.Round((displ_ratio*mean_radius/2.0,3.0*mean_radius/2.0 + w + gap)+center,mean_radius/2.0+w/2.0,mean_radius/2.0-w/2.0, initial_angle=0, final_angle=2.0*numpy.pi,number_of_points=2000,max_points=199,layer=layer_num)
    bool = gdspy.boolean([race1,ring1],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,ring2],summ,max_points=199,layer=layer_num)
    return bool

def draw_raceref(layer_num,center,mean_radius,w, l_ratio,gap):
    race1 = draw_racetrack(layer_num,center,mean_radius,w, l_ratio)
    ring1 = gdspy.Round((0,3.0*mean_radius/2.0 + w + gap)+center,mean_radius/2.0+w/2.0,mean_radius/2.0-w/2.0, initial_angle=0, final_angle=2.0*numpy.pi,number_of_points=2000,max_points=199,layer=layer_num)
    ring2 = gdspy.Round((0,-mean_radius/2.0 + w + gap)+center,mean_radius/2.0+w/2.0,mean_radius/2.0-w/2.0, initial_angle=0, final_angle=2.0*numpy.pi,number_of_points=2000,max_points=199,layer=layer_num)
    bool = gdspy.boolean([race1,ring1],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,ring2],summ,max_points=199,layer=layer_num)
    return bool

def draw_waveguide(layer_num,center,lin_l,tap_w,tap_l,wv_w,wv_l,wv_r,wv_h,l_sq):
    sq1 = gdspy.Rectangle((0,l_sq+lin_l+tap_l+wv_l+wv_r+wv_r+wv_l+tap_l+lin_l+l_sq)+center,(l_sq,l_sq+lin_l+tap_l+wv_l+wv_r+wv_r+wv_l+tap_l+lin_l)+center,layer=layer_num)
    rect1 = gdspy.Rectangle((l_sq/2.0-tap_w/2.0,l_sq+lin_l+tap_l+wv_l+wv_r+wv_r+wv_l+tap_l+lin_l)+center,(l_sq/2.0+tap_w/2.0,l_sq+lin_l+tap_l+wv_l+wv_r+wv_r+wv_l+tap_l)+center,layer=layer_num)
    trap1 = gdspy.Polygon([(l_sq/2.0-tap_w/2.0,l_sq+lin_l+tap_l+wv_l+wv_r+wv_r+wv_l+tap_l)+center,(l_sq/2.0-wv_w/2.0,l_sq+lin_l+tap_l+wv_l+wv_r+wv_r+wv_l)+center,(l_sq/2.0+wv_w/2.0,l_sq+lin_l+tap_l+wv_l+wv_r+wv_r+wv_l)+center,(l_sq/2.0+tap_w/2.0,l_sq+lin_l+tap_l+wv_l+wv_r+wv_r+wv_l+tap_l)+center],layer=layer_num)
    rect2 = gdspy.Rectangle((l_sq/2.0-wv_w/2.0,l_sq+lin_l+tap_l+wv_l+wv_r+wv_r+wv_l)+center,(l_sq/2.0+wv_w/2.0,l_sq+lin_l+tap_l+wv_l+wv_r+wv_r)+center,layer=layer_num)
    ben1 = gdspy.Round((l_sq/2.0+wv_r,l_sq+lin_l+tap_l+wv_l+wv_r+wv_r)+center,wv_w/2.0+wv_r,wv_r-wv_w/2.0, initial_angle=1.0*numpy.pi, final_angle=3.0*numpy.pi/2.0,number_of_points=2000,max_points=199,layer=layer_num)
    wghor = gdspy.Rectangle((l_sq/2.0+wv_r,l_sq+lin_l+tap_l+wv_l+wv_r+wv_w/2.0)+center,(l_sq/2.0+wv_r+wv_h,l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0)+center,layer=layer_num)
    ben2 = gdspy.Round((l_sq/2.0+wv_r+wv_h,l_sq+lin_l+tap_l+wv_l)+center,wv_w/2.0+wv_r,wv_r-wv_w/2.0, initial_angle=0.0*numpy.pi, final_angle=1.0*numpy.pi/2.0,number_of_points=2000,max_points=199,layer=layer_num)
    rect3 = gdspy.Rectangle((l_sq/2.0+wv_r+wv_h+wv_r-wv_w/2.0,l_sq+lin_l+tap_l+wv_l)+center,(l_sq/2.0+wv_r+wv_h+wv_r+wv_w/2.0,l_sq+lin_l+tap_l)+center,layer=layer_num)
    trap2 = gdspy.Polygon([(l_sq/2.0+wv_r+wv_h+wv_r-wv_w/2.0,l_sq+lin_l+tap_l)+center,(l_sq/2.0+wv_r+wv_h+wv_r-tap_w/2.0,l_sq+lin_l)+center,(l_sq/2.0+wv_r+wv_h+wv_r+tap_w/2.0,l_sq+lin_l)+center,(l_sq/2.0+wv_r+wv_h+wv_r+wv_w/2.0,l_sq+lin_l+tap_l)+center],layer=layer_num)
    rect4 = gdspy.Rectangle((l_sq/2.0+wv_r+wv_h+wv_r-tap_w/2.0,l_sq+lin_l)+center,(l_sq/2.0+wv_r+wv_h+wv_r+tap_w/2.0,l_sq)+center,layer=layer_num)
    sq2 = gdspy.Rectangle((l_sq/2.0+wv_r+wv_h+wv_r-l_sq/2.0,l_sq)+center,(l_sq/2.0+wv_r+wv_h+wv_r+l_sq/2.0,0)+center,layer=layer_num)

    bool = gdspy.boolean([sq1,rect1],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,trap1],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,rect2],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,ben1],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,wghor],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,ben2],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,rect3],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,trap2],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,rect4],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,sq2],summ,max_points=199,layer=layer_num)
    return bool

def draw_squares(layer_num,center):
    sqr = gdspy.Rectangle((0,0)+center,(1,1)+center,layer=layer_num)
    bool = gdspy.boolean([sqr,sqr],summ,max_points=199,layer=layer_num)
    for ii in range(1,10):
        sqr2 = gdspy.Rectangle((0,7.0*ii)+center,(1,1+7.0*ii)+center,layer=layer_num)
        bool = gdspy.boolean([bool,sqr2],summ,max_points=199,layer=layer_num)
    return bool

def draw_devices(layer_num,center,lin_l,tap_w,tap_l,wv_w,wv_l,wv_r,wv_h,l_sq,mean_radius,w, l_ratio,gap,displ_ratio,dspl_wavh,gap_mol):
    d1w = draw_waveguide(layer_num,center,lin_l,tap_w,tap_l,wv_w,wv_l,wv_r,wv_h,l_sq)
    d1d = draw_racedring(layer_num,(5,5),mean_radius,w, l_ratio,gap,displ_ratio)
    d1sq = draw_squares(layer_num,center+(l_sq/2.0+wv_r+wv_h+wv_r+wv_w/2.0,0))
    bool = gdspy.boolean([d1w,d1d],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,d1sq],summ,max_points=199,layer=layer_num)
    return bool
    
	
    	
## ------------------------------------------------------------------ ##
##  DRAWING                                                           ##
## ------------------------------------------------------------------ ##

# Layers
layer_vector = [1] # order: disks, bullseye mod a, bullseye mod wRing, idmarks, working area, align marks

# Create a cell for the unit element
unit_cell1 = gdspy.Cell('testcell')


unit_cell1.add(draw_devices(1,(0,0),lth_lin,wth_tap,lth_tap,wth_wv,lth_wv,r_wv,lth_wvh,l,radius,wth_race,ratio_race,gap_ring,disp_ratio,dspl_wavh,gap_mol))

			
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
