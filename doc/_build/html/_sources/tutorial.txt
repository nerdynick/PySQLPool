.. The "tutorial.rst" file

==============================
Getting Started with PySQLPool
==============================

The basic usage of PySQLPool is pretty simple as you can see in this basic example::

    import PySQLPool
    
    connection = PySQLPool.getNewConnection(username='root', password='123456', host='localhost', db='mydb')
    query = PySQLPool.getNewQuery(connection)
    query.Query('select * from table')
    for row in query.record:
        print row['column']

Selecting Data
==============

Here is how you would select a set of data from the DB and print it out

>>> query.Query('select * from table')
>>> for row in query.record:
>>>     print 'Column Value:', row['column']
Column Value: 0


Updating Data
=============

Here is how you would update a table and see how many rows your update statement affected

>>> query.Query('update table set column = 1')
>>> print 'Affected Rows:', query.affectedRows
Affected Rows: 10

Inserting New Data
==================

Here is how you would insert a new row and get back its insert ID for Auto-Increment indexes

>>> query.Query('insert into table ('column') values ('1')')
>>> print 'Last Insert ID:', query.lastInsertID
Last Insert ID: 11


Using PySQLPool with Threads
============================

When using PySQLPool with threads you need to do things a little bit different from a single threaded app.
The following example will show you a basic code structure you would use with a thread::

    import PySQLPool
    import threading
    
    connection = PySQLPool.getNewConnection(username='root', password='123456', host='localhost', db='mydb')
    
    class MyThread(threading.thread):
    	def __init__(self):
    		...
    		
        def run(self):
            query = PySQLPool.getNewQuery(connection)
            query.Query('insert into table ('column') values ('1')')
            
By requesting a new PySQLQuery object in the threads run method you allow the pooling layer to create new connections
to the DB as needed for each thread. Don't worry you will not create 1 connect per thread but will create new ones as
demand rises based on speed of threads and query execution time, but you will not create more then the limit.

Setting the Max Connection Limit
================================

The max connection limit is a limiter on the auto creation of new connections based on thread demand. The limit is set
globally to be used by each set of connection credentials. What that means is that for each set of connection arguments
you use, specifically the host/username/password/db, the max connection limiter will keep those connections <= to its 
value. There currently is no way to set a limit per connection credentials.

By default the limit is set to 10, but you can change it farely easy.::

    import PySQLPool
    PySQLPool.getNewPool().maxActiveConnections = 1
    

Stream Selected Data
====================

Sometimes you may be dealing with a very large dataset and would wish not to load it all up into memory on your local
machine, but would rather let it stream back from the MySQL server row by row. You can achieve this by simply changing
out what method you call on your PySQLQuery object.::

    import PySQLPool
    
    connection = PySQLPool.getNewConnection(username='root', password='123456', host='localhost', db='mydb')
    query = PySQLPool.getNewQuery(connection)
    query.QueryOne('select * from table')
    for row in query.record:
        print row['column']
        
As you will notice we switched out the query.Query() with a query.QueryOne(). This causes PySQLPool/MySQLdb to return
back to you a Python Generator that will fetch from the server row by row as you iterate through the results.

