import unittest,doctest
from tests import test_basic

def test_suite():
    return unittest.TestSuite([
        test_basic.test_suite()
        #,doctest.DocFileSuite('../../README.txt'),
        ])
            
