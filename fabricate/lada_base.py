from sys import path
path.append('../../Lada/fabricate') ## add lada library path
from lada import *

### main enclosure
T = 3* mm
main_LENGTH = 269 * mm + 2 * T
main_WIDTH = 206 * mm + 2 * T
main_HEIGHT = 56 * mm + 2 * T
can = new_canvas("NovaBooth_lada.pdf", 20*inch, 12*inch, .5*inch)
main_lada = Lada(main_LENGTH, main_WIDTH, main_HEIGHT, T, max_edge_span=60*mm)
main_lada.drawOn(can)
can.save()
print 'wrote', can._filename
main_scad = main_lada.toScad(name='main')

### TiM Case
T = 3* mm
tim_LENGTH = 4.2 * inch + 2 * T + 2 * .4 * inch # main_WIDTH + 2 * T
tim_WIDTH = main_HEIGHT + 2 * T
tim_HEIGHT =  main_LENGTH + 2 * T
can = new_canvas("TiM_lada.pdf", 20*inch, 12*inch, .5*inch)
tim_lada = Lada(tim_LENGTH, tim_WIDTH, tim_HEIGHT, T, max_edge_span=200*mm)
tim_lada.drawOn(can)
can.save()
print 'wrote', can._filename
tim_scad = tim_lada.toScad(name='tim')


f = open("NovaBooth_lada.scad", 'w')
## print >> f, main_scad
print >> f, tim_scad
f.close()
print 'write', f.name
