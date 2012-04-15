import pygtk
import gtk
import math
import string

import inspect

class Mouse(object):

    def __init__(self):
    
        self.x = 0
        
        self.y = 0

#--- Polygons

class Label(object):

    def __init__(self, text):

        self.text = text

        self.visible = True

    def draw(self, draw_area, x, y):

        draw_area.text_area.set_text(self.text)

        draw_area.canvas.window.draw_layout(draw_area.gc, x, y, draw_area.text_area)

        #self.item_to_draw = ''

class Node(object):

    def __init__(self, name, xy):

        self.name = name

        self.xy = xy

        self.label_area = Label(name)

        self.visible = True

        self.dot_central_x = None

        self.dot_central_y = None


    def draw(self, draw_area):

        x, y = self.xy

        print '<draw node>',

        print '<x = ',x,', y = ',y,'>'

        text_length = len(self.name)

        text_length_pixel = text_length*6

        dot_pixel = 60

        print '<text length>', text_length

        #------------------------------------------------------

        top_right             = ( x , y) 
        
        top_left              = ( x + text_length_pixel + dot_pixel , y)

        #------------------------------------------------------

        bottom_right          = ( x , y + 30)

        bottom_left           = ( x + text_length_pixel + dot_pixel , y + 30)

        #vertical_top_mid      = ( x+text_length+35 , y)
        vertical_top_mid      = ( x + text_length_pixel + 35 , y)

        #vertical_bottom_mid   = ( x+text_length+35 , y+30)
        vertical_bottom_mid   = ( x + text_length_pixel + 35 , y + 30)

        #self.canvas.window.draw_polygon(self.gc, False, [ top_left , top_right , vertical_top_right , vertical_bottom_right , bottom_left , vertical_bottom_left , vertical_top_left , vertical_top_mid , vertical_bottom_mid , bottom_right ])

        draw_area.canvas.window.draw_polygon(draw_area.gc, False, [ vertical_bottom_mid , bottom_left , top_left , vertical_top_mid , vertical_bottom_mid , bottom_right , top_right , vertical_top_mid  ])

        self.label_area.draw(draw_area, x+10, y+10)  

        draw_area.canvas.window.draw_arc(draw_area.gc, False, (vertical_top_mid[0] + 10), (vertical_top_mid[1] + 13) , 5, 5, 0, 360 * 64)

        self.dot_central_x = vertical_top_mid[0] + 10 + 2

        self.dot_central_y = vertical_top_mid[1] + 13 + 2


class LineConnector(object):

    def __init__(self, from_node, to_node):

        self.bgn_xy = (from_node.dot_central_x, from_node.dot_central_y)

        self.end_xy = to_node.xy

    def draw(self, draw_area):

        draw_area.window.draw_line(draw_area.gc, self.bgn_xy[0], self.bgn_xy[1], self.end_xy[0], self.end_xy[1])

class Polygon(object):

    def __init__(self, name, base_x_y, visible):

        self.t = ''

        self.name = name

        self.base_x_y = base_x_y

        self.visible = visible

        self.line_bgn_xy = (0,0)

        self.line_end_xy = (0,0)

        self.dot = (0,0)

    def set_type(self, t):

        self.t = t

    def get_type(self):

        return self.t

    def set_name(self, name):

        self.name = name

    def get_name(self):

        return self.name

    def set_xy( self , base_x_y ):

        self.base_x_y = base_x_y

    def get_xy(self):

        return self.base_x_y

    def set_visible(self, visible):

        self.visible = visible

    def is_visible(self):

        return self.visible

    def set_dot_point(self,xy):

        self.dot = xy

    def get_dot_point(self):

        return self.dot

    #--- Line bgn point

    def set_line_begin_point(self, xy):

        self.line_bgn_xy = xy
    
    def get_line_begin_point(self):

        return self.line_bgn_xy
    
    #--- Line end point

    def set_line_end_point(self, xy):

        self.line_end_xy = xy

    def get_line_end_point(self):

        return self.line_end_xy

        self.line_end_xy = xy

#--- Draw

class Draw(object):

    #--- [END] event functions ------------------------------------------

    #--- original version
    #def expose(self, widget, event):
    #
    #    self.style = widget.get_style()
    #
    #    self.gc = self.style.fg_gc[gtk.STATE_NORMAL] # graphics context
    #
    #    self.font = self.style.get_font()
    #
    #    self.canvas.window.draw_string(self.font, self.gc, 50, 60, "Point")
    #    
    #    #self.draw_frame.window.draw_rectangle(self.gc, gtk.TRUE, x+10, y+10, 20, 20)
    #
    #    return gtk.True

    
    #--- Redraw/Refresh function
    #
    #--- simplescrible.py version ---------------------------------------------------

    def expose(self, widget, event):
    
        x, y, width, height = event.area
      
        self.gc = widget.style.fg_gc[gtk.STATE_NORMAL] # graphics context
                
        widget.window.draw_drawable(self.gc, self.pixmap, x, y, x, y, width, height)

        for element in self.get_element_list() :

            if element == None :

                continue

            if element.visible == True:

                #self.draw_polygon(polygon) #--- old line
                element.draw(self) #--- new line
    
        return False

    #--------------------------------------------------------------------------------

    def configure(self, widget, event):
    
        x, y, width, height = widget.get_allocation()
        
        self.pixmap = gtk.gdk.Pixmap( widget.window, width, height )
        
        self.pixmap.draw_rectangle(widget.get_style().white_gc, True, 0, 0, width, height)

    #--- desenhando em movimento com o boto 1 pressionado --------------- 
    def motion_notify_event(self, widget, event):
    
        if event.is_hint :
            
            x, y, state = event.window.get_pointer()

            print '<inside the window><'+str(x)+','+str(y)+'>'
            
        else :
            
            print '<<out of window>>'

            x = event.x
            y = event.y
            state = event.state

        self.mouse.x = x
        self.mouse.y = y
           
        if state & gtk.gdk.BUTTON1_MASK and self.pixmap != None:
        
            #print '<dragging_move><' + str(x) +' , '+ str(y) +'>'
            print '<dragging_move_mouse><' + str(self.mouse.x) +' , '+ str(self.mouse.y) +'>'

    #--- desenhando apenas com o click
    def button_press_event(self, widget, event):
    
        print '<mouse_button_1_pressed>'
        
        print '<item_to_draw><' + self.item_to_draw + '>'
        
        #--- filtrando qual flag esta disponivel
        
        if self.item_to_draw == 'node':
            
            print '<building node>'

            node_name = self.text_entry_node_name.get_text()

            if node_name != '' and node_name != None :

                n = Node(node_name, (self.mouse.x , self.mouse.y))

                n.draw(self)

                self.element_list.append(n)

                self.text_entry_node_name.set_text('')

            else :

                print '<empity names arent allowed>'

        else :

            print '<building nothing>'

        self.item_to_draw = ''


            #-----------------------------------------------------------

            #p = self.create_polygon('1111', (self.mouse.x, self.mouse.y), True)
            #
            #p.set_type( self.item_to_draw )
            #
            #self.draw_polygon( p )

            #----------------------------------------------------------

            #if self.item_to_draw == 'label' : 

            #    self.label ( 'dunnox' , self.mouse.x , self.mouse.y )

            #elif self.item_to_draw == 'node' :
                
            #    self.node( 'test node', (self.mouse.x, self.mouse.y) )

    #--- [END] event functions ------------------------------------------

    def __init__(self):
        
        self.frame = gtk.Frame("Draw Area")
        
        self.canvas = gtk.DrawingArea()

        self.canvas.connect( "expose-event", self.expose) #--- pixmap handles
        
        self.pixmap = None
        
        self.text_entry_node_name = None
        
        #--- [BGN] new from scrible --------------------------------
        
        self.canvas.connect( "configure_event", self.configure ) #--- pixmap handles
        
        self.canvas.connect( "motion_notify_event", self.motion_notify_event )

        self.canvas.connect( "button_press_event", self.button_press_event )
        
        #--- relacionados aos eventos do mouse
        self.canvas.set_events(gtk.gdk.EXPOSURE_MASK | gtk.gdk.LEAVE_NOTIFY_MASK | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK)
        
        #--- [END] new from scrible --------------------------------

        #--- paking --------------

        self.frame.add(self.canvas)

        #--- label text buffer -----------------------------
        
        self.text_area = self.canvas.create_pango_layout('')
        
        #---------------------------------------------------
        
        #--- object to draw flags -----

        self.item_to_draw = ''

        #------------------------------
        
        #--- Le mouse abstraction

        self.mouse = Mouse()

        #-------------------

        #--- polygon structs
        
        #self.polygon_dict = {}
        self.element_dict = {}

        self.element_list = []

        #---------------------

        self.canvas.show()

        self.frame.show() 

    #-------------------------------------
    #
    #              --- OOP ---
    #
    #--------------------------------------

    #--- text entry

    def set_entry(self, entry):

        self.text_entry_node_name = entry

    #--- frame

    def get_frame(self):

        return self.frame

    def get_draw_area(self):

        return self.canvas

        
    #--- organizando os poligonos
    
    def append_element(self, element):

        self.element_dict[element.get_name()] = element
        self.element_list.append( element )

    def get_element(self, label):

        return self.element_dict.get(label)

    def get_element_list(self):

        return self.element_list

    #--- drawing

    #def create_polygon(self, name, points, visible):
    #
    #    p = Polygon( name, points, visible )
    #
    #    self.polygon_list.append( p )
    #
    #    return p
     
    def draw_polygon(self, polygon) : 
     
        print '<drawing_polygon>'+'<'+str(polygon.get_xy())+'>'

        if polygon.get_type() == 'node':

            self.node(polygon.get_name(), polygon.get_xy() )
        
        elif polygon.get_type() == 'label':

            self.node(polygon.get_name(), polygon.get_xy() )

    def label(self, text, x, y):

        self.text_area.set_text(text)

        self.canvas.window.draw_layout(self.gc, x, y, self.text_area)

        self.item_to_draw = ''

    def connector(self, from_x, from_y, to_x, to_y):

        print 'todo'

    def dot( self , x , y ) :

        self.canvas.window.draw_arc(self.gc, False, x + 10, y, 5, 5, 0, 360 * 64)

    def node(self, text, points):

        x, y = points

        text_length = len(text)

        top_right             = ( x                , y) 
        
        top_left              = ( x+text_length+60 , y)

        bottom_right          = ( x                , y+30)

        bottom_left           = ( x+text_length+60 , y+30)

        vertical_top_mid      = ( x+text_length+35 , y)

        vertical_bottom_mid   = ( x+text_length+35 , y+30)

        
#        self.canvas.window.draw_polygon(self.gc, False, [ top_left , top_right , vertical_top_right , vertical_bottom_right , bottom_left , vertical_bottom_left , vertical_top_left , vertical_top_mid , vertical_bottom_mid , bottom_right ])

        self.canvas.window.draw_polygon(self.gc, False, [ vertical_bottom_mid , bottom_left , top_left , vertical_top_mid , vertical_bottom_mid , bottom_right , top_right , vertical_top_mid  ])

        self.label(text, x+10, y+10) 

        self.dot( vertical_top_mid[0] , vertical_top_mid[1] + 13)

        self.item_to_draw = ''
    
    #--- flag ------

    def set_item_to_draw(self, label):

        self.item_to_draw = label

#--- Manager

class Manager(object):

    def clicked_add_node(self, widget, data=None):

        print 'i was clicked'

        self.draw.set_item_to_draw('node')

    def clicked_add_connector(self, widget, data=None):

        print 'i was clicked'

        self.draw.set_item_to_draw('connector')

    def __init__(self):

        self.window = gtk.Window()

        self.window.set_default_size(800, 600)

        self.window.connect("delete_event", lambda w : gtk.main_quit() )

        self.table = gtk.Table(3,1)

        self.window.add(self.table)

        #--- draw area

        self.draw = Draw()

        #--- line entrys

        self.entry_node_name = gtk.Entry()

        self.draw.set_entry(self.entry_node_name)

        #--- buttons

        self.button_add_node = gtk.Button("Add Node")

        self.button_add_node.connect("clicked", self.clicked_add_node)

        self.button_add_conector = gtk.Button("Add Conector")

        self.button_add_conector.connect("clicked", self.clicked_add_node)

        self.button_quit = gtk.Button("quit")

        self.button_quit.connect("clicked", lambda w : gtk.main_quit())

        #--- packing

        self.table.attach(self.draw.get_frame(), 0, 2, 0, 1)

        self.table.attach(self.button_add_node, 0, 1, 1, 2, gtk.FILL, gtk.FILL)

        self.table.attach(self.button_add_conector, 1, 2, 1, 2, gtk.FILL, gtk.FILL)
        
        self.table.attach(self.entry_node_name, 2, 3, 1, 2, gtk.FILL, gtk.FILL)

        self.table.attach(self.button_quit, 0, 2, 2, 3, gtk.FILL, gtk.FILL)
        
        self.window.show_all()
        
        self.draw.get_draw_area().show()
        self.draw.get_frame().show()
        gtk.main()

if __name__ == "__main__":

    m = Manager()

        
