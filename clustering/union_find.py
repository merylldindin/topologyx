# Author:  DINDIN Meryll
# Date:    26/06/2018
# Project: clustering

from clustering.imports import *

# Credits
# http://code.activestate.com/recipes/215912-union-find-data-structure/

# Implementation of the UnionFind algorithm

class UnionFind:
    
    # Initialization
    def __init__(self):

        self.num_weights = {}
        self.parent_pointers = {}
        self.num_to_objects = {}
        self.objects_to_num = {}
        
    # Insert objects among the already existing ones
    def insert_objects(self, objects):

        for object in objects: self.find(object)
            
    # Find a given object / build it if non-existing
    def find(self, object):

        if not object in self.objects_to_num:

            obj_num = len(self.objects_to_num)
            self.num_weights[obj_num] = 1
            self.objects_to_num[object] = obj_num
            self.num_to_objects[obj_num] = object
            self.parent_pointers[obj_num] = obj_num

            return object
        
        stk = [self.objects_to_num[object]]
        par = self.parent_pointers[stk[-1]]

        while par != stk[-1]:
            stk.append(par)
            par = self.parent_pointers[par]

        for i in stk: self.parent_pointers[i] = par
            
        return self.num_to_objects[par]
    
    # Link two different objects in a same distinct set
    def union(self, object1, object2):

        o1p = self.find(object1)
        o2p = self.find(object2)
        
        if o1p != o2p:
        	
            on1 = self.objects_to_num[o1p]
            on2 = self.objects_to_num[o2p]
            w1 = self.num_weights[on1]
            w2 = self.num_weights[on2]

            if w1 < w2: o1p, o2p, on1, on2, w1, w2 = o2p, o1p, on2, on1, w2, w1

            self.num_weights[on1] = w1+w2
            del self.num_weights[on2]
            self.parent_pointers[on2] = on1
