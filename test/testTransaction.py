'''
Created on Jun 12, 2010

@author: nick
'''
import unittest
import PySQLPool

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Transaction)

class Transaction(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def testContext(self):
        pass
    
    def testSingleThread(self):
        pass
    
    def testMultiThread(self):
        pass
    
if __name__ == "__main__":
    unittest.main(defaultTest='suite')