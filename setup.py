from setuptools import setup, find_packages

setup(name='motmot.wxvideo',
      description='wx viewer of image sequences',
      long_description = \
"""Allows for display and resizing/rotation of images.

This is a subpackage of the motmot family of digital image utilities.
""",
      packages = find_packages(),
      namespace_packages = ['motmot'],
      url='http://code.astraw.com/projects/motmot',
      version='0.5.2',
      author='Andrew Straw',
      author_email='strawman@astraw.com',
      license='BSD',
      install_requires=[
          'numpy>=1.0.4',
          'PIL>=1.1.6',
          'motmot.imops',
          'wxPython>=2.8'
          ],
      )
