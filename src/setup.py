#!/usr/bin/env python

from distutils.core import setup
import PySQLPool

setup(name='PySQLPool',
      version=PySQLPool.__version__,
      license='LGPL V3',
      platforms=['ALL'],
      description='Python MySQL Connection Pooling and MySQL Query management',
      author=PySQLPool.__author__,
      author_email=PySQLPool.__author_email__,
      url='http://code.google.com/p/pysqlpool/',
      download_url="http://code.google.com/p/pysqlpool/downloads/list",
      classifiers = [
                     'Topic :: Software Development :: Libraries :: Python Modules',
                     'Topic :: Database',
                     'Programming Language :: Python',
                     'Operating System :: OS Independent',
                     'Development Status :: 5 - Production/Stable'],
      requires=['MySQL-python'],
      provides=['pysqlpool','PySQLPool'],
      packages=['PySQLPool'],
     )