from setuptools import setup, find_packages

setup(name='motmot.wxvideo',
      packages = find_packages(),
      namespace_packages = ['motmot'],
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
