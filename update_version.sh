#!/usr/bin/env sh
sed -e "s#^__version__ = .*#__version__ = '$1'#" -i src/PySQLPool/__init__.py setup.py
