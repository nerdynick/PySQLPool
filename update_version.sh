#!/usr/bin/env sh
sed -e "s#^__version__ = .*#__version__ = '$1'#" -i PySQLPool/PySQLPool/__init__.py setup.py
