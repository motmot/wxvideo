import sys, traceback

from wxwrap import wx
import numpy
import imops

class DynamicImageCanvas(wx.Window):
    
    def __init__(self,*args,**kw):
        wx.Window.__init__(*(self,)+args, **kw)
        #w,h=10,10
        self.bitmap =wx.EmptyBitmap(0,0)#w, h)
        if 1:
            drawDC = wx.MemoryDC()
            #assert drawDC.Ok(), "drawDC not OK"
            drawDC.SelectObject( self.bitmap ) # draw into bmp
            drawDC.SetBrush(wx.Brush(self.GetBackgroundColour()))
            drawDC.Clear()
        
        wx.EVT_PAINT(self, self._onPaint)
        self.id_val = None
        self.do_draw_points = True
        self.mirror_display = False
        self.display_rotate_180 = False
        
    def set_clipping(self,val):
        print 'ignoring set_clipping command in wxvideo: clipping not implemented'

    def update_image_and_drawings(self,
                                  id_val,
                                  image,
                                  format=None,
                                  points=None,
                                  linesegs=None,
                                  xoffset=0,
                                  yoffset=0):
        # create bitmap, don't paint on screen
        if points is None:
            points = []
        if linesegs is None:
            linesegs = []
        if format is None:
            raise ValueError("must specify format")
        if xoffset != 0 or yoffset != 0:
            raise NotImplementedError("offset (%d,%d) not yet supported"%(xoffset,yoffset))

        rgb8 = imops.to_rgb8(format,image)

        if self.id_val is None:
            self.id_val = id_val
        if id_val != self.id_val:
            raise NotImplementedError("only 1 image source currently supported")
        
        h,w,three = rgb8.shape
        image = wx.EmptyImage(w,h)
        
        if 0: # now we do the whole thing
            # wx seems to flip data LR
            rgb8 = rgb8[:,::-1]
            
        # XXX TODO could eliminate data copy here?
        image.SetData( rgb8.tostring() )
        bmp = wx.BitmapFromImage(image)

        # now draw into bmp

        drawDC = wx.MemoryDC()
        #assert drawDC.Ok(), "drawDC not OK"
        drawDC.SelectObject( bmp ) # draw into bmp
        drawDC.SetPen(wx.Pen('GREEN'))
        drawDC.SetBrush(wx.Brush(wx.Colour(255,255,255), wx.TRANSPARENT))
        point_radius=8
        if self.do_draw_points:
            for pt in points:
                drawDC.DrawCircle(int(pt[0]),int(pt[1]),point_radius)
            for lineseg in linesegs:
                drawDC.DrawLine(*lineseg)

        if self.mirror_display:
            img = wx.ImageFromBitmap(bmp)
            img = img.Mirror(True)
            if self.display_rotate_180:
                img = img.Rotate90()
                img = img.Rotate90()
            bmp = wx.BitmapFromImage(img)
        elif self.display_rotate_180:
            img = wx.ImageFromBitmap(bmp)
            img = img.Rotate90()
            img = img.Rotate90()
            bmp = wx.BitmapFromImage(img)
        
        self.bitmap = bmp

    def set_flip_LR(self, val):
        self.mirror_display = val
        
    def set_rotate_180(self, val):
        self.display_rotate_180 = val
        
    def gui_repaint(self, drawDC=None):
        """blit bitmap to DC"""
        if drawDC is None:
            drawDC=wx.ClientDC(self)

        drawDC.BeginDrawing()
        drawDC.DrawBitmap(self.bitmap, 0, 0)
        drawDC.EndDrawing()  

    def _onPaint(self, evt):
        """called by OS during paint event to paint screen"""
        self.gui_repaint(drawDC=wx.PaintDC(self))
        evt.Skip()
