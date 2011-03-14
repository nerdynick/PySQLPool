'''
Created on Jun 12, 2010

@author: nick
'''
import unittest
import PySQLPool

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Logging)

class Logging(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def testLogging(self):
        pass
    
    def testQueryLogging(self):
        pass
    
if __name__ == "__main__":
    unittest.main(defaultTest='suite')