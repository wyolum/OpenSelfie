from sys import path
path.append('../../Lada/fabricate') ## add lada library path
from lada import *

### main enclosure
T = 3* mm
main_LENGTH = 300 * mm
main_WIDTH = 50.5 * mm
main_HEIGHT = 210 * mm
can = new_canvas("NovaBooth_lada.pdf", 20*inch, 12*inch, .5*inch)
main_lada = Lada(main_LENGTH, main_WIDTH, main_HEIGHT, T, max_edge_span=100*mm)
main_lada.drawOn(can)
can.save()
print 'wrote', can._filename
main_scad = main_lada.toScad(name='main')

### TiM Case
T = 3* mm
tim_LENGTH = 5 * inch + 2 * T
tim_WIDTH = main_LENGTH + 2 * T
tim_HEIGHT =  main_WIDTH + 2 * T
can = new_canvas("TiM_lada.pdf", 20*inch, 12*inch, .5*inch)
tim_lada = Lada(tim_LENGTH, tim_WIDTH, tim_HEIGHT, T, max_edge_span=400*mm)
tim_lada.drawOn(can)
can.save()
print 'wrote', can._filename
tim_scad = tim_lada.toScad(name='tim')


f = open("NovaBooth_lada.scad", 'w')
## print >> f, main_scad
print >> f, tim_scad
f.close()
print 'write', f.name
