__version__ = '0.4'
__author__ = 'Nick Verbeck'
__author_email__ = 'nerdynick@gmail.com'

import logging
logger = None
log_level = logging.INFO

#We rename these for legacy support. Will phase out with 1.0 most likely
import connection
import query
import pool

#Connection short cuts
def getNewConnection(*args, **kargs):
	"""
	Quickly Create a new PySQLConnection class
	
	@param host: Hostname for your database
	@param username: Username to use to connect to database
	@param password: Password to use to connect to database 
	@param schema: Schema to use
	@param port: Port to connect on
	@param commitOnEnd: Default False, When query is complete do you wish to auto commit. This is a always on for this connection
	@author: Nick Verbeck
	@since: 5/12/2008
	@updated: 7/19/2008 - Added commitOnEnd support
	"""
	kargs = dict(kargs)
	if len(args) > 0:
		if len(args) >= 1:
			kargs['host'] = args[0]
		if len(args) >= 2:
			kargs['user'] = args[1]
		if len(args) >= 3:
			kargs['passwd'] = args[2]
		if len(args) >= 4:
			kargs['db'] = args[3]
		if len(args) >= 5:
			kargs['port'] = args[4]
		if len(args) >= 6:
			kargs['commitOnEnd'] = args[5]
	return connection.Connection(*args, **kargs)

#Query short cuts
def getNewQuery(connection = None, commitOnEnd=False, *args, **kargs):
	"""
	Create a new PySQLQuery Class
	
	@param PySQLConnectionObj: Connection Object representing your connection string
	@param commitOnEnd: Default False, When query is complete do you wish to auto commit. This is a one time auto commit
	@author: Nick Verbeck
	@since: 5/12/2008
	@updated: 7/19/2008 - Added commitOnEnd support
	"""
	if connection is None:
		return query.PySQLQuery(getNewConnection(*args, **kargs), commitOnEnd = commitOnEnd)
	else:
		#Updated 7/24/08 to include commitOnEnd here
		#-Chandler Prall
		return query.PySQLQuery(connection, commitOnEnd = commitOnEnd)


#Pool short cuts
def getNewPool():
	"""
	Create a new PySQLPool
	
	@author: Nick Verbeck
	@since: 5/12/2008
	"""
	return pool.Pool()

def terminatePool():
	"""
	Terminate all Connection
	
	@author: Nick Verbeck
	@since: 5/12/2008
	"""
	pool.Pool().Terminate()
	
def commitPool():
	"""
	Commits All changes in pool
	
	@author: Nick Verbeck
	@since: 9/12/2008
	"""
	pool.Pool().Commit()	
	
def cleanupPool():
	"""
	Cleanup connection pool. Closing all inactive connections.
	
	@author: Nick Verbeck
	@since: 9/12/2008
	"""
	pool.Pool().Cleanup()	