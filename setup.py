#!/usr/bin/env python

from distutils.core import setup

__version__ = '0.3.7'
__author__ = 'Nick Verbeck'
__author_email__ = 'nerdynick@gmail.com'

setup(name='PySQLPool',
      version=__version__,
      author=__author__,
      author_email=__author_email__,
      license='LGPL V3',
      platforms=['ALL'],
      description='Python MySQL Connection Pooling and MySQL Query management',
      url='https://github.com/nerdynick/PySQLPool/',
      download_url="http://code.google.com/p/pysqlpool/downloads/list",
      classifiers = [
                     'Topic :: Software Development :: Libraries :: Python Modules',
                     'Topic :: Database',
                     'Programming Language :: Python',
                     'Operating System :: OS Independent',
                     'Development Status :: 5 - Production/Stable'],
      install_requires=['MySQL_python'],
      provides=['pysqlpool','PySQLPool'],
      packages=['PySQLPool'],
      package_dir={'PySQLPool': 'PySQLPool/PySQLPool'}
     )
