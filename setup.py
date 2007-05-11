from setuptools import setup

from motmot_utils import get_svnversion_persistent
version_str = '0.4.dev%(svnversion)s'
version = get_svnversion_persistent('wxvideo/version.py',version_str)

setup(name='wxvideo',
      version=version,
      packages = ['wxvideo'],
      author='Andrew Straw',
      author_email='strawman@astraw.com',
      license='BSD',
      install_requires = ['wxwrap',
                          'imops>=0.1.dev808',
                          ],
      )
