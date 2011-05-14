'''
Created on May 14, 2011

@author: nick
'''
import unittest
import PySQLPool
from mock import Mock

def suite():
    loader = unittest.TestLoader()
    alltests = unittest.TestSuite()
    alltests.addTest(loader.loadTestsFromTestCase(Pool))
        
    return alltests

class Pool:
    def setUp(self):
        pass
    
    def testPoolBorg(self):
        pass
    
    def testPoolGetConnection(self):
        pass
    
    def testPoolTerminate(self):
        pass
    
    def testPoolCleanup(self):
        pass
    
    def testPoolCommit(self):
        pass
    
    def testPoolConnectionCreation(self):
        pass
    
    def testPoolMultiThreadGetConnection(self):
        pass
    
    def testPoolMultiThreadGetConnectionWithTransactions(self):
        pass