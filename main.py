import gtk,gobject#,math, urllib,os,sys,threading,traceback#,cairo
from ToolBar import ToolBar#,ToolPanel
#from FolderBar import FolderBar
import cairo_magic
import filehandler
import systray

class ventanaPrincipal:
    def __init__(self,path):
        self.cm = cairo_magic.cm(self)
        self.fh = filehandler.fh(self,self.cm)
        self.cm.fh = self.fh
        #self.supports_alpha = False
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_events(gtk.gdk.EXPOSURE_MASK| gtk.gdk.LEAVE_NOTIFY_MASK| gtk.gdk.BUTTON_RELEASE_MASK| gtk.gdk.BUTTON_PRESS_MASK| gtk.gdk.POINTER_MOTION_MASK| gtk.gdk.POINTER_MOTION_HINT_MASK| gtk.gdk.SCROLL_MASK)            
        self.window.set_title("PViewer")
        #self.icono = gtk.gdk.pixbuf_new_from_file()
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_decorated(False)
        self.window.maximize()
        self.window.set_app_paintable(True)
        self.window.connect('expose-event',self.cm.expose)
        self.window.connect('screen-changed',self.cm.screen_changed)
        self.cm.screen_changed(self.window)
        self.rootwin = self.window.get_screen().get_root_window()
        
        #####################################
        if path:
            w = gtk.gdk.get_default_root_window()
            p = gtk.gdk.atom_intern('_NET_WORKAREA')
            pant = w.property_get(p)[2]
            wi,he = (pant[2] - pant[0]),(pant[3] - pant[1])
            gobject.idle_add(lambda *a : self.fh.open_new_image(path, wi, he))
        #####################################
        if self.cm.transparency == 2:
            self.cm.get_bg()
        #####################################      
        
        #self.F = FolderBar()
        self.TB = ToolBar()
        #self.TX = ToolPanel()
        
        self.linea = gtk.EventBox()
        self.linea.modify_bg(gtk.STATE_NORMAL,self.linea.get_colormap().alloc_color("black"))
        self.linea.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.linea.connect("enter-notify-event",self.Show_TB)
        
        
        self.hbox0=gtk.HBox(False,0)
        self.vbox1=gtk.VBox(False,0)
        self.hboxF = gtk.HBox(False,0)
        #self.hboxF.pack_start(self.F,True,True,30)
        #self.vbox1.pack_start(self.hboxF,False,False,7)
        
        #self.imagen_animada = gtk.Image()
        #self.image_animada.set_from_file('/home/panda/rs_464x274-130810153745-mlp_breaking_bad.gif')
        #self.vbox1.pack_start(self.imagen_animada,True,True,7)
        #self.vbox1.pack_start(self.S,True,True,0)
        #self.vbox1.pack_end(self.G.get(),False,False,0)
        self.hbox0.pack_start(self.vbox1,True,True,0)
        self.hbox0.pack_end(self.linea,False,False,1)
        #self.hbox0.pack_end(self.TX,False,False,0)
        self.hbox0.pack_end(self.TB,False,False,5)
        self.window.add(self.hbox0)
        self.window.show_all()
        
        gobject.timeout_add(1000,self.cm.chck_n_hide_TB)
        gobject.timeout_add(200,self.cm.signs_timeout)
        if self.cm.limit: gobject.timeout_add(70,self.cm.cinematica)
            
        self.window.connect("motion_notify_event", self.cm.motion_notify_event)
        self.window.connect("button_press_event", self.cm.button_press_event)
        self.window.connect("button_release_event", self.cm.button_release_event)
        self.window.connect("scroll-event", self.cm.on_scroll_event)
        self.window.connect("key_release_event",self.cm.mapeoteclas)
        self.window.drag_dest_set(gtk.DEST_DEFAULT_ALL, [('text/uri-list', 0, 0)], gtk.gdk.ACTION_COPY | gtk.gdk.ACTION_MOVE)
        self.window.connect('drag_data_received', self.fh.drag_n_drop_event)
        
        self.TB.quite.connect("clicked",lambda *args: gtk.main_quit())
        self.TB.mini.connect("clicked",lambda *args: self.window.iconify())
        self.TB.flip_H.connect("clicked",lambda *args: self.cm.flip(True))
        self.TB.flip_V.connect("clicked",lambda *args: self.cm.flip(False))
        self.TB.pref.connect("clicked",lambda *args: self.cm.chng_cursor())
        self.TB.Zin.connect("clicked",self.cm.zoom_in_out,True)
        self.TB.Zout.connect("clicked",self.cm.zoom_in_out,False)
        self.TB.Zfit.connect("clicked",self.cm.zoom_best_fit_one)
        self.TB.Z_one.connect("clicked",self.cm.zoom_best_fit_one,False)
        
        self.TB.exe.connect("clicked",self.cm.get_bg)
        
        self.ST = systray.systray(self,self.cm)

    def main(self):
        #gtk.gdk.threads_init()
        gtk.main()
        
    def delete_event(self, widget, event, data=None):
        print "saliendo..."
    
    def destroy(self, widget):
        gtk.main_quit()
        

    
    def Show_TB(self,*args):
        self.TB.set_visible(True) #make toobar visible
        self.shw_TB = 0 #reset the timeout
        self.cm.trigger_expose() #update background so the back-border-line is visible
        
    
'''
def start():
    viewer = ventanaPrincipal()
    viewer.window.set_visible(True)
    viewer.main()
start()'''
