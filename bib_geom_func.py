
import os
import numpy
import gdspy
from numpy import *
import imecsetup as ims

print('Using gdspy module version ' + gdspy.__version__)


name = (os.path.abspath(os.path.dirname(os.sys.argv[0]))) + os.sep + 'rezendev2'

print('Creating layout')

# This bib contains a bunch of geometric forms used in LPD's designs  


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
sq_l           = 1.0                   # square side                        [um]
race_r      = 16.0                  # racetrack radius                      [um]
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

#Hint: Arguments in functions have the same name of parameters, without _.

##-------------------------------------------------------------##
##        FUNCTIONS
##-------------------------------------------------------------##


def draw_racetrack(layer_num,origin,racer,racew, raced):
    #Inputs:
    #layer_num:         layer number
    #origin:            figure position
    #racer              racetrack bend part inner radius
    #racew              racetrack width
    #raced              racetrack linear semilength

    #Description: This function draws a (horizontal) racetrack of width racew, inner radius racer and linear semilength raced, which center is localized at point origin.

    #Output: bool,a gdspy object
    rec1 = gdspy.Rectangle(numpy.array([-raced,-racer-racew])+numpy.array(origin),numpy.array([raced,racer+racew])+numpy.array(origin),layer=layer_num)                                                     # external rectangle
    rec2 = gdspy.Rectangle(numpy.array([-raced,-racer])+numpy.array(origin),numpy.array([raced,racer])+numpy.array(origin),layer=layer_num)                                                                 # internal rectangle (to be subtracte)
    ansec1 = gdspy.Round(numpy.array([-raced,0])+numpy.array(origin),racer+racew,racer, initial_angle=numpy.pi/2.0, final_angle=3.0*numpy.pi/2.0,number_of_points=pow(2,12)-1,max_points=pow(2,12)-1,layer=layer_num)      # left side semi annular section
    ansec2 = gdspy.Round(numpy.array([raced,0])+numpy.array(origin),racer+racew,racer, initial_angle=-numpy.pi/2.0, final_angle=numpy.pi/2.0,number_of_points=pow(2,12)-1,max_points=pow(2,12)-1,layer=layer_num)          # right side semi annular section
    bool = gdspy.boolean([rec1,rec2],subtraction,max_points=pow(2,12)-1,layer=layer_num)
    bool = gdspy.boolean([bool,ansec1],summ,max_points=pow(2,12)-1,layer=layer_num)
    bool = gdspy.boolean([bool,ansec2],summ,max_points=pow(2,12)-1, **ims.wgcor)
    return bool

def draw_stadium(layer_num,origin,star, stad):
    #Inputs:
    #layer_num:         layer number
    #origin:            figure position
    #star               stadium bent part radius
    #stad               stadium linear semilength

    #Description: This function draws a (horizontal) stadium of width racew and linear semilength raced, which center is localized at point origin.

    #Output: bool,a gdspy object
    
    rec = gdspy.Rectangle(numpy.array([-stad,-star])+numpy.array(origin),numpy.array([stad,star])+numpy.array(origin),layer=layer_num)                                                                      # rectangle part
    csec1 = gdspy.Round(numpy.array([-stad,0])+numpy.array(origin),star,0, initial_angle=numpy.pi/2.0, final_angle=3.0*numpy.pi/2.0,number_of_points=pow(2,12)-1,max_points=pow(2,12)-1,layer=layer_num)                   # left side semi circular section
    csec2 = gdspy.Round(numpy.array([stad,0])+numpy.array(origin),star,0, initial_angle=-numpy.pi/2.0, final_angle=numpy.pi/2.0,number_of_points=pow(2,12)-1,max_points=pow(2,12)-1,layer=layer_num)                       # right side semi circular section
    bool = gdspy.boolean([rec,csec1],summ,max_points=pow(2,12)-1,layer=layer_num)
    bool = gdspy.boolean([bool,csec2],summ,max_points=pow(2,12)-1,**ims.wgcor)
    bool = bool.rotate(numpy.pi/2)
    return bool

def draw_mushroom(layer_num,origin,star):
    #Inputs:
    #layer_num:         layer number
    #origin:            figure position
    #star               stadium bent part radius
    
    #Description: This function draws a (horizontal) mushroom of width racew and linear semilength raced, which center is localized at point origin.

    #Output: bool,a gdspy object
    
    rec = gdspy.Rectangle(numpy.array([-star,-star/2])+numpy.array(origin),numpy.array([0,star/2])+numpy.array(origin),layer=layer_num)                                                                      # rectangle part
    csec1 = gdspy.Round(numpy.array([-star,0])+numpy.array(origin),star,0, initial_angle=numpy.pi/2.0, final_angle=3.0*numpy.pi/2.0,number_of_points=pow(2,12)-1,max_points=pow(2,12)-1,layer=layer_num)                   # left side semi circular section
    bool = gdspy.boolean([rec,csec1],summ,max_points=pow(2,12)-1,**ims.wgcor).rotate(numpy.pi/2.0)
    return bool

def draw_racedring(layer_num,origin,rrgap,ringp):
    ##  PARAMETERS
    race_r = 20             # racetrack bent part inner radius          [um]
    race_w = 0.45            # racetrack width                           [um]
    race_d = 20             # racetrack linear semilength               [um]

    #Inputs:
    #layer_num:         layer number
    #origin:            figure position
    #rrgap              gap between racetrack and ring
    #ringp              ring position parameter

    #Description: This function draws a (horizontal) racetrack of width race_w and linear semilength race_d, which center is localized at point origin. Also, it draws an inner microring and an outter one, with the same width and radii equals a half of racetrack radius.
    #The microrings are posicioned at the linear part of the racetrack, with a gap of rrgap. Their centers move in oposite direction, through the ringp parameter (0,1), so that 0 stands for align centers and 1 stands for a lngth difference of 2 microring's radius
    
    #Output: bool,a gdspy object

    
    race1 = draw_racetrack(layer_num,origin,race_r,race_w, race_d)
    ring1 = gdspy.Round(numpy.array(origin)+numpy.array([ringp*race_r/2.0,race_r+2.0*race_w+rrgap+race_r/2.0]),race_r/2.0+race_w,race_r/2.0, initial_angle=0.0, final_angle=2.0*numpy.pi,number_of_points=pow(2,12)-1,max_points=pow(2,12)-1,layer=layer_num)
    ring2 = gdspy.Round(numpy.array(origin)+numpy.array([-ringp*race_r/2.0,race_r-race_w-rrgap-race_r/2.0]),race_r/2.0+race_w,race_r/2.0,initial_angle=0.0, final_angle=2.0*numpy.pi,number_of_points=pow(2,12)-1,max_points=pow(2,12)-1,layer=layer_num)
    bool = gdspy.boolean([race1,ring1],summ,max_points=pow(2,12)-1,layer=layer_num)
    bool = gdspy.boolean([bool,ring2],summ,max_points=pow(2,12)-1,**ims.wgcor)
    bool = bool.rotate(numpy.pi/2)
    return bool

def draw_cring(layer_num,origin,gap):
     ##  PARAMETERS
    race_r = 20             # racetrack bent part inner radius          [um]
    race_w = 0.45            # racetrack width                           [um]
    ring_i = 9.4
    # racetrack linear semilength               [um]

    #Inputs:
    #layer_num:         layer number
    #origin:            figure position
    #rrgap              gap between racetrack and ring
    #ringp              ring position parameter

    #Description: This function draws a (horizontal) racetrack of width race_w and linear semilength race_d, which center is localized at point origin. Also, it draws an inner microring and an outter one, with the same width and radii equals a half of racetrack radius.
    #The microrings are posicioned at the linear part of the racetrack, with a gap of rrgap. Their centers move in oposite direction, through the ringp parameter (0,1), so that 0 stands for align centers and 1 stands for a lngth difference of 2 microring's radius
    
    #Output: bool,a gdspy object

    
    ring0 = gdspy.Round(numpy.array(origin)+numpy.array([0,0]),race_r+race_w,race_r, initial_angle=0.0, final_angle=2.0*numpy.pi,number_of_points=pow(2,12)-1,max_points=pow(2,12)-1,layer=layer_num)
    ring1 = gdspy.Round(numpy.array(origin)+numpy.array([0,-gap-race_w-ring_i]),ring_i+race_w,ring_i, initial_angle=0.0, final_angle=2.0*numpy.pi,number_of_points=pow(2,12)-1,max_points=pow(2,12)-1,layer=layer_num)
    ring2 = gdspy.Round(numpy.array(origin)+numpy.array([0,gap+race_w+ring_i]),ring_i+race_w,ring_i, initial_angle=0.0, final_angle=2.0*numpy.pi,number_of_points=pow(2,12)-1,max_points=pow(2,12)-1,layer=layer_num)
    bool = gdspy.boolean([ring0,ring1],summ,max_points=pow(2,12)-1,layer=layer_num)
    bool = gdspy.boolean([bool,ring2],summ,max_points=pow(2,12)-1,**ims.wgcor)
    bool = bool.rotate(numpy.pi/2)
    return bool

def draw_waveguide(layer_num,origin,n,N):
 ##PARAMETERS
    l_sq = 1               # protection square side                    [um]
    lin_l = 49             # linear tapped waveguide length            [um]
    tap_w = 0.15           # linear tapped waveguide width             [um]
    tap_l = 50             # tapper length                             [um]
    wv_w =  0.45           # waveguide width                           [um]
    wv_l = 300             # waveguide length                          [um]
    wv_r = 30              # waveguide bend region radius              [um]
    wv_v = 900             # waveguide vertical region length          [um]
    vgap = 0              # vertical gap between waveguides           [um]
    hgap = 10              # horizontal gap between waveguides         [um]
    

    #Inputs:
    #layer_num:         layer number
    #origin:            figure position
    #n                  waveguide number
    

    #Description: This function draws a (horizontal) waveguide of width wv_w and tapered ends with width tap_w and length tap_l plus a square of size. The waveguides have a S-shape, so that the ends are vertically separeted by wv_v
    
    
    #Output: bool,a gdspy object

    sq1 = gdspy.Rectangle(numpy.array([0,0])+numpy.array(origin),numpy.array([l_sq,l_sq])+numpy.array(origin),layer=layer_num)
    rect1 = gdspy.Rectangle(numpy.array([l_sq,l_sq/2.0 -tap_w/2.0])+numpy.array(origin),numpy.array([l_sq+lin_l,l_sq/2.0 +tap_w/2.0])+numpy.array(origin),layer=layer_num)
    trap1 = gdspy.Polygon([numpy.array([l_sq+lin_l,l_sq/2.0 -tap_w/2.0])+numpy.array(origin),numpy.array([l_sq+lin_l,l_sq/2.0 +tap_w/2.0])+numpy.array(origin),numpy.array([l_sq+lin_l+tap_l,l_sq/2.0 +wv_w/2.0])+numpy.array(origin),numpy.array([l_sq+lin_l+tap_l,l_sq/2.0 -wv_w/2.0])+numpy.array(origin)],layer = layer_num)
    rect2 = gdspy.Rectangle(numpy.array([l_sq+lin_l+tap_l,l_sq/2.0 -wv_w/2.0])+numpy.array(origin),numpy.array([l_sq+lin_l+tap_l+wv_l,l_sq/2.0 +wv_w/2.0])+numpy.array(origin)-numpy.array([hgap*(N-n),0]),layer=layer_num)
    ben1 = gdspy.Round(numpy.array([l_sq+lin_l+tap_l+wv_l,l_sq/2.0 +wv_r])+numpy.array(origin)-numpy.array([hgap*(N-n),0]),wv_r+wv_w/2.0,wv_r-wv_w/2.0,initial_angle=-numpy.pi/2.0, final_angle=0,number_of_points=pow(2,12)-1,max_points=pow(2,12)-1,layer=layer_num)                                     
    wgver = gdspy.Rectangle(numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0,l_sq/2.0 +wv_r])+numpy.array(origin)-numpy.array([hgap*(N-n),0]),numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w,l_sq/2.0 +wv_r+ wv_v])+numpy.array(origin)-numpy.array([hgap*(N-n),vgap*n]),layer=layer_num)
    ben2 = gdspy.Round(numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r,l_sq/2.0 +wv_r+ wv_v])+numpy.array(origin)-numpy.array([hgap*(N-n),vgap*n]),wv_r+wv_w/2.0,wv_r-wv_w/2.0,initial_angle=numpy.pi/2.0, final_angle=numpy.pi,number_of_points=pow(2,12)-1,max_points=pow(2,12)-1,layer=layer_num)
    rect3 = gdspy.Rectangle(numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r,l_sq/2.0 +wv_r+ wv_v+wv_r+wv_w/2.0])+numpy.array(origin)-numpy.array([hgap*(N-n),vgap*n]),numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r+wv_l,l_sq/2.0 +wv_r+ wv_v+wv_r-wv_w/2.0])+numpy.array(origin)-numpy.array([0,vgap*n]),layer=layer_num)
    trap2 = gdspy.Polygon([numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r+wv_l,l_sq/2.0 +wv_r+ wv_v+wv_r-wv_w/2.0])+numpy.array(origin)-numpy.array([0,vgap*n]),numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r+wv_l,l_sq/2.0 +wv_r+ wv_v+wv_r+wv_w/2.0])+numpy.array(origin)-numpy.array([0,vgap*n]),numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r+wv_l+tap_l,l_sq/2.0 +wv_r+ wv_v+wv_r+tap_w/2.0])+numpy.array(origin)-numpy.array([0,vgap*n]),numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r+wv_l+tap_l,l_sq/2.0 +wv_r+ wv_v+wv_r-tap_w/2.0])+numpy.array(origin)-numpy.array([0,vgap*n])],layer = layer_num)
    rect4 = gdspy.Rectangle(numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r+wv_l+tap_l,l_sq/2.0 +wv_r+ wv_v+wv_r-tap_w/2.0])+numpy.array(origin)-numpy.array([0,vgap*n]),numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r+wv_l+tap_l+lin_l,l_sq/2.0 +wv_r+ wv_v+wv_r+tap_w/2.0])+numpy.array(origin)-numpy.array([0,vgap*n]),layer=layer_num)
    sq2 = gdspy.Rectangle(numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r+wv_l+tap_l+lin_l,l_sq/2.0 +wv_r+ wv_v+wv_r+l_sq/2.0])+numpy.array(origin)-numpy.array([0,vgap*n]),numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r+wv_l+tap_l+lin_l+l_sq,l_sq/2.0 +wv_r+ wv_v+wv_r-l_sq/2.0])+numpy.array(origin)-numpy.array([0,vgap*n]),layer=layer_num)
   

    bool = gdspy.boolean([sq1,rect1],summ,max_points=pow(2,12)-1,layer=layer_num)
    bool = gdspy.boolean([bool,trap1],summ,max_points=pow(2,12)-1,layer=layer_num)
    bool = gdspy.boolean([bool,rect2],summ,max_points=pow(2,12)-1,layer=layer_num)
    bool = gdspy.boolean([bool,ben1],summ,max_points=pow(2,12)-1,layer=layer_num)
    bool = gdspy.boolean([bool,wgver],summ,max_points=pow(2,12)-1,layer=layer_num)
    bool = gdspy.boolean([bool,ben2],summ,max_points=pow(2,12)-1,layer=layer_num)
    bool = gdspy.boolean([bool,rect3],summ,max_points=pow(2,12)-1,layer=layer_num)
    bool = gdspy.boolean([bool,trap2],summ,max_points=pow(2,12)-1,layer=layer_num)
    bool = gdspy.boolean([bool,rect4],summ,max_points=pow(2,12)-1,layer=layer_num)
    bool = gdspy.boolean([bool,sq2],summ,max_points=pow(2,12)-1,**ims.wgcor)
    return bool

def draw_bondaries(layer_num,origin,n,N):
 ##PARAMETERS
    y_shift = -10
    l_width = 20                # 
    l_sq = 0              # protection square side                    [um]
    
    lin_l = 50              # linear tapped waveguide length            [um]
    tap_w = 0              # linear tapped waveguide width             [um]
    tap_l = 50             # tapper length                             [um]
    wv_w =  5.45           # waveguide width                           [um]
    wv_l = 300             # waveguide length                          [um]
    wv_r = 30              # waveguide bend region radius              [um]
    wv_v = 900             # waveguide vertical region length          [um]
    vgap = 0              # vertical gap between waveguides           [um]
    hgap = 10              # horizontal gap between waveguides         [um]
    

    #Inputs:
    #layer_num:         layer number
    #origin:            figure position
    #n                  waveguide number
    

    #Description: This function draws a (horizontal) waveguide of width wv_w and tapered ends with width tap_w and length tap_l plus a square of size. The waveguides have a S-shape, so that the ends are vertically separeted by wv_v
    
    
    #Output: bool,a gdspy object

    sq1 = gdspy.Rectangle(numpy.array([0,0+y_shift])+numpy.array(origin),numpy.array([lin_l,l_width+y_shift])+numpy.array(origin),layer=layer_num)
    trap1 = gdspy.Polygon([numpy.array([lin_l,l_width+y_shift])+numpy.array(origin),numpy.array([lin_l+tap_l,l_width/2.0 +wv_w/2.0+y_shift])+numpy.array(origin),numpy.array([lin_l+tap_l,l_width/2.0 -wv_w/2.0+y_shift])+numpy.array(origin),numpy.array([lin_l,0+y_shift])+numpy.array(origin)],layer = layer_num)
    rect2 = gdspy.Rectangle(numpy.array([l_sq+lin_l+tap_l,l_sq/2.0 -wv_w/2.0])+numpy.array(origin),numpy.array([l_sq+lin_l+tap_l+wv_l,l_sq/2.0 +wv_w/2.0])+numpy.array(origin)-numpy.array([hgap*(N-n),0]),layer=layer_num)
    ben1 = gdspy.Round(numpy.array([l_sq+lin_l+tap_l+wv_l,l_sq/2.0 +wv_r])+numpy.array(origin)-numpy.array([hgap*(N-n),0]),wv_r+wv_w/2.0,wv_r-wv_w/2.0,initial_angle=-numpy.pi/2.0, final_angle=0,number_of_points=pow(2,12)-1,max_points=pow(2,12)-1,layer=layer_num)                                     
    wgver = gdspy.Rectangle(numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0,l_sq/2.0 +wv_r])+numpy.array(origin)-numpy.array([hgap*(N-n),0]),numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w,l_sq/2.0 +wv_r+ wv_v])+numpy.array(origin)-numpy.array([hgap*(N-n),vgap*n]),layer=layer_num)
    ben2 = gdspy.Round(numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r,l_sq/2.0 +wv_r+ wv_v])+numpy.array(origin)-numpy.array([hgap*(N-n),vgap*n]),wv_r+wv_w/2.0,wv_r-wv_w/2.0,initial_angle=numpy.pi/2.0, final_angle=numpy.pi,number_of_points=pow(2,12)-1,max_points=pow(2,12)-1,layer=layer_num)
    rect3 = gdspy.Rectangle(numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r,l_sq/2.0 +wv_r+ wv_v+wv_r+wv_w/2.0])+numpy.array(origin)-numpy.array([hgap*(N-n),vgap*n]),numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r+wv_l,l_sq/2.0 +wv_r+ wv_v+wv_r-wv_w/2.0])+numpy.array(origin)-numpy.array([0,vgap*n]),layer=layer_num)
    trap2 = gdspy.Polygon([numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r+wv_l,l_sq/2.0 +wv_r+ wv_v+wv_r-wv_w/2.0])+numpy.array(origin)-numpy.array([0,vgap*n]),numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r+wv_l,l_sq/2.0 +wv_r+ wv_v+wv_r+wv_w/2.0])+numpy.array(origin)-numpy.array([0,vgap*n]),numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r+wv_l+tap_l,l_sq/2.0 +wv_r+ wv_v+wv_r+l_width/2.0])+numpy.array(origin)-numpy.array([0,vgap*n]),numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r+wv_l+tap_l,l_sq/2.0 +wv_r+ wv_v+wv_r-l_width/2.0])+numpy.array(origin)-numpy.array([0,vgap*n])],layer = layer_num)
    sq2 = gdspy.Rectangle(numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r+wv_l+tap_l,l_sq/2.0 +wv_r+ wv_v+wv_r-l_width/2.0])+numpy.array(origin)-numpy.array([0,vgap*n]),numpy.array([l_sq+lin_l+tap_l+wv_l+wv_r-wv_w/2.0+wv_w/2.0+wv_r+wv_l+tap_l+tap_l,l_sq/2.0 +wv_r+ wv_v+wv_r+l_width/2.0])+numpy.array(origin)-numpy.array([0,vgap*n]),layer=layer_num)
   

    
    bool = gdspy.boolean([sq1,trap1],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,rect2],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,ben1],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,wgver],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,ben2],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,rect3],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,trap2],summ,max_points=199,layer=layer_num)
    bool = gdspy.boolean([bool,sq2],summ,max_points=199, **ims.wgcld)
    return bool


def draw_squares(layer_num,origin,n,N):
 ##PARAMETERS
    x_shift = 650
    y_shift = 962.625                # 
    l_sq = 90              # protection square side                    [um]
   
    

    #Inputs:
    #layer_num:         layer number
    #origin:            figure position
    #n                  waveguide number
    

    #Description: This function draws a (horizontal) waveguide of width wv_w and tapered ends with width tap_w and length tap_l plus a square of size. The waveguides have a S-shape, so that the ends are vertically separeted by wv_v
    
    
    #Output: bool,a gdspy object

    bool = gdspy.Rectangle(numpy.array([x_shift,y_shift])+numpy.array(origin),numpy.array([x_shift+l_sq,y_shift+l_sq])+numpy.array(origin),**ims.wgcld)
    return bool
    
	
    	
## ------------------------------------------------------------------ ##
##  DRAWING                                                           ##
## ------------------------------------------------------------------ ##

# Layers
layer_vector = [1] # order: disks, bullseye mod a, bullseye mod wRing, idmarks, working area, align marks

# Create a cell for the unit element
unit_cell1 = gdspy.Cell('waveguides')
vetor=[]
dpmet = numpy.array([1001.375,-700])
outfunc=[draw_racedring(1,dpmet,0.2,0),draw_racedring(1,dpmet+numpy.array([-100,0]),0.2,0),draw_racedring(1,dpmet+numpy.array([-200,0]),0.2,0),draw_racedring(1,dpmet+numpy.array([-300,0]),0.2,0.01),draw_racedring(1,dpmet+numpy.array([-400,0]),0.2,0.01),draw_racedring(1,dpmet+numpy.array([-500,0]),0.2,0.01),draw_racedring(1,dpmet+numpy.array([-600,0]),0.2,0.35),draw_racedring(1,dpmet+numpy.array([-700,0]),0.2,0.35),draw_racedring(1,dpmet+numpy.array([-800,0]),0.2,0.35),draw_racedring(1,dpmet+numpy.array([-900,0]),0.2,1.0),draw_racedring(1,dpmet+numpy.array([-1000,0]),0.2,1.0),draw_racedring(1,dpmet+numpy.array([-1100,0]),0.2,1.0),draw_stadium(1,dpmet+numpy.array([-1200.45,0]),20,20),draw_stadium(1,dpmet+numpy.array([-1696,1018.975]),20,20).rotate(numpy.pi/2),draw_cring(1,dpmet+numpy.array([-1420,0]),0.075),draw_cring(1,dpmet+numpy.array([-1520,0]),0.1),draw_cring(1,dpmet+numpy.array([-1620,0]),0.125)]
outfunc2 = [draw_cring(1,dpmet+numpy.array([-1420,100]),0.075),draw_cring(1,dpmet+numpy.array([-1520,100]),0.1),draw_cring(1,dpmet+numpy.array([-1620,100]),0.125)]


for x in range(0,17):
    unit_cell1.add(draw_waveguide(1,(0,-100*x),x,17))
    unit_cell1.add(draw_squares(2,(0,-100*x),x,17))
    unit_cell1.add(draw_bondaries(2,(0,-100*x),x,17))
    unit_cell1.add(outfunc[x])

for x in range(14,17):
    unit_cell1.add(draw_squares(2,(-100,-100*x),x,17))
    unit_cell1.add(outfunc2[x-14])

for x in range(3,6):
    unit_cell1.add(draw_squares(2,(-600,280-100*x),x,17))
    unit_cell1.add(draw_mushroom(1,(+500+100*x,-100),15))    

    
    
	
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
