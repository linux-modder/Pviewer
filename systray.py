import gtk

class systray(gtk.StatusIcon):
    
    def __init__(self,parent,cm):
        gtk.StatusIcon.__init__(self)
        self.parent = parent
        self.cm = cm
        self.set_from_stock(gtk.STOCK_ABOUT)
        #self.set_from_file()  
        #self.tray = gtk.status_icon_new_from_file("logo.png")
        self.connect('popup-menu', self.make_menu)
        self.connect("activate",self.on_left_click)
        self.set_tooltip(('Pviewer'))
        
        
    def on_left_click(self, widget):
        if self.parent.window.get_visible():
        #hacerla invisible            
            self.parent.window.set_visible(False)                        
        else:
            #hacerla visible
            if self.cm.transparency == 2: self.cm.get_bg()          
            self.parent.window.set_visible(True)                        
            self.parent.window.present() 

    def make_menu(self, icon, event_button, event_time):
        menu = gtk.Menu()        
        about = gtk.MenuItem("about")
        about.show()
        menu.append(about)
        about.connect("activate",self.about)
        #menu.add(gtk.VSeparator())
        salir = gtk.MenuItem("salir")
        salir.show()
        menu.append(salir)
        salir.connect("activate",self.parent.destroy)
        menu.popup(None, None, gtk.status_icon_position_menu,event_button, event_time, self)
        
    def about(self,widget):
        self.cm.draw_pic = False
        self.cm.msg = ["por panda; en mis ratos libres ='3","by panda; in my free time XD"]
        if self.parent.window.get_visible():
            #hacerla invisible            
            self.parent.window.present()                        
        else:
            #hacerla visible y ponerla adelante           
            self.parent.window.set_visible(True)                        
            self.parent.window.present()
