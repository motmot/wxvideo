from setuptools import setup, find_packages
import os

kws = {}

setup(name='motmot.wxvideo',
      description='wx viewer of image sequences',
      long_description = \
"""Allows for display and resizing/rotation of images.

This is a subpackage of the motmot family of digital image utilities.
""",
      packages = find_packages(),
      namespace_packages = ['motmot'],
      url='http://code.astraw.com/projects/motmot',
      version='0.5.6',
      author='Andrew Straw',
      author_email='strawman@astraw.com',
      license='BSD',
      **kws)
