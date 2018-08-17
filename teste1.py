import numpy
import gdspy

path_cell = gdspy.Cell('PATHS')
path1 = gdspy.Path(1, (0, 0))
spec = {'layer': 1, 'datatype': 1}
path1.arc(2, -numpy.pi , numpy.pi , **spec)
path_cell.add(path1)

gdspy.gds_print('teste1.gds', unit=1.0e-6, precision=1.0e-9)
gdspy.LayoutViewer()
