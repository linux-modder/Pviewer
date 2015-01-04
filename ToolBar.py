# -*- coding: utf-8 -*-
import gtk,traceback

class nuevoBoton(gtk.Button):
    def __init__(self,imagenID,tip):
        gtk.Button.__init__(self)
        imagen = gtk.Image()
        imagen.set_from_stock(imagenID,gtk.ICON_SIZE_BUTTON)
        self.add(imagen)
        self.set_tooltip_text(tip)
        
class ToolBar(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self,False,0)
        
        self.quite = nuevoBoton(gtk.STOCK_REMOVE,"salir")
        self.pack_start(self.quite,False,False,5)
        self.mini = nuevoBoton(gtk.STOCK_GO_DOWN,"minimizar")
        self.pack_start(self.mini,False,False,5)
        self.Zout = nuevoBoton(gtk.STOCK_ZOOM_OUT,"zoom out")
        self.pack_start(self.Zout,False,False,5)
        self.Zin = nuevoBoton(gtk.STOCK_ZOOM_IN,"zoom in")
        self.pack_start(self.Zin,False,False,5)
        self.Zfit = nuevoBoton(gtk.STOCK_ZOOM_FIT,"best fit")
        self.pack_start(self.Zfit,False,False,5)
        self.Z_one = nuevoBoton(gtk.STOCK_ZOOM_100,"zoom 100%")
        self.pack_start(self.Z_one,False,False,5)
        self.pref = nuevoBoton(gtk.STOCK_PREFERENCES,"preferences")
        self.pack_start(self.pref,False,False,5)
        self.flip_V = nuevoBoton(gtk.STOCK_GO_UP,"flip Vertical")
        self.pack_start(self.flip_V,False,False,5)
        self.flip_H = nuevoBoton(gtk.STOCK_GO_FORWARD,"flip Horizontal")
        self.pack_start(self.flip_H,False,False,5)
        self.delete = nuevoBoton(gtk.STOCK_NO,"delete")
        self.pack_start(self.delete,False,False,5)
        self.ver_tool_panel = gtk.CheckButton()
        self.ver_tool_panel.set_tooltip_text("panel de herramientas")
        self.pack_start(self.ver_tool_panel,False,False,5)
        self.exe = nuevoBoton(gtk.STOCK_EXECUTE,"MAS OPCIONES!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
        
        
        '''abrir un panel mas grande con mas botones y hareas de texto para elejir la pagina
        datos sobre la imagen,coordenasdas,angulo,escala,mucho mas.'''
        
        "' Open a browser and copy/paste link in url to further view/manage/modify the image'" // English translation 
        
        self.pack_start(self.exe,False,False,5)
        self.exe = nuevoBoton(gtk.STOCK_EXECUTE,"execute")
        self.pack_start(self.exe,False,False,5)
        self.exe = nuevoBoton(gtk.STOCK_EXECUTE,"execute")
        self.pack_start(self.exe,False,False,5)
        self.exe = nuevoBoton(gtk.STOCK_EXECUTE,"execute")
        self.pack_start(self.exe,False,False,5)#'''
        
        
class ToolPanel(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self,False,0)
        
        adj = gtk.Adjustment(1.0, 1.0, 31.0, 1.0, 5.0, 0.0)
        spinner = gtk.SpinButton(adj, 0, 0)
        spinner.set_size_request(50,-1)
        #spinner = gtk.SpinButton()
        spinner.set_wrap(gtk.TRUE)
        self.pack_start(spinner,False,False,5)
        self.page_num = gtk.Entry(3)
        self.page_num.set_size_request(100,-1)
        self.pack_start(self.page_num,False,False,5)
