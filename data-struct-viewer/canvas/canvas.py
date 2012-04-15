#!/usr/bin/env python
# clock_ex3.py

# a pygtk widget that implements a clock face
# porting of Davyd Madeley's 
# http://www.gnome.org/~davyd/gnome-journal-cairo-article/clock-ex3.c

# author: Lawrence Oluyede <l.oluyede@gmail.com>
# date: 03 December 2005

import gtk
import math
from gtk import gdk

class Drawer(gtk.DrawingArea):
    
    def __init__(self):
    
        gtk.DrawingArea.__init__(self)

        self.connect("expose_event", self.expose)

        self.polygonos_list = []
        
    def expose(self, widget, event):
    
        self.context = widget.window.cairo_create()
        
        # set a clip region for the expose event
        
        self.context.clip()

        self.draw(self.context)

        print type(self.context)
        
        return False
    
    def basic_color_table(self, color):

        rgb = None

        if color == 'black':

            rgb = (0,0,0)

        elif color == 'white':

            rgb = (9,9,9)
    
        return rgb

    def draw_square(self, context, draw_area_x, draw_area_y, width, height, color):

        context.rectangle(draw_area_x, draw_area_y, width, height)
        
        #--- coloring
        if type(color) == str:

            color = self.basic_color_table(color)

        context.set_source_rgb(color[0], color[1], color[2])

       
        context.fill()
 
    def draw(self, context):
        rect = self.get_allocation()
        x = rect.x + rect.width / 2
        y = rect.y + rect.height / 2
        
        radius = min(rect.width / 2, rect.height / 2) - 5
        
        # clock back
        context.arc(x, y, radius, 0, 2 * math.pi)
        context.set_source_rgb(1, 1, 1)
        context.fill_preserve()
        context.set_source_rgb(0, 0, 0)
        context.stroke()
        
        # clock ticks
        for i in xrange(12):
            context.save()
            
            if i % 3 == 0:
                inset = 0.2 * radius
            else:
                inset = 0.1 * radius
                context.set_line_width(0.5 * context.get_line_width())
            
            context.move_to(x + (radius - inset) * math.cos(i * math.pi / 6),
                            y + (radius - inset) * math.sin(i * math.pi / 6))
            context.line_to(x + radius * math.cos(i * math.pi / 6),
                            y + radius * math.sin(i * math.pi / 6))
            context.stroke()
            context.restore()
        

#-----------------------------------------

draw_area = Drawer()

def main():
    
    X = 1

    Y = 1

   
    window = gtk.Window()
    
    window.set_default_size(400,600)

    table  = gtk.Table(2,2,False)

    window.add(table)

    b1 = gtk.Button("add node")
    b2 = gtk.Button("line")

    #b1.connect ("clicked", add_node)

    #--- packing
    table.attach( Drawer(), 0,1, 0,1)
    
    table.attach(b1, 1, 2, 0, 1)
    table.attach(b2, 1,2,1,2)

    window.connect("destroy", gtk.main_quit)

    window.show_all()
    
    gtk.main()
    
if __name__ == "__main__":
    main()
