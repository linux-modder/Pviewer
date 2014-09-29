import cairo,math,gtk,traceback
"""
the images are draw as part of the window background
"""
class cm():
    def __init__(self,parent):
        self.parent = parent
        self.fh = ""
        self.supports_alpha = False
        self.alpha      = 0.9
        self.shw_TB     = 0
        self.show_scale = 0
        self.scale      = 1
        self.msg        = ["panda Viewer","by Panda",":3","thanks to Python, pyGTK and Cairo projects","inspired on picasa viewer and comix"]
        self.draw_pic   = False
        self.rot_ang    = 0 #rotation angle
        self.rot_phase  = 0
        self.rot_c_X    = 0
        self.rot_c_Y    = 0 #rotation center X and Y
        self.rot_r_X    = 0
        self.rot_r_Y    = 0 #rotation reference point X and Y
        self.M_X        = 0
        self.M_Y        = 0 #mouse coordinate X and Y
        self.oldMX      = 0
        self.oldMY      = 0 #old mouse coordinates
        #self.iniciar_rotacion = 0
        self.img_H,self.img_W = 0,0 #pixbuf height and width
        self.imgY   = 0
        self.imgX   = 0 #image coordinates        
        self.oldIX  = 0
        self.oldYX  = 0 #old coordinates
        self.click_in   = False
        self.update_bg      = False #re-draw the background
        self.OPACE, self.TRANSP, self.FAKE = 0, 1, 2
        self.transparency = 1 #transparency mode.
        self.limit = True #limit frame per second
        self.BG_color = [0.0,0.0,0.0]
        
    def mapeoteclas(self,widget,event,data=None):
        D = 50
        A = math.pi/12
        if event.keyval == gtk.keysyms.Escape:
            self.parent.window.set_visible(False)
            #print "presionado esc. escondiendo"
        elif event.keyval == 65464:#8
            self.imgY += -D
        elif event.keyval == 65462:#6
            self.imgX += D
        elif event.keyval == 65458:#2
            self.imgY += D
        elif event.keyval == 65460:#4
            self.imgX += -D
        elif event.keyval == 65455:#/
            self.rot_ang += A
        elif event.keyval == 65450:#*
            self.rot_ang += -A
        elif event.keyval == 65535:#delete
            print "suprimir"
        elif event.keyval == 65461:#5
            self.zoom_best_fit_one("", True)
            return None
        elif event.keyval == 65457:#1
            self.zoom_best_fit_one("", False)
            return None
        elif event.keyval == 65451:#+
            self.zoom_in_out("", True)
            return None
        elif event.keyval == 65453:#-
            self.zoom_in_out("", False)
            return None
        elif event.keyval == 65365:#re pag
            self.flip(False)
            return None
        elif event.keyval == 65366:#av pag
            self.flip(True)
            return None
        else:
            return None
        self.trigger_expose()
        
    def chng_cursor(self,icono=gtk.gdk.EXCHANGE): #change the cursor icon for another
        if icono:
            mode = gtk.gdk.Cursor(icono)
            self.parent.hbox0.window.set_cursor(mode)
        else:
            self.parent.hbox0.window.set_cursor(None)
        '''if icono == "normal":
            self.parent.hbox0.window.set_cursor(None)
        else:
            #gdk_win = gtk.gdk.Window(self.window.window,gtk.gdk.screen_width(),gtk.gdk.screen_height(),gtk.gdk.WINDOW_CHILD,0,gtk.gdk.INPUT_ONLY)
            mode = gtk.gdk.Cursor(icono)
            #gdk_win.set_cursor(mode)
            self.parent.hbox0.window.set_cursor(mode)'''

    def screen_changed(self,widget, old_screen=None):
        # To check if the display supports alpha channels, get the colormap
        screen = widget.get_screen()
        colormap = screen.get_rgba_colormap()
        if colormap == None:
            print 'Your screen does not support alpha channels!'
            colormap = screen.get_rgb_colormap()
            self.supports_alpha = False
        else:
            #print 'Your screen supports alpha channels!'
            self.supports_alpha = True
        # Now we have a colormap appropriate for the screen, use it
        widget.set_colormap(colormap)
        return False
    
    def chck_n_hide_TB(self):
        '''check if the cursor is over the toolbar'''
        Mx, My, mods = self.parent.rootwin.get_pointer()
        x0,y0 = self.parent.window.get_position()
        size = self.parent.window.allocation
        #size.width, size.height
        if ( (size.width-50<=Mx-x0<=size.width) and (0<=My-y0<=size.height) ):#is the pointer over the toolbar?
            self.shw_TB = 0
        else:
            self.shw_TB += 1
        if self.shw_TB == 5: #when the mouse is out for 5 s the toolbar is hiden
            self.parent.TB.set_visible(False)
            self.trigger_expose()
        return True
    
    def signs_timeout(self):
        '''timeout to hide the scale sign'''
        if self.show_scale > 0:
            self.show_scale -= 1
        elif self.show_scale == 0:
            self.trigger_expose()
            self.show_scale = -1 #hide scale sign
        return True
    
    def cinematica(self):
        '''a long with gobject.timeout_add(70,self.cm.cinematica) limits the refrash rate for the background'''
        if self.update_bg: #if the flag is set refresh the BG
            rect = gtk.gdk.Rectangle (0,0,*self.parent.window.get_size())
            self.parent.window.window.invalidate_rect(rect,True) #this triggers the expose event
            self.update_bg = False
        return True
    
    def flip(self,H_V): #flip pixbuf
        self.fh.pixbuf = self.fh.pixbuf.flip(H_V)
        self.trigger_expose()
        
        
    def expose(self,widget, event):
        #print "expose!"
        cr = widget.window.cairo_create()
        cr.set_operator(cairo.OPERATOR_SOURCE)# Draw the background
        
        if self.transparency == self.FAKE:
            n,m = self.parent.window.get_position()
            cr.set_source_pixbuf(self.bg,-n,-m)
            cr.paint()
            cr.set_operator(cairo.OPERATOR_OVER)
        if self.supports_alpha and self.transparency:
            cr.set_source_rgba(*(self.BG_color + [self.alpha]))#(0.0, 0.0, 0.0,self.alpha)
            cr.paint()
        else:
            cr.set_source_rgb(*self.BG_color)
            cr.paint()
            
        cr.set_operator(cairo.OPERATOR_OVER)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        width, height = widget.window.get_size()
        self.draw_bg_txt(cr, self.msg)
        if self.draw_pic:
        
            if self.scale != 1.0 or self.rot_ang != 0:
                cr.save()
                matrix = cairo.Matrix ( 1, 0, 0, 1,self.imgX,self.imgY)
                cr.transform ( matrix )
                cr.scale(self.scale,self.scale)
                if self.rot_ang !=0:
                    matrix = cairo.Matrix ( 1, 0, 0, 1,self.img_W/2,self.img_H/2)
                    cr.transform ( matrix )
                    cr.rotate(-self.rot_ang)
                    cr.set_source_pixbuf(self.fh.pixbuf,-self.img_W/2,-self.img_H/2)
                else:
                    cr.set_source_pixbuf(self.fh.pixbuf,0,0)#,self.imgX,self.imgY)
                cr.paint()
                cr.restore()
            else:
                cr.set_source_pixbuf(self.fh.pixbuf,self.imgX,self.imgY)
                #cr.rectangle(self.imgX,self.imgY,self.fh.pixbuf.get_width(),self.fh.pixbuf.get_height())
                #cr.fill()
                cr.paint()
            cr.set_line_width(0)
            cr.stroke()
            cr.set_line_width(2)
            if self.rot_phase == 1:#inicia rotacion
                cr.set_source_rgba(0,1,0,0.8)
                cr.arc(self.rot_c_X,self.rot_c_Y, 100, 0, 2.0*3.15)
                cr.set_line_width(4)
                cr.stroke ()
                #y dibujar el angulo en un cuadrito
                cr.set_source_rgb(1,1,1)
                cr.move_to(self.rot_c_X+20,self.rot_c_Y-25)
                cr.set_line_width(28)
                cr.line_to(self.rot_c_X+150,self.rot_c_Y-25)
                cr.stroke()
                cr.set_source_rgb(0.1,0.1,0.1)
                cr.move_to(self.rot_c_X+20,self.rot_c_Y-25)
                cr.set_line_width(25)
                cr.line_to(self.rot_c_X+150,self.rot_c_Y-25)
                cr.stroke()
                cr.set_source_rgb(1,1,1)
                cr.select_font_face("Georgia",cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                cr.set_font_size(15)
                cr.move_to(self.rot_c_X+25,self.rot_c_Y-20)
                cr.show_text("%.f" % (180*self.rot_ang/math.pi))
            elif self.rot_phase == 2:#rotando
                cr.set_source_rgba(0.3,0.3,0.3,0.8)
                cr.arc(self.rot_c_X,self.rot_c_Y, 100, 0, 2.0*3.15)
                cr.stroke ()
                cr.set_source_rgba(0,0,1,0.8)
                cr.move_to(self.rot_c_X,self.rot_c_Y)
                cr.line_to(self.rot_r_X,self.rot_r_Y)
                cr.stroke ()
                cr.set_source_rgba(1,0,0,0.8)
                cr.move_to(self.rot_c_X,self.rot_c_Y)
                cr.line_to(self.M_X,self.M_Y)
                cr.stroke ()            
                #y dibujar el angulo en un cuadrito
                cr.set_source_rgb(1,1,1)
                cr.move_to(self.rot_c_X+20,self.rot_c_Y-25)
                cr.set_line_width(28)
                cr.line_to(self.rot_c_X+150,self.rot_c_Y-25)
                cr.stroke()
                cr.set_source_rgb(0.1,0.1,0.1)
                cr.move_to(self.rot_c_X+20,self.rot_c_Y-25)
                cr.set_line_width(25)
                cr.line_to(self.rot_c_X+150,self.rot_c_Y-25)
                cr.stroke()
                cr.set_source_rgb(1,1,1)
                cr.select_font_face("Georgia",cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                cr.set_font_size(15)
                cr.move_to(self.rot_c_X+25,self.rot_c_Y-20)
                cr.show_text("%.f" % (180*self.rot_ang/math.pi))
        if self.parent.TB.get_visible():
            cr.set_source_rgb(0,0,0)
            self.alloc = self.parent.TB.get_allocation()
            cr.move_to(width-12-self.alloc.width,0)
            cr.line_to(width-12-self.alloc.width,height)
            cr.set_line_width(2)
            cr.stroke()
        if self.draw_pic and (self.show_scale > 0):
            cr.set_source_rgb(1,1,1)
            cr.move_to(self.M_X+20,self.M_Y-25)
            cr.set_line_width(28)
            cr.line_to(self.M_X+150,self.M_Y-25)
            cr.stroke()
            cr.set_source_rgb(0.1,0.1,0.1)
            cr.move_to(self.M_X+20,self.M_Y-25)
            cr.set_line_width(25)
            cr.line_to(self.M_X+150,self.M_Y-25)
            cr.stroke()
            cr.set_source_rgb(1,1,1)
            cr.select_font_face("Georgia",cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(15)
            cr.move_to(self.M_X+20,self.M_Y-20)
            cr.show_text("  scale: %.2f" % self.scale)
        return False

    def draw_bg_txt(self,cr,mnsj):
        cr.set_source_rgb(1,1,1)
        cr.select_font_face("Georgia",cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(12)
        #x_bearing, y_bearing, width, height = self.cr.text_extents(self.msg)[:4]
        new_line = 60
        for m in mnsj:#.split("\n"):
            new_line += 20
            cr.move_to(20,new_line)
            cr.show_text(m)
            
    def click_over_image(self,event):
        '''find out is the click was over the image'''
        if self.rot_ang == 0:
            return ( (self.imgX<=event.x<=self.imgX+self.fh.pixbuf.get_width()*self.scale) and (self.imgY<=event.y<=self.imgY+self.fh.pixbuf.get_height()*self.scale) )
        else:
            #rotar y trasladar la coordenada del mouse
            #not implemented yet
            return ( (self.imgX<=event.x<=self.imgX+self.fh.pixbuf.get_width()*self.scale) and (self.imgY<=event.y<=self.imgY+self.fh.pixbuf.get_height()*self.scale) )
            
    def on_scroll_event(self,widget, event):
        '''change the image scale'''
        if ( self.click_over_image(event) ): # was the event over the image?
            self.M_X,self.M_Y = event.x,event.y
            old_scale = self.scale 
            self.scale *= {gtk.gdk.SCROLL_UP:1.1,gtk.gdk.SCROLL_DOWN:0.9}[event.direction]
            self.imgX = self.M_X - ((self.M_X - self.imgX)*self.scale/old_scale)
            self.imgY = self.M_Y - ((self.M_Y - self.imgY)*self.scale/old_scale)
            #get the new coordinates so the image seem to be attached to the cursor while changing its scale
            self.show_scale = 10
            self.trigger_expose()
            #self.update_bg = True
            '''
    def on_scroll_event_2(self,widget, event):
        if ( (self.imgX<=event.x<=self.imgX+self.fh.pixbuf.get_width()*self.scale) and (self.imgY<=event.y<=self.imgY+self.fh.pixbuf.get_height()*self.scale) ):
            self.M_X,self.M_Y = event.x,event.y
            escala_old = self.scale 
            self.scale *= {gtk.gdk.SCROLL_UP:1.1,gtk.gdk.SCROLL_DOWN:0.9}[event.direction]
            self.imgX = self.M_X - ((self.M_X - self.imgX)*self.scale/escala_old)
            self.imgY = self.M_Y - ((self.M_Y - self.imgY)*self.scale/escala_old)'''
        
    def button_press_event(self,widget, event):
        #print "button_press_event", event.button
        self.click_in = self.click_over_image(event)
        self.oldMX,self.oldMY = event.x,event.y
        self.oldIX,self.oldIY = self.imgX,self.imgY
        if self.click_in and (event.button == 1):
            self.chng_cursor(gtk.gdk.FLEUR)
        if self.click_in and (event.button == 2):
            w,h = self.parent.window.get_size()
            #self.imgX = (w-self.fh.pixbuf.get_width())/2
            #self.imgY = (h-self.fh.pixbuf.get_height())/2
            self.scale = 1
            self.rot_ang = 0
            #w,h = self.parent.window.get_size()
            if self.fh.pixbuf.get_height() > h or self.fh.pixbuf.get_width() > w:
                if float(self.fh.pixbuf.get_height())/h < float(self.fh.pixbuf.get_width())/w:
                    self.scale = w/float(self.fh.pixbuf.get_width())
                    self.imgX = 0
                    self.imgY = (h-self.fh.pixbuf.get_height()*self.scale)/2
                else:
                    self.scale = h/float(self.fh.pixbuf.get_height())
                    self.imgX = (w-self.fh.pixbuf.get_width()*self.scale)/2
                    self.imgY = 0
            else:
                self.imgX = (w-self.fh.pixbuf.get_width())/2
                self.imgY = (h-self.fh.pixbuf.get_height())/2
        if event.button == 3:
            self.rot_phase = 1
            self.rot_c_X,self.rot_c_Y = event.x,event.y
            self.trigger_expose()
            #self.update_bg = True
            self.chng_cursor()
            
    def button_release_event(self,widget, event):
        self.rot_phase = 0 #stop drawing the rotation indicator
        #self.update_bg = True #set the flag so the BG is updated
        self.trigger_expose()
        self.chng_cursor(None) #change cursor to normal
        
    def motion_notify_event(self,widget, event):
        if self.click_in and (event.state & gtk.gdk.BUTTON1_MASK):
            if event.is_hint:
                X,Y, state = event.window.get_pointer()
            else: X,Y = event.x,event.y
            self.imgX,self.imgY = (self.oldIX + X-self.oldMX),(self.oldIY + Y-self.oldMY)
            self.trigger_expose()
        if event.state & gtk.gdk.BUTTON3_MASK:
            if event.is_hint:
                X,Y, state = event.window.get_pointer()
            else: X,Y = event.x,event.y
            if (self.rot_phase == 1) and ( 10000 < ( (self.rot_c_X-X)**2+(self.rot_c_Y-Y)**2 ) ):
                self.rot_phase = 2
                self.rot_r_X,self.M_X,self.rot_r_Y,self.M_Y = X,X,Y,Y
                self.ref_ang = math.atan( float(self.rot_c_X-X)/(Y-self.rot_c_Y) )
                #self.update_bg = True
                self.trigger_expose()
            if (self.rot_phase == 2) and ( 10000 < ( (self.rot_c_X-X)**2+(self.rot_c_Y-Y)**2 ) ):
                self.M_X,self.M_Y = X,Y
                if self.rot_c_X-X == 0:
                    self.rot_ang = {True:math.pi/2,False:3*math.pi/2}[(self.rot_c_Y-Y)>0]
                    #for the veertical position
                else:
                    if X-self.rot_c_X > 0:
                        self.rot_ang = math.atan( (self.rot_c_Y-Y)/float(X-self.rot_c_X) )
                    else:
                        self.rot_ang = math.atan( (Y-self.rot_c_Y)/float(self.rot_c_X-X) ) + math.pi
                self.trigger_expose()
            
    def trigger_expose(self):
        if self.limit:
            self.update_bg = True
        else:
            try:
                rect = gtk.gdk.Rectangle (0,0,*self.parent.window.get_size())
                self.parent.window.window.invalidate_rect(rect,True)
            except: print traceback.format_exc()
    
    def zoom_in_out(self,widget,in_out):
        old_scale = self.scale
        w,h = self.parent.window.get_size()
        self.scale *= {True:1.2,False:0.8}[in_out]
        self.imgX = w/2 - ((w/2 - self.imgX)*self.scale/old_scale)
        self.imgY = h/2 - ((h/2 - self.imgY)*self.scale/old_scale) #image change scale but dont jump to the center of the screen
        #print self.imgX,self.imgY
        self.show_scale = 10
        self.M_X,self.M_Y = w/2,h/2
        self.trigger_expose()
    
    def zoom_best_fit_one(self,widget,best=True):
        self.scale = 1
        self.rot_ang = 0
        w,h = self.parent.window.get_size()
        if best and (self.fh.pixbuf.get_height() > h or self.fh.pixbuf.get_width() > w):
            if float(self.fh.pixbuf.get_height())/h < float(self.fh.pixbuf.get_width())/w:
                self.scale = w/float(self.fh.pixbuf.get_width())
                
                self.imgX = 0
                self.imgY = (h-self.fh.pixbuf.get_height()*self.scale)/2
            else:
                self.scale = h/float(self.fh.pixbuf.get_height())
                self.imgX = (w-self.fh.pixbuf.get_width()*self.scale)/2
                self.imgY = 0
        else:
            self.imgX = (w-self.fh.pixbuf.get_width())/2
            self.imgY = (h-self.fh.pixbuf.get_height())/2
        self.trigger_expose()
        
    def get_bg(self,waa=None):
        '''take a screenshot for the fake transparency'''
        w = gtk.gdk.get_default_root_window()
        sz = w.get_size()
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
        self.bg = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
        #pb.save("screenshot.png","png")
        
