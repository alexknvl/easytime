#!/usr/bin/env python

from distutils.core import setup

setup(name='osunlp-easytime',
      version='0.2',
      description='A less error-prone date&time manipulation library',
      author='Alexander Konovalov',
      author_email='alex.knvl@gmail.com',
      packages=['easytime'],
      install_requires=[
          'pytz',
          'python-dateutil'
      ])
