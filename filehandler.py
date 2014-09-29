import gtk, os, urllib, traceback, Image

class fh():
    def __init__(self,parent,cm):
        self.cm = cm
        self.parent = parent
        self.ruta_imagen = ""
        self.ruta_dir = ""
        #self.draw_pic = True
        self.tiene_animacion = False
        self.img = gtk.Image()
        self.Smart_bg_color = False #use the image's edge color as background color
        
    def open_new_image(self,path,w,h):
        self.img = gtk.Image()
        self.img.set_from_file(path)
        #print self.img.get_storage_type()
        #print self.img.get_storage_type() | 0
        if self.img.get_storage_type() == 6 :#if self.img.get_storage_type() == gtk.ImageType. GTK_IMAGE_ANIMATION :
            print "estatica? ",self.img.get_animation().is_static_image()
            self.pixbuf = self.img.get_animation().get_static_image()
        else: self.pixbuf = self.img.get_pixbuf()
        #self.pixbuf = gtk.gdk.pixbuf_new_from_file(path)
        self.ruta_imagen = path
        self.cm.draw_pic = True
        self.cm.scale = 1
        self.cm.rot_ang = 0
        #w,h = self.window.get_size()
        '''self.cm.img_H,self.cm.img_W = self.pixbuf.get_height(), self.pixbuf.get_width()
        if self.pixbuf.get_height() > h or self.pixbuf.get_width() > w:
            if float(self.pixbuf.get_height())/h < float(self.pixbuf.get_width())/w:
                self.cm.scale = w/float(self.pixbuf.get_width())
                self.cm.imgX = 0
                self.cm.imgY = (h-self.pixbuf.get_height()*self.cm.scale)/2
            else:
                self.cm.scale = h/float(self.pixbuf.get_height())
                self.cm.imgX = (w-self.pixbuf.get_width()*self.cm.scale)/2
                self.cm.imgY = 0
        else:
            self.cm.imgX = (w-self.pixbuf.get_width())/2
            self.cm.imgY = (h-self.pixbuf.get_height())/2'''
        self.cm.msg = [path[path.rfind("/")+1:] , str(self.pixbuf.get_width()) + "x" + str(self.pixbuf.get_height()) + " px", str (os.path.getsize(path)/1024) + " Kb"]
        self.parent.window.set_title("PV "+self.cm.msg[0])
        if self.Smart_bg_color:
            color = self.get_most_common_edge_colour(self.pixbuf)
            if color[3] == 0.0: self.cm.BG_color = [0.0,0.0,0.0] #debo poner el color del usurio despues. <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            else: self.cm.BG_color = color[:3]
        #self.cm.trigger_expose()
        self.cm.zoom_best_fit_one(True)
        
    def drag_n_drop_event(self, widget, context, x, y, selection, drag_id, eventtime):
        """Handle drag-n-drop events on the main layout area."""
        #copied from comix filehandler.py
        # The drag source is inside Comix itself, so we ignore.
        if (context.get_source_widget() is not None):
            return
        uris = selection.get_uris()
        if not uris:
            return
        #print uris
        uri = uris[0] # Open only one file.
        if uri.startswith('file://localhost/'):  # Correctly formatted.
            uri = uri[16:]
        elif uri.startswith('file:///'):  # Nautilus etc.
            uri = uri[7:]
        elif uri.startswith('file:/'):  # Xffm etc.
            uri = uri[5:]
            
        path = urllib.url2pathname(uri)
        print path
        if self.is_image_file(path): self.open_new_image(path,*self.parent.window.get_size())
        else: print "not an image file"
        
    def is_image_file(self,path):
        """Return True if the file at <path> is an image file recognized by PyGTK."""
        #copied from comix filehandler.py
        if os.path.isfile(path):
            about = gtk.gdk.pixbuf_get_file_info(path)
            return about is not None
        return False
    
    def get_most_common_edge_colour(self,pixbuf):
        """Return the most commonly occurring pixel value along the four edges
        of <pixbuf>. The return value is a sequence, (r, g, b), with 16 bit
        values.
    
        Note: This could be done more cleanly with subpixbuf(), but that
        doesn't work as expected together with get_pixels().
        """
        #copied from comix image.py
        width = pixbuf.get_width()
        height = pixbuf.get_height()
        top_edge = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, width, 1)
        bottom_edge = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, width, 1)
        left_edge = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, 1, height)
        right_edge = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, 1, height)
        pixbuf.copy_area(0, 0, width, 1, top_edge, 0, 0)
        pixbuf.copy_area(0, height - 1, width, 1, bottom_edge, 0, 0)
        pixbuf.copy_area(0, 0, 1, height, left_edge, 0, 0)
        pixbuf.copy_area(width - 1, 0, 1, height, right_edge, 0, 0)
        
        colour_count = {}
        for edge in (top_edge, bottom_edge, left_edge, right_edge):
            im = self.pixbuf_to_pil(edge)
            for count, colour in im.getcolors(im.size[0] * im.size[1]):
                colour_count[colour] = colour_count.setdefault(colour, 0) + count
        max_count = 0
        most_common_colour = None
        for colour, count in colour_count.iteritems():
            if count > max_count:
                max_count = count
                most_common_colour = colour
        #return [val * 257 for val in most_common_colour]
        return [val/255.0 for val in most_common_colour] #modified to get color in a float numbers 


    def pil_to_pixbuf(self,image):
        """Return a pixbuf created from the PIL <image>."""
        #copied from comix image.py
        imagestr = image.tostring()
        IS_RGBA = image.mode == 'RGBA'
        return gtk.gdk.pixbuf_new_from_data(imagestr, gtk.gdk.COLORSPACE_RGB,
            IS_RGBA, 8, image.size[0], image.size[1],
            (IS_RGBA and 4 or 3) * image.size[0])
    
    
    def pixbuf_to_pil(self,pixbuf):
        """Return a PIL image created from <pixbuf>."""
        #copied from comix image.py
        dimensions = pixbuf.get_width(), pixbuf.get_height()
        stride = pixbuf.get_rowstride()
        pixels = pixbuf.get_pixels()
        mode = pixbuf.get_has_alpha() and 'RGBA' or 'RGB'
        return Image.frombuffer(mode, dimensions, pixels, 'raw', mode, stride, 1)
