=================
What is PySQLPool
=================

PySQLPool is at the heart a MySQL Connection Pooling library for use with the MySQLDB Python bindings.

Part of the PySQLPool is the MySQL Query class that handles all the thread safe connection locking, 
connection management in association with the Connection Manager, and cursor management. 
Leaving all the work you have to do in your code is write MySQL Queries. Saving you hours of work.

============
Installation
============

Linux/Mac OS X
==============
cd PySQLPool
python setup.py build
sudo python setup.py install

Windows
=======
cd PySQLPool
python setup.py build 
python setup.py install 

====================
How to Use PySQLPool
====================

Documentation can be read locally at doc/index.rst or via the web at http://packages.python.org/PySQLPool

You can also generate your own html docs via the make file in doc/. This will produce the same docs as 
hosted on the website.

=======
License
=======

PySQLPool is licensed under the LGPL. You can find out more in the included LICENSE file.

=================================================
Got a Bug, Question, or Idea to Improve PySQLPool
=================================================

Bugs can be submitted at https://bugs.launchpad.net/pysqlpool
Blueprints/Ideas can be submitted at https://blueprints.launchpad.net/pysqlpool
Questions/Answers can be submitted at https://answers.edge.launchpad.net/pysqlpool

=====
Links
=====

Homepages: 
* https://github.com/nerdynick/PySQLPool 
* http://code.google.com/p/pysqlpool/
* https://launchpad.net/pysqlpool/
          
Documentation: 
* http://packages.python.org/PySQLPool/