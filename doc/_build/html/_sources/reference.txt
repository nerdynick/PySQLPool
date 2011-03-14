.. "reference.rst" file
.. moduleauthor:: NerdyNick <nerdynick@gmail.com>
.. sectionauthor:: NerdyNick <nerdynick@gmail.com>
.. sectionauthor:: NerdyNick <nerdynick@gmail.com>
.. module:: PySQLPool
   :synopsis: MySQL Connection Pooling

===========================
PySQLPool Object Reference
===========================

This is a standard object reference for PySQLPool. Being that PySQLPool is a connection pooling wrapper 
around MySQLdb many of the same methods and parameters are support. You can kind hints or further docs 
by reading the MySQLdb Documentation at http://mysql-python.sourceforge.net/MySQLdb-1.2.2/

:mod:`PySQLPool`
==================

.. attribute:: __version__
   
   PySQLPool Version Number

.. attribute:: __author__
   
   PySQLPool Author String

.. function:: getNewConnection(*args, **kargs)
   
   Fast function to generate a new PySQLConnection instance. Arguments are those of :class:`PySQLConnection`

.. function:: getNewQuery([connection[, commitOnEnd[, **kargs]]])
   
   Fast method to generate a new PySQLQuery instance.
   
   If an instance of a PySQLConnection object is passes for the connection parameter. It will be used for the 
   connection. Otherwise \**kargs will be used to generate a PySQLConnection instance via the :meth:`getNewConnection` method.

.. function:: getNewPool()
   
   Returns a reference to the current PySQLPool object

.. function:: terminatePool()
   
   Causes PySQLPool to commit and terminate all your current MySQL connections

.. function:: commitPool()
   
   Causes PySQLPool to commit all your current MySQL connections

.. function:: cleanupPool()
   
   Causes PySQLPool to analyse all current MySQL connections, and clean up an dead connections.
  


:mod:`PySQLPool.PySQLQuery`
=============================

The PySQLQuery class is by far one of the biggest work horses in the whole PySQLPool library, next to the PySQLPool class.
It is responsable for handaling the execution of your query(s). Which in itself is a lot of work. PySQLQuery handles talking 
to the heart of PySQLPool, The PySQLPool class. To fetch a new connection or one that has been estabished. It then creates a 
MySQL cursor object to handle the execution of your sql statement against your MySQL database. 

.. class:: PySQLQuery(PySQLConnectionObj[, commitOnEnd])

   .. attribute:: Pool
   
       Used to store a reference to the PySQLPool object

   .. attribute:: connInfo
   
       Used to store the connection information to be used for talking to the db. This is a PySQLConnection instance.

   .. attribute:: commitOnEnd
   
       A boolean flag used to tell the connection that it should auto commit your statement at the end of its execution.

   .. attribute:: record
   
       A storage reference to your results that where returned from your last select statement.

   .. attribute:: rowcount
   
       The number of rows returned by your last select statement.

   .. attribute:: affectedRows
   
       The number of affected rows that your last delete/insert/update statement affected.

   .. attribute:: conn
   
       An internaly used reference to the current locked connection as returned by the PySQLPool class. This is an 
       instance of a PySQLConnectionManager object.

   .. attribute:: lastError
   
       A reference to the last MySQL error as returned by the under lying MySQLdb library. You can reference this if you need. 
       But PySQLQuery will raise this error forward for you to catch yourself.

   .. attribute:: lastInsertID
   
       The last auto incrament ID that an insert statement create.

   .. method:: __del__()
   
       The destructor method used for freeing up any locked connections that may not have be release do to some reason. 
   
   .. method:: Query(query[, args])
   
       Depricated alias for :meth:`query`
       
   .. method:: query(query[, args])
   
       Executes the given query.
       
       query - string, query to execute on server
       args - optional sequence or mapping, parameters to use with query
       
       Note: If args is a sequence, then %s must be used as the parameter placeholder in the query. 
       If a mapping is used, %(key)s must be used as the placeholder.
       
       Returns the number of affected rows.

   .. method:: QueryOne(query[, args])
   
       Depricated alias for :meth:`queryOne`
       
   .. method:: queryOne(query[, args])
   
       A generator style version of :meth:`query`. 
       
       Parameters are the same as :meth:`query`, but instead of fetching all the data from the server at once.
       It is returned one row at a time for every iteration. Each row will be returned as well as record can 
       still be used to access the current row.

   .. method:: queryMany(query, args)
   .. method:: executeMany(query, args)
   
       Execute a multi-row query.
       
       query - string, query to execute on server
       args - sequence of sequences or mappings, parameters to use with query.
       
       Returns the number of affected rows

   .. method:: queryMulti(queries)
   .. method:: executeMulti(queries)
   
       Executes a sequence of query strings
       
       Each sequence item and be a sequence or a string. If item is a sequence the 1st item but be the query. 
       The 2nd must be the replacement sequence or mapping to use with the query. 
       
       Returns the total number of affected rows

   .. method:: _GetConnection()
   
       Private method used to fetch a connection from the central pool of connections

   .. method:: _ReturnConnection()
   
       Private method used to return a connection to the central pool of connections
       
   .. method:: escape()
   
       Varius string escape methods as provided by MySQLdb. Each matchs a function of the same name in MySQLdb  
       
   .. method:: escapeString()
       
       See :meth:`escape`
       
   .. method:: escape_string()
       
       See :meth:`escape`



:mod:`PySQLPool.PySQLPool`
===========================

.. class:: PySQLPool()

   .. attribute:: __pool
    
   .. attribute:: maxActiveConnections
    
   .. attribute:: maxActivePerConnection
    
   .. method:: Terminate()
    
   .. method:: Cleanup()
    
   .. method:: Commit()
    
   .. method:: GetConnection(PySQLConnectionObj)
    
   .. method:: returnConnection(connObj)



:mod:`PySQLPool.PySQLConnection`
=================================

.. attribute:: connection_timeout

A `datetime.timedelta` representing your default MySQL connection_timeout. This is used 
to improve performance with checking to see if connections are valid and reconnecting if needed. Each
connection instance maintains a timestamp of its last activity. That is updated for every query or test.
The connection is auto tested for every new instance of a PySQLQuery created on its initial fetching 
of a connection.

.. class:: PySQLConnection([host, [user, [passwd, [db, [port]]]]], **kargs)
	
   Command Pattern Object to store connection information for use in PySQLPool
	
   Supported kargs are:
	* **host** - string, host to connect
	* **user,username** - string, user to connect as
	* **passwd,password** - string, password to use
	* **db,schema** - string, database to use
	* **port** - integer, TCP/IP port to connect to
	* **unix_socket** - string, location of unix_socket to use
	* **conv** - conversion dictionary, see MySQLdb.converters
	* **connect_timeout** - number of seconds to wait before the connection attempt fails.
	* **compress** - if set, compression is enabled
	* **named_pipe** - if set, a named pipe is used to connect (Windows only)
	* **init_command** - command which is run once the connection is created
	* **read_default_file** - file from which default client values are read
	* **read_default_group** - configuration group to use from the default file
	* **cursorclass** - class object, used to create cursors (keyword only)
	* **use_unicode** - If True, text-like columns are returned as unicode objects using the 
	  connection's character set. Otherwise, text-like columns are returned as strings. 
	  columns are returned as normal strings. Unicode objects will always be encoded to 
	  the connection's character set regardless of this setting.
	* **charset** - If supplied, the connection character set will be changed to this character set (MySQL-4.1 and newer). 
	  This implies use_unicode=True
	* **sql_mode** - If supplied, the session SQL mode will be changed to this setting (MySQL-4.1 and newer). 
	  For more details and legal values, see the MySQL documentation.
	* **client_flag** - integer, flags to use or 0 (see MySQL docs or constants/CLIENTS.py)
	* **ssl** - dictionary or mapping, contains SSL connection parameters; see the MySQL documentation for more details (mysql_ssl_set()). 
	  If this is set, and the client does not support SSL, NotSupportedError will be raised.
	* **local_inifile** - integer, non-zero enables LOAD LOCAL INFILE; zero disables
	
   Note: There are a number of undocumented, non-standard methods. 
   See the documentation for the MySQL C API for some hints on what they do.

   .. attribute:: info
   
   Dictionary containing the connection info to be passed off to the MySQLdb layer

   .. attribute:: key
   
   An auto generated md5 checksum to represent your connection in the pool. This is generated off of the
   username, password, host, and db/schema.

   .. method:: __getattr__(name)
   
       Accessor to :attr:`info`


.. class:: PySQLConnectionManager

   .. method:: __init__(PySQLConnectionObj)

   .. method:: updateCheckTime()

   .. method:: Connect()

   .. method:: ReConnect()

   .. method:: TestConnection(forceCheck = False)
   
   .. method:: Commit()
   
   .. method:: Close()