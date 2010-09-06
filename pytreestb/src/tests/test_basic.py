import unittest
#import mocker

import pytreestb
import numpy
import scipy.sparse
from numpy import eye,arange,ones,array
from numpy.random import randn
from numpy.ma.testutils import assert_equal
#from scipy.io import savemat,loadmat
from os import remove

class TreesTBTestCase(unittest.TestCase):

    def setUp(self):
        self.session = pytreestb._session

    def test_edit_module(self):
        e = pytreestb.edit
        resample_tree = e.resample_tree


    def test_converters(self):
        s = self.session
        tree = pytreestb.sample_tree()
        assert isinstance(tree, pytreestb.Tree)

    def test_pierson_tract(self):
        s = self.session
        tree = pytreestb.Tree()

        # create a fake pierson tract
        pt = numpy.zeros((10,3))
        D =  3.0*numpy.ones(10)

        pt[:,0] = numpy.linspace(0,100,num=10)
        
        # both invocations should work
        # 1. comfy
        tree.from_pierson_tract(pt,D=D)
        assert pytreestb.IO.ver_tree(tree)

        # 2. native D shape invocation
        D =  D[None].T
        tree.from_pierson_tract(pt,D=D)

        assert isinstance(tree, pytreestb.Tree)
        assert pytreestb.IO.ver_tree(tree)



    def test_resample(self):
        s = pytreestb.sample_tree()
        #pytreestb.edit.resample_tree(s)

    def test_tree_to_matlab(self):
        s = self.session
        t1 = pytreestb.sample_tree()
        # put (to_matlab)
        s.s = t1
        # get (converter to Tree)
        t2 = s.s
        assert isinstance(t1, pytreestb.Tree)
        assert isinstance(t2, pytreestb.Tree)
        assert t1==t2

    def test_ver_tree(self):
        s = self.session
        t1 = pytreestb.sample_tree()
        assert isinstance(t1, pytreestb.Tree)
        assert pytreestb.IO.ver_tree(t1)
        t1.dA = scipy.sparse.csc_matrix((10,10))
        assert pytreestb.IO.ver_tree(t1)==False
        

        

def test_suite():

    suite = unittest.makeSuite(TreesTBTestCase,'test')
    return suite



if __name__ == "__main__":

    # unittest.main()
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite())
