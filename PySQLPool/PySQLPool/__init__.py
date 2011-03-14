__version__ = '0.3.7'
__author__ = 'Nick Verbeck <nick@skeletaldesign.com>'

import PySQLConnection

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
	return PySQLConnection.PySQLConnection(*args, **kargs)

import PySQLQuery
def getNewQuery(connection = None, commitOnEnd=False, *args, **kargs):
	"""
	Create a new PySQLQuery Class
	
	@param PySQLConnectionObj: PySQLConnection Object representing your connection string
	@param commitOnEnd: Default False, When query is complete do you wish to auto commit. This is a one time auto commit
	@author: Nick Verbeck
	@since: 5/12/2008
	@updated: 7/19/2008 - Added commitOnEnd support
	"""
	if connection is None:
		return PySQLQuery.PySQLQuery(getNewConnection(*args, **kargs), commitOnEnd = commitOnEnd)
	else:
		#Updated 7/24/08 to include commitOnEnd here
		#-Chandler Prall
		return PySQLQuery.PySQLQuery(connection, commitOnEnd = commitOnEnd)

import PySQLPool
def getNewPool():
	"""
	Create a new PySQLPool
	
	@author: Nick Verbeck
	@since: 5/12/2008
	"""
	return PySQLPool.PySQLPool()

def terminatePool():
	"""
	Terminate all Connection
	
	@author: Nick Verbeck
	@since: 5/12/2008
	"""
	PySQLPool.PySQLPool().Terminate()
	
def commitPool():
	"""
	Commits All changes in pool
	
	@author: Nick Verbeck
	@since: 9/12/2008
	"""
	PySQLPool.PySQLPool().Commit()	
	
def cleanupPool():
	"""
	Cleanup connection pool. Closing all inactive connections.
	
	@author: Nick Verbeck
	@since: 9/12/2008
	"""
	PySQLPool.PySQLPool().Cleanup()	