import numpy
import scipy.sparse
import pymatlab

class Tree(object):
        
    def __init__(self,matlab_struct):

        ms = matlab_struct
        if isinstance(ms,pymatlab.Container):
            ms = ms.data

        if isinstance(ms,dict):
            #matlab struct list [{}] was unpacked already
            ms = ms
        elif len(ms)==1 and isinstance(ms[0],dict):
            # list with 1 dict element
            ms = ms[0]
        else:
            raise TypeError, "expected MATLAB struct of len==1"

        self.X = ms['X']
        self.Y = ms['Y']
        self.Z = ms['Z']
        self.R = ms['R']
        self.D = ms['D']
        self.rnames = ms['rnames']
        dA = ms['dA']
        if isinstance(dA,tuple) and len(dA)==4:
            self.dA = scipy.sparse.csc_matrix(dA[:3],shape=dA[3])
        elif isinstance(dA,scipy.sparse.csc_matrix):
            self.dA = dA
        else:
            raise TypeError, "adjacency matrix, dA, in unexpected format."

    def to_matlab(self):
        """ This function is used by pymatlab.FuncWrap
        if it exists to allow this class a chance to convert to something
        to send to MATLAB """

        # (data, indices, indptr)
        dA = (self.dA.data,self.dA.indices,self.dA.indptr,numpy.array(self.dA.shape,dtype=numpy.int32))
        struct = [{'X':self.X,'Y':self.Y,'Z':self.Z,
                   'R':self.R, 'D':self.D, 'rnames':self.rnames,
                   'dA':dA}]
        return struct
                   

    def from_pierson_tract(self,pos):
        pos = numpy.array(pos)
        self.X = pos[:,0][None].T
        self.Y = pos[:,1][None].T
        self.Z = pos[:,2][None].T
        self.R = numpy.ones_like(self.X)
        self.D = numpy.ones_like(self.X)
        self.D = numpy.array(self.D,dtype = float)
        self.dA = scipy.sparse.lil_matrix((len(self.X),len(self.X)))
        self.rnames = ['axon']
        for idx in range(len(self.X)-1):
            #self.dA[idx][idx+1] = 1
            self.dA[idx+1,idx] = 1
        # convert sparse matrix repr
        # to compressed sparse column format
        # as matlab likes
        self.dA = self.dA.tocsc()


    def __eq__(self,other):
        if not isinstance(other,Tree):
            return False
        
        for n in ['X','Y','Z','R','D']:
            if not numpy.allclose(self.__dict__[n],other.__dict__[n]):
                return False

        if not self.rnames==other.rnames:
            return False

        # check the sparse adjacency matrixces are equal
        # yeah, its a bit funny how to do this without
        # going to a dense matrix.
        return self.dA.todok().items()==other.dA.todok().items()
