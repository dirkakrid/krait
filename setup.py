#!/usr/bin/env python

from distutils.core import setup

setup(name='krait',
      verstion='0.1',
      description='Powershell Enabler for Junos Devices',
      author='Tyler Christiansen',
      author_email='tyler@tylerc.me',
      url='http://tylerc.me/blog/',
      packages=['krait'],
      package_dir={'': 'lib'}
     )
