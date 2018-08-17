import os
import numpy
import gdspy
from numpy import *

print('Using gdspy module version ' + gdspy.__version__)


name = (os.path.abspath(os.path.dirname(os.sys.argv[0]))) + os.sep + 'teste_racetracks'
summ = lambda p1, p2: p1 or p2
print('Creating layout')
def draw_ractangle(layer_num,center):
    center = numpy.array(center)+numpy.array([-1,-1])
    rectangle1 = gdspy.Rectangle(numpy.array([0,0])+numpy.array(center),numpy.array([1,1])+numpy.array(center),layer=layer_num)
    return rectangle1
def draw_circle(layer_num,center):
    circle1 = gdspy.Round(center,1,0, initial_angle=0.0*numpy.pi/2.0, final_angle=2.0*numpy.pi,number_of_points=2000,max_points=199,layer=layer_num)
    return circle1

def translate(layer_num,center):
    r1=draw_ractangle(layer_num,center)
    c1=draw_circle(layer_num,center)
    bool = gdspy.boolean([r1,c1],summ,max_points=199,layer=layer_num)
    return bool

layer_vector = [1]
unit_cell1 = gdspy.Cell('testcell')
unit_cell1.add(translate(1,(1,1)))

gdspy.gds_print(name + '.gds', unit=1.0e-6, precision=1.0e-9)
print('Sample gds file saved: ' + name + '.gds')

print('Opening viewer')
gdspy.LayoutViewer()
