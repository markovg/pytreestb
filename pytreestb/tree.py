import numpy
import scipy.sparse
import pymatlab

class Tree(object):
        
    def __init__(self,**kwargs):
        fields = ['rnames', 'D', 'dA', 'R', 'Y', 'X', 'Z']
        d = kwargs

        # support Tree()
        if d=={}:
            for x in fields:
                d[x] = None

        # if any fields given, no field can be missing
        for x in fields:
            if x not in d:
                raise TypeError, "expected keys = %s, '%s' missing" % (str(fields), x)

        self.__dict__.update(d)

    def __repr__(self):
        return \
            "    dA: %s, %s\n" % (self.dA.shape, self.dA.dtype) + \
            "     R: %s, %s\n" % (self.R.shape, self.R.dtype) + \
            "     X: %s, %s\n" % (self.X.shape, self.X.dtype) + \
            "     Y: %s, %s\n" % (self.Y.shape, self.Y.dtype) + \
            "     Z: %s, %s\n" % (self.Z.shape, self.Z.dtype) + \
            "     D: %s, %s\n" % (self.D.shape, self.D.dtype) + \
            "rnames: %s" % self.rnames

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
                   

    def from_pierson_tract(self,pos, D=None):
        pos = numpy.array(pos)
        self.X = pos[:,0][None].T
        self.Y = pos[:,1][None].T
        self.Z = pos[:,2][None].T
        self.R = numpy.ones_like(self.X)
        if D==None:
            self.D = numpy.ones_like(self.X)
        else:
            D = numpy.array(D,dtype=float)
            if len(D.shape)==1:
                self.D = D[None].T
            else:
                self.D = D

        # check that all worked out well
        assert self.D.shape == self.X.shape

        self.rnames = ['axon']

        self.dA = scipy.sparse.lil_matrix((len(self.X),len(self.X)))
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



def matlab_tree_converter(matlab_struct):

    tree = Tree()

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

    try:
        tree.X = ms['X']
        tree.Y = ms['Y']
        tree.Z = ms['Z']
        tree.R = ms['R']
        tree.D = ms['D']
        tree.rnames = ms['rnames']
        dA = ms['dA']
    except KeyError as e:
        raise TypeError, "MATLAB struct expected key '%s' missing." % e.args[0]

    # TODO check shapes of X,Y,Z,R,D, dA

    if isinstance(dA,tuple) and len(dA)==4:
        tree.dA = scipy.sparse.csc_matrix(dA[:3],shape=dA[3])
    elif isinstance(dA,scipy.sparse.csc_matrix):
        tree.dA = dA
    else:
        raise TypeError, "adjacency matrix, dA, in unexpected format."

    return tree

    
