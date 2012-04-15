# -*- coding: iso-8859-1

import pygtk
pygtk.require('2.0')
import gtk

#--- Abstração visual
class ListViewerFrame(object):
    
    def __init__(self):

        self.frame = gtk.Frame("ListViewer")

    def get_frame(self):
        
        return self.frame

#--- Tipos de Listas
class SimpleLinkedList(object):

    def show(self):

        self.label.show()        

        self.frame.show()

    def __init__(self):

        self.frame = gtk.Frame("Lista simplismente encadeada")
        
        # dois colunas no frame principal: 1) carregador o vizualizador, 2) debugg de text ou editor! .-.

        self.label = gtk.Label("LSE")

        self.show()

    def get_label(self):

        return self.label

    def get_frame(self):

        return self.frame

#------------------------------------------------------------------

class ListNotebook(object):

    def __init__(self):

        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_RIGHT)
        
        #--- packing - Lista Simplismente Encadeada

        self.sll = SimpleLinkedList()

        self.notebook.append_page( self.sll.get_frame(), self.sll.get_label()) # (gtk.Frame, gtk.Label)

        self.notebook.set_current_page(1)

    def get_notebook(self):

        return self.notebook

class ListCommandsFrame(object):
    
    def build_addition_buttons_frame(self):

        self.frame_addition_commands.add(self.table_add)
      
        #--------------------        

        self.table_add.attach(self.button_add_at_top, 0, 1, 0, 1) #, gtk.FILL, gtk.FILL)

        self.table_add.attach(self.button_add_at_end, 0, 1, 1, 2) #, gtk.FILL, gtk.FILL)        

        self.table_add.attach(self.button_add_at_position, 0, 1, 2, 3) #, gtk.FILL, gtk.FILL)

        self.table.attach( self.frame_addition_commands , 0 , 1 , 0 , 1, yoptions=gtk.FILL) #, gtk.FILL)

    def build_remove_buttons_frame(self):

        self.frame_remove_commands.add(self.table_rem)

        
        self.table_rem.attach(self.button_rem_at_top, 0, 1, 0, 1) #, gtk.FILL, gtk.FILL)

        self.table_rem.attach(self.button_rem_at_end, 0, 1, 1, 2) #, gtk.FILL, gtk.FILL)


        self.table_rem.attach(self.button_rem_at_position, 0, 1, 2, 3) #, gtk.FILL, gtk.FILL)

        self.table.attach( self.frame_remove_commands , 1 , 2 , 0 , 1 , yoptions=gtk.FILL) #, gtk.FILL)


    def show(self):

        self.button_add_at_top.show()
        self.button_add_at_end.show()
        self.button_add_at_position.show()
        self.frame_addition_commands.show()
 
        self.button_rem_at_top.show()
        self.button_rem_at_end.show()
        self.button_rem_at_position.show()
        self.frame_remove_commands.show()       

        self.table_add.show()
        self.table_rem.show()

        self.table.show()


    def __init__(self):

        self.frame = gtk.Frame("Comandos")
        
        self.table = gtk.Table( 3 , 1 , False)

        self.frame.add(self.table)
 
        #--- lista de botoes
        
        #------ adicionadores

        self.button_add_at_top = gtk.Button("ao topo")
        
        self.button_add_at_end = gtk.Button("ao fim")

        self.button_add_at_position = gtk.Button("em dada posicao")

        #------ removedores

        self.button_rem_at_top = gtk.Button("do topo")
        
        self.button_rem_at_end = gtk.Button("do fim")

        self.button_rem_at_position = gtk.Button("em dada posicao")

        #--- packing additions

        #--- Build frames ---
       
        self.frame_addition_commands = gtk.Frame("Adicionar")

        self.table_add = gtk.Table( 1 , 3 , False)

        self.build_addition_buttons_frame()

        #--- packing removes

        self.frame_remove_commands = gtk.Frame("Remover")

        self.table_rem = gtk.Table( 1 , 3 , False)

        self.build_remove_buttons_frame() 

        #--- show up!

        self.show() 

    def get_frame(self):
    
        return self.frame

class MainWindow(object):

    def quit(self, widget, data=None):

        gtk.main_quit()    

    def __init__(self):
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.set_default_size(400, 300)

        #--- events connectors        

        self.window.connect("delete_event", self.quit)
        
        #--- packing
 
        self.table = gtk.Table(2 , 2, False)

        self.window.add(self.table)
        
        #--- attaching Frames  

        self.list_viewer_frame = ListViewerFrame().get_frame()        

        self.list_command_frame = ListCommandsFrame().get_frame() 

        self.notebook_viewer = ListNotebook().get_notebook()

        #--------------------
        
        self.table.attach( self.notebook_viewer , 0 , 1 , 0 , 1) #, gtk.FILL, gtk.FILL)
        
        self.table.attach( self.list_command_frame , 0 , 1 , 1 , 2, yoptions=gtk.FILL) #, gtk.FILL)
        
        #self.table.attach( self.list_viewer_frame , 0 , 1 , 2 , 3 )

        

        
        self.list_viewer_frame.show()
        self.list_command_frame.show()
        self.notebook_viewer.show()
        self.table.show()
        self.window.show()
    

    def loop(self):
        
        gtk.main()

if __name__ == '__main__':
    
    hello = MainWindow()

    hello.loop()
