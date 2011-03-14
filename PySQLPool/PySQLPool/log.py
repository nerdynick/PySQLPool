'''
Created on Jun 14, 2010

@author: nick
'''
from logging import Handler
import logging
import PySQLPool

class LogHandler(Handler):
    def __init__(self, level=PySQLPool.log_level):
        Handler.__init__(self, level)
        self.formatter = logging.Formatter("%(asctime)s - %(name)s:%(threadName)s - %(levelname)s - %(message)s")
        
    def flush(self):
        if PySQLPool.logger is not None:
            PySQLPool.logger.flush()
    
    def close(self):
        if PySQLPool.logger is not None:
            PySQLPool.logger.close()
    
    def emit(self, record):
        if PySQLPool.logger is not None:
            PySQLPool.logger.write(record)
            
logger = logging.getLogger('pysqlpool')
logger.setLevel(PySQLPool.log_level)
logger.addHandler(LogHandler())