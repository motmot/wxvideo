************************************************************************************
:mod:`motmot.wxvideo` -- display of uncompressed video using wxPython
************************************************************************************

.. module:: motmot.wxvideo
  :synopsis: display of uncompressed video using wxPython
.. index::
   module: motmot.wxvideo
   single: wxvideo

The wxvideo package allows display of numpy arrays into wxPython
OpenGL contexts. In particular, it defines a class
:class:`~motmot.wxvideo.wxvideo.DynamicImageCanvas`, which is a
subclass of :class:`wx.glcanvas.GLCanvas` into which arrays are
blitted.

See also :mod:`motmot.wxglvideo.simple_overlay` for hardware
accelarated video display in a manner compatible with this module.

:mod:`motmot.wxvideo.wxvideo`
=============================

.. automodule:: motmot.wxvideo.wxvideo
   :members:
   :show-inheritance:
