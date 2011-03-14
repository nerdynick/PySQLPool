=====
FAQs
=====

In an attempt to help answer some questions preemptively. A FAQ page has been create along 
side the with the docs. Lets hope this helps. 

How do I enable debugging?
===========================

Currently debugging is very limited, but we do contain a simple debugging capability. You can 
enable debugging by assigning PySQLQuery.logging_path to a string value of a file to write the 
debugging output to. This will cause every query executed and any errors to be written to the 
supplied file.

Example::

    import PySQLPool
    
    PySQLPool.PySQLQuery.logging_path = '/path/to/file.txt'



What type of exception are raised?
===================================

At this time PySQLPool does not wrap the exceptions that come out of MySQLdb. So any and all errors 
thrown from any of your queries and/or other actions by MySQLdb will be of its types. Of which the base is
MySQLdb.Error. To find out what error you have caused. MySQLdb.Error contains a two-element tuple called args.
The 1st value will contain the MySQL error number, and the second will contain the error message.

Example::

    try:
        connection = PySQLPool.getNewConnection(username='root', password='123456', host='localhost', db='mydb')
        query = PySQLPool.getNewQuery(connection)
        query.Query('select * from table')
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit (1)
