#!/usr/bin/env python
import pygtk
import gtk

#declarando a lista de quadrados
quadrados=[]

def cria_quadrado(tela,evento):
    global quadrados

    #obtendo as coordenadas do clique de mouse
    coor=evento.get_coords()
    x=coor[0]
    y=coor[1]

    #criando um novo quadrado e incluindo ele na lista
    novo_quadrado=[x-25,y-25,50,50]
    quadrados.append(novo_quadrado)

    # disparando a funcao 'desenha()'
    # para incluir o nosso novo quadrado
    desenha(tela,None)

# a funcao desenha() deve ser chamada sempre que
# quisermos redesenhar a tela
# ou quando a tela precisar ser redesenhada
# por ter sido encoberta por outra janele, por
# exemplo
def desenha(tela,evento ):
    global quadrados
    #criando um "graphics context"
    gc=tela.get_style().fg_gc[gtk.STATE_NORMAL]

    #definindo as cores
    verde=gtk.gdk.Color(0,48255,0,0)
    preto=gtk.gdk.Color(0,0,0,0)
    fundo=gtk.gdk.Color(65535,65535,65535,0)

    #pintando o fundo da nossa tela
    gc.set_rgb_fg_color(fundo)
    tela.window.draw_rectangle(gc,True,0,0,800,600 )

    # desenhando cada um dos quadrados
    for q in quadrados:

        #desenhando o quadrado preenchido
        gc.set_rgb_fg_color(verde)
        tela.window.draw_rectangle(gc,True,q[0],q[1],q[2],q[3])

        #desenhando a borda do quadrado
        gc.set_rgb_fg_color(preto)
        tela.window.draw_rectangle(gc,False,q[0],q[1],q[2],q[3])

def limpar(botao):
    global quadrados
    global tela
    #limpando a lista de quadrados
    quadrados=[]

    #disparando novamente a funcao "desenha()"
    #para desenhar a tela branca sem nenhum quadrado
    desenha(tela, None)

win=gtk.Window()
win.set_title( "medeubranco.wordpress.com - Desenhando na tela com PyGTK" )
win.set_size_request(800,600)
win.connect('destroy',gtk.main_quit)

box=gtk.VBox()

#aqui a nossa tela sendo criada
tela=gtk.DrawingArea()

tela.connect('expose-event',desenha)
tela.add_events( gtk.gdk.BUTTON_PRESS_MASK )
tela.connect('button-press-event',cria_quadrado)

botao=gtk.Button( "limpar" )

botao.connect("clicked",limpar)

win.add(box)
box.set_border_width(10)

box.pack_start(tela)
box.pack_start(botao,False)
win.show_all()
gtk.main()


