 # -*- coding: latin-1 -*-
import StringIO
import string
from string import *
import os.path
from random import choice
import string
from numpy import *
import PIL.Image
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing, Group, String, Circle, Rect
from reportlab.lib.units import inch, mm, cm
from reportlab.lib.colors import pink, black, red, blue, green, white
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
import reportlab.rl_config
import codecs
reportlab.rl_config.warnOnMissingFontGlyphs = 0
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import glob
import os.path
import sys

from numpy import arange
from copy import deepcopy

def new_canvas(name, width, height, margin):
    can = canvas.Canvas(name,
                        pagesize=(width + 2 * margin, height + 2 * margin))
    return can

OFFSET = .4 * inch
M3_RAD = 1.7 * mm

class Sida:
    def __init__(self, x, y, holes):
        self.x = x
        self.y = y
        self.holes = holes ### [(x, y, r), ...]
        
    def drawOn(self, lower_left, can):
        can.translate(lower_left[0], lower_left[1])
        can.rect(0, 0, self.x, self.y)
        for hole in self.holes:
            can.circle(*hole)
            
        can.translate(-lower_left[0], -lower_left[1])
    
    def toScad(self, material_thickness):
        hole_scad = []
        for hole in self.holes:
            hole_scad.append('translate([%s * mm, %s * mm, -1])cylinder(h=%s*mm, r=%s*mm);' % (hole[0] / mm, hole[1] / mm, material_thickness / mm + 2, hole[2] / mm))
        hole_scad = '\n    '.join(hole_scad)
        out = """\
difference(){
    color([1, 1, 1, .4])cube([%s*mm, %s*mm, %s*mm]);
    %s
}
""" % (self.x / mm, self.y / mm, material_thickness / mm, hole_scad)
        return out

class Lada:
    def __init__(self, length, width, height, material_thickness, max_edge_span=10*inch, margin=0):
        total_h = 3 * margin + height + width
        total_w = 3 * margin + length  + width
        
        self.length = length
        self.height = height
        self.width = width
        self.margin = margin
        self.material_thickness = material_thickness
        self.max_edge_span = max_edge_span
        
        n_edge_l = int((self.length - 2 * self.material_thickness  - 2 * OFFSET) / max_edge_span)
        n_edge_w = int((self.width - 2 * self.material_thickness  - 2 * OFFSET) / max_edge_span)
        n_edge_h = int((self.height - 2 * self.material_thickness  - 2 * OFFSET) / max_edge_span)

        front_holes = [
            (self.material_thickness + OFFSET, OFFSET, M3_RAD),
            (self.length - self.material_thickness - OFFSET, OFFSET, M3_RAD),
            (self.length - self.material_thickness - OFFSET, self.height - OFFSET - 2 * self.material_thickness, M3_RAD),
            (self.material_thickness + OFFSET, self.height - OFFSET - 2 * self.material_thickness, M3_RAD)
            ]
        top_holes = [
            (self.material_thickness + OFFSET, self.material_thickness + OFFSET, M3_RAD),
            (self.length - (self.material_thickness + OFFSET), self.material_thickness + OFFSET, M3_RAD),
            (self.length - (self.material_thickness + OFFSET), self.width - (self.material_thickness + OFFSET), M3_RAD),
            (self.material_thickness + OFFSET, self.width - (self.material_thickness + OFFSET), M3_RAD)
            ]
        side_holes = [
            (OFFSET, OFFSET, M3_RAD),
            (self.height - OFFSET - 2 * self.material_thickness, OFFSET, M3_RAD),
            (self.height - OFFSET - 2 * self.material_thickness, self.width - 2 * self.material_thickness - OFFSET, M3_RAD),
            (OFFSET, self.width - 2 * self.material_thickness - OFFSET, M3_RAD)
            ]

        
        xstart = self.material_thickness + OFFSET
        dx = (self.length - 2 * xstart) / (n_edge_l + 1)
        for i in range(n_edge_l):
            front_holes.append((xstart + (i + 1) * dx, OFFSET, M3_RAD))
            front_holes.append((xstart + (i + 1) * dx, self.height - OFFSET - 2 * self.material_thickness, M3_RAD))

            top_holes.append((xstart + (i + 1) * dx, self.material_thickness + OFFSET, M3_RAD))
            top_holes.append((xstart + (i + 1) * dx, self.width - self.material_thickness - OFFSET, M3_RAD))

            
        for i in range(n_edge_h):
            ystart = OFFSET
            dy = (self.height - 2 * (ystart + self.material_thickness)) / (n_edge_h + 1)
            front_holes.append((self.material_thickness + OFFSET, ystart + (i + 1) * dy, M3_RAD))
            front_holes.append((self.length - self.material_thickness - OFFSET, ystart + (i + 1) * dy, M3_RAD))
            
            side_holes.append((ystart + (i + 1) * dy, OFFSET, M3_RAD))
            side_holes.append((ystart + (i + 1) * dy, self.width - OFFSET - 2 * self.material_thickness, M3_RAD))
        
        for i in range(n_edge_w):
            ystart = OFFSET + self.material_thickness
            dy = (self.width - 2 * OFFSET - 2 * self.material_thickness) / (n_edge_w + 1)
            top_holes.append((self.material_thickness + OFFSET, ystart + (i + 1) * dy, M3_RAD))
            top_holes.append((self.length - 2 * OFFSET - self.material_thickness + OFFSET, ystart + (i + 1) * dy, M3_RAD))

            ystart = OFFSET
            side_holes.append((OFFSET, ystart + (i + 1) * dy, M3_RAD))
            side_holes.append((self.height - OFFSET - 2 * self.material_thickness, ystart + (i + 1) * dy, M3_RAD))
            

        self.top = Sida(self.length, self.width, top_holes)
        self.front = Sida(self.length, self.height - 2 * self.material_thickness, front_holes)
        self.side = Sida(self.height - 2 * self.material_thickness, self.width - 2 * self.material_thickness, side_holes)

    def drawOn(self, can):
        lower_left = []
        def dim(val):
            return '%.2f [%.3f]' % (val / mm, val / inch)
        can.drawString(self.margin, self.height + self.length, "Lada, L=%s, W=%s, H=%s, T=%s" % tuple(map(dim, (self.length, self.width, self.height, self.material_thickness))))
        self.front.drawOn((self.margin, self.margin), can)
        self.top.drawOn((self.margin, self.height - self.material_thickness + 2 * self.margin), can)
        if True: ## one page
            self.side.drawOn((2 * self.margin + self.length + self.material_thickness, 2 * self.margin + self.height), can)
            can.showPage()
        else:
            can.showPage()
            self.side.drawOn((self.margin, self.margin), can)
            can.showPage()
            
    def toScad(self):
        out = StringIO.StringIO()
        print >> out, 'mm = 1;'

        print >> out, self.top.toScad(self.material_thickness)
        print >> out, 'translate([0, 0, %s*mm])' % ((self.height - self.material_thickness) / mm)
        print >> out, self.top.toScad(self.material_thickness)
        
        print >> out, '''module front_back(){
%s
}''' % self.front.toScad(self.material_thickness)

        print >> out, "translate([0, %s*mm, %s*mm])" % (self.material_thickness / mm, self.material_thickness / mm)
        print >> out, "rotate(v=[1, 0, 0], a=90)"
        print >> out, 'front_back();'
        print >> out, 'translate([0, %s*mm, %s*mm])' % (self.width / mm, self.material_thickness / mm)
        print >> out, "rotate(v=[1, 0, 0], a=90)"
        print >> out, 'front_back();'
        
        print >> out, '''module side(){
%s
}''' % self.side.toScad(self.material_thickness)
        print >> out, 'translate([%s*mm, %s*mm, %s*mm])' % (self.material_thickness / mm, self.material_thickness / mm, self.material_thickness / mm)
        print >> out, 'rotate(v=[0, 1, 0], a=-90)'
        print >> out, 'side();'
        print >> out, 'translate([%s*mm, %s*mm, %s*mm])' % ((self.length) / mm, self.material_thickness / mm, self.material_thickness / mm)
        print >> out, 'rotate(v=[0, 1, 0], a=-90)'
        print >> out, 'side();'
        
        out.seek(0)
        return out.read()

def test():
    T = 3* mm
    LENGTH = 300*mm
    WIDTH = 50.5 * mm
    HEIGHT = 210*mm
    can = new_canvas("photobooth_alum.pdf", 20*inch, 12*inch, .5*inch)
    lada = Lada(LENGTH, WIDTH, HEIGHT, 3 * mm, max_edge_span=100*mm)
    lada.drawOn(can)
    can.save()
    print 'wrote', can._filename

    scad = lada.toScad()
    f = open("photobooth_alum.scad", 'w')
    print >> f, scad
    f.close()
    print 'write', f.name
    

if __name__ == '__main__':
    test()
