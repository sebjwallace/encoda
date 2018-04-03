from math import floor
from random import randint

class SDR:

    @staticmethod
    def Overlap(arr1,arr2):
        return [i for i in arr1 if i in arr2]

    @staticmethod
    def Union(arrs):
        return sum(arrs,[])

    @staticmethod
    def Subtract(arr1,arr2):
        return [i for i in arr1 if i not in arr2]

    @staticmethod
    def Difference(arr1,arr2):
        return [i for i in arr1 + arr2 if i not in SDR.Overlap(arr1,arr2)]

    @staticmethod
    def Subsample(arr,size = 8):
        indices = sorted(arr)
        out = []
        for i in range(size):
            out.append(indices[i * floor(len(indices) / size)])
        return out

    @staticmethod
    def BinaryToIndexArray(arr):
        indices = []
        for i, b in enumerate(arr):
            if (b == 1):
                indices.append(i)
        return indices

    @staticmethod
    def Chunk(binaryArray,size=3,offset=1,asBinary=False):
        chunks = []
        for i in range(0, len(binaryArray), offset):
            bin = binaryArray[i:i + size]
            if (asBinary):
                chunks.append(bin)
            else:
                indices = SDR.BinaryToIndexArray(bin)
                if (len(indices)):
                    chunks.append(indices)
        return chunks

    def __init__(self,range=2048,indices=None,binaryArray=None):
        self.indices = indices or []
        self.range = range
        if(binaryArray != None):
            self.fromBinaryArray(binaryArray)
        if(len(self.indices) == 0):
            self.random()

    def __call__(self,indices = None):
        if(indices != None):
            self.indices = indices
        return self.indices

    def random(self,size = 8):
        self.indices = []
        r = self.range / size
        for i in range(size):
            self.indices.append(int((r*i)+randint(0,r)))

    def union(self,arrs):
        return sum(arrs,self.indices)

    def overlap(self,arr):
        return SDR.Overlap(self.indices,arr)

    def subtract(self,arr):
        return SDR.Subtract(self.indices,arr)

    def difference(self,arr):
        return SDR.Difference(self.indices,arr)

    def subsample(self,size = 8):
        return SDR.Subsample(self.indices,size)

    def match(self,arrs):
        return self.sort(arrs)[-1]

    def sort(self,arrs):
        return sorted(arrs,key=lambda arr: self.overlap(arr))

    def chunk(self,size,offset,asBinary=False):
        return SDR.Chunk(binaryArray=self.toBinaryArray(),size=size,offset=offset,asBinary=asBinary)

    def density(self):
        return len(self.indices) / self.range

    def sparsity(self):
        return 1 - self.density()

    def fromIndexArray(self,arr):
        self.indices = arr

    def toIndexArray(self):
        return self.indices

    def toBinaryArray(self):
        arr = [0] * self.range
        for index in self.indices:
            arr[index] = 1
        return arr

    def fromBinaryArray(self,arr):
        self.indices = SDR.BinaryToIndexArray(arr)