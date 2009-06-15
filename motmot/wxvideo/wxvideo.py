import sys, traceback

import wx
import numpy
import motmot.imops.imops as imops
import warnings

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
        self.lbrt = {}
        self.full_image_numpy = None
        self.doresize = False
        self.resize = 1

    def set_clipping(self,val):
        print 'ignoring set_clipping command in wxvideo: clipping not implemented'

    def get_resize(self):
        return self.resize

    def set_resize(self,val):
        self.doresize = val

    # so that use is the same as simple_overlay
    def get_child_canvas(self, id_val):
        return self

    def update_image_and_drawings(self,
                                  id_val,
                                  image,
                                  format=None,
                                  points=None,
                                  linesegs=None,
                                  point_colors=None,
                                  point_radii=None,
                                  lineseg_colors=None,
                                  lineseg_widths=None,
                                  xoffset=0,
                                  yoffset=0,
                                  doresize=None):

        # create bitmap, don't paint on screen
        if points is None:
            points = []
        if linesegs is None:
            linesegs = []
        if format is None:
            format='MONO8'
            warnings.warn('format unspecified - assuming MONO8')

        # if doresize is not input, then use the default value
        if doresize is None:
            doresize = self.doresize

        rgb8 = imops.to_rgb8(format,image)

        if doresize:
            from scipy.misc.pilutil import imresize

            # how much should we resize the image
            windowwidth = self.GetRect().GetWidth()
            windowheight = self.GetRect().GetHeight()
            imagewidth = rgb8.shape[1]
            imageheight = rgb8.shape[0]
            resizew = float(windowwidth) / float(imagewidth)
            resizeh = float(windowheight) / float(imageheight)
            self.resize = min(resizew,resizeh)
            # resize the image
            rgb8 = imresize(rgb8,self.resize)
            # scale all the points and lines
            pointscp = []
            for pt in points:
                pointscp.append([pt[0]*self.resize,pt[1]*self.resize])
            points = pointscp
            linesegscp = []
            for line in linesegs:
                linesegscp.append([line[0]*self.resize,line[1]*self.resize,line[2]*self.resize,line[3]*self.resize])
            linesegs = linesegscp

        if self.id_val is None:
            self.id_val = id_val
        if id_val != self.id_val:
            raise NotImplementedError("only 1 image source currently supported")

        h,w,three = rgb8.shape
        # get full image
        if self.full_image_numpy is not None:
            full_h, full_w, tmp = self.full_image_numpy.shape
            if h<full_h or w<full_w:
                self.full_image_numpy[yoffset:yoffset+h,xoffset:xoffset+w,:] = rgb8
                rgb8 = self.full_image_numpy
                h,w = full_h, full_w
        else:
            self.full_image_numpy = rgb8

        image = wx.EmptyImage(w,h)

        # XXX TODO could eliminate data copy here?
        image.SetData( rgb8.tostring() )
        bmp = wx.BitmapFromImage(image)

        # now draw into bmp

        drawDC = wx.MemoryDC()
        #assert drawDC.Ok(), "drawDC not OK"
        drawDC.SelectObject( bmp ) # draw into bmp
        drawDC.SetBrush(wx.Brush(wx.Colour(255,255,255), wx.TRANSPARENT))

        if self.do_draw_points and points is not None and len(points) > 0:
            if point_radii is None:
                point_radii = [ 8 ] * len(points)
            if point_colors is None:
                point_colors = [ (0,1,0) ]*len(points)
        if self.do_draw_points and linesegs is not None and len(linesegs) > 0:
            if lineseg_widths is None:
                lineseg_widths = [ 1 ] * len(linesegs)
            if lineseg_colors is None:
                lineseg_colors = [ (0,1,0) ]*len(linesegs)
        
        # fixing drawing point colors!!!
        if self.do_draw_points:
            for i in range(len(points)):

                # point
                pt = points[i]

                # point color
                ptcolor = point_colors[i]
                wxptcolor = wx.Colour(round(ptcolor[0]*255),
                                      round(ptcolor[1]*255),
                                      round(ptcolor[2]*255))
                
                # radius of point
                ptradius = point_radii[i]

                # draw it
                drawDC.SetPen(wx.Pen(colour=wxptcolor,
                                     width=1))
                drawDC.DrawCircle(int(pt[0]),int(pt[1]),ptradius)

            for i in range(len(linesegs)):
                lineseg = linesegs[i]
                linesegcolor = lineseg_colors[i]
                wxlinesegcolor = wx.Colour(round(linesegcolor[0]*255),
                                           round(linesegcolor[1]*255),
                                           round(linesegcolor[2]*255))
                linesegwidth = lineseg_widths[i]

                drawDC.SetPen(wx.Pen(colour=wxlinesegcolor,
                                     width=linesegwidth))
                drawDC.DrawLine(*lineseg)

        if id_val in self.lbrt:
            drawDC.SetPen(wx.Pen('GREEN',width=1))
            l,b,r,t = self.lbrt[id_val]
            drawDC.DrawLine(l,b, r,b)
            drawDC.DrawLine(r,b, r,t)
            drawDC.DrawLine(r,t, l,t)
            drawDC.DrawLine(l,t, l,b)

        img = wx.ImageFromBitmap(bmp)
        if self.mirror_display:
            if not self.display_rotate_180:
                img = img.Rotate90()
                img = img.Rotate90()
        else:
            img = img.Mirror(True)
            if not self.display_rotate_180:
                img = img.Rotate90()
                img = img.Rotate90()
        bmp = wx.BitmapFromImage(img)

        self.bitmap = bmp

    def set_lbrt(self,id_val,lbrt):
        self.lbrt[id_val]=lbrt

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
