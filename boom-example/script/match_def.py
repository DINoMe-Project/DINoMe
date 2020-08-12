import os
import sys
import collections
import re
import numpy
from IPython import embed
#nSets=8
#nWays=4
nMem=32
nEntry=32
import init_analyze
import bisect
class BaseModel:
    """ 
    """
    def __init__(self):
        self.other_symbols=collections.OrderedDict()
        self.secret_symbols=collections.OrderedDict()
        self.attack_symbols=collections.OrderedDict()
        self.observable_symbols=collections.OrderedDict()
        self.declass_symbols=collections.OrderedDict()

class ModelCacheSideChannelDemands(BaseModel):
    """ 
    """
    def __init__(self):
        BaseModel.__init__(self)
        # secret offset = operands in second instruction
        for i in range(0,32*4):
            if nWays>1:
                self.other_symbols["\\top.boom_tile.dcache.random_map_array_way[%d]"%(i)]=[(0,sys.maxint)]
            self.other_symbols["\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(i)]=[(0,sys.maxint)]

            self.other_symbols["\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(i)]=[(0,sys.maxint)]
        # demand
        self.secret_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[0]"]=[(52,8)]
        # base_address
        self.other_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[0]"]=[(20,8)]
        for i in range(16):
            self.other_symbols["\\top.boom_tile.dcache.MaxPeriodFibonacciLFSR.state_%d"%(i)]=[(0,1)]

        if not model_observe_counter:
            for i in range(0,nWays*nSets):
                self.other_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i)]=[(0,sys.maxint)]
            for i in range(0,nWays):
                for j in range(0,nSets):
                    self.observable_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i*nSets+j)]=[(0,sys.maxint)]
        for i in range(0,32):
            self.observable_symbols["final_cache_observe_%d"%(i)]=[(0,sys.maxint)]
        attack_random=collections.OrderedDict()
        for i in range(0,32):
            for way in range(0,nWays):
                if nWays>1:
                    attack_random["attack_\\top.boom_tile.dcache.random_map_array_way[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                attack_random["attack_\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                attack_random["attack_\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
        
        self.observable_symbols.update(attack_random)
        self.other_symbols.update(attack_random)
        for i in range(0,32):
            self.attack_symbols["cache_observe_%d"%(i)] = [(0,1)]

class ModelCacheDefenseRandom(BaseModel):
    """ 
    """
    def __init__(self):

        BaseModel.__init__(self)
        # secret offset = operands in second instruction
        for addr in range(0,32):
            for way in range(0,16):
                i=way*nMem+addr
                self.other_symbols["\\top.boom_tile.dcache.random_map_array_way[%d]"%(i)]=[(0,sys.maxint)]
                self.other_symbols["\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(i)]=[(0,sys.maxint)]
                self.other_symbols["\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(i)]=[(0,sys.maxint)]                
                if args.leak==1:
                    self.declass_symbols["\\top.boom_tile.dcache.random_map_array_way[%d]"%(i)]=[(0,sys.maxint)]
                    self.declass_symbols["\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(i)]=[(0,sys.maxint)]
                    self.declass_symbols["\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(i)]=[(0,sys.maxint)]
                    self.observable_symbols["\\top.boom_tile.dcache.random_map_array_way[%d]"%(i)]=[(0,sys.maxint)]
                    self.observable_symbols["\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(i)]=[(0,sys.maxint)]
                    self.observable_symbols["\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(i)]=[(0,sys.maxint)]
                
        self.secret_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[0]"]=[(52,8)]
        # size
        for i in range(16):
            self.other_symbols["\\top.boom_tile.dcache.MaxPeriodFibonacciLFSR.state_%d"%(i)]=[(0,1)]
        if not model_observe_counter:
            for i in range(0,nWays*nSets):
                self.other_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i)]=[(0,sys.maxint)]
            for i in range(0,nWays):
                for j in range(0,nSets):
                    self.observable_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i*nSets+j)]=[(0,sys.maxint)]
        for i in range(0,32):
            self.observable_symbols["final_cache_observe_%d"%(i)]=[(0,sys.maxint)]
        attack_random=collections.OrderedDict()
        for i in range(0,32):
            for way in range(0,nWays):
                if nWays>1:
                    attack_random["attack_\\top.boom_tile.dcache.random_map_array_way[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                attack_random["attack_\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                attack_random["attack_\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
        self.observable_symbols.update(attack_random)
        self.other_symbols.update(attack_random)
        self.declass_symbols.update(attack_random)
        for i in range(0,32):
            self.attack_symbols["cache_observe_%d"%(i)] = [(0,1)]


class ModelCacheSideChannelRandom(BaseModel):
    """ 
    """
    def __init__(self):
        BaseModel.__init__(self)
        # secret offset = operands in second instruction
        for addr in range(0,32):
            for way in range(0,16):
                i=way*nMem+addr
                self.other_symbols["\\top.boom_tile.dcache.random_map_array_way[%d]"%(i)]=[(0,sys.maxint)]
                self.other_symbols["\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(i)]=[(0,sys.maxint)]
                self.other_symbols["\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(i)]=[(0,sys.maxint)]                
                if args.leak==1:
                    self.declass_symbols["\\top.boom_tile.dcache.random_map_array_way[%d]"%(i)]=[(0,sys.maxint)]
                    self.declass_symbols["\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(i)]=[(0,sys.maxint)]
                    self.declass_symbols["\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(i)]=[(0,sys.maxint)]
                    self.observable_symbols["\\top.boom_tile.dcache.random_map_array_way[%d]"%(i)]=[(0,sys.maxint)]
                    self.observable_symbols["\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(i)]=[(0,sys.maxint)]
                    self.observable_symbols["\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(i)]=[(0,sys.maxint)]
                
        self.secret_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[0]"]=[(52,8)]
        # size
        for i in range(16):
            self.other_symbols["\\top.boom_tile.dcache.MaxPeriodFibonacciLFSR.state_%d"%(i)]=[(0,1)]
        for i in range(32):
            self.other_symbols["cache_observe_way_%d"%(i)]=[(0,sys.maxint)]
        if not model_observe_counter:
            for i in range(0,nWays*nSets):
                self.other_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i)]=[(0,sys.maxint)]
            for i in range(0,nWays):
                for j in range(0,nSets):
                    self.observable_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i*nSets+j)]=[(0,sys.maxint)]
        for i in range(0,32):
            self.observable_symbols["final_cache_observe_%d"%(i)]=[(0,sys.maxint)]
        attack_random=collections.OrderedDict()
        for i in range(0,32):
            for way in range(0,nWays):
                if nWays>1:
                    attack_random["attack_\\top.boom_tile.dcache.random_map_array_way[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                attack_random["attack_\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                attack_random["attack_\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
        self.observable_symbols.update(attack_random)
        self.other_symbols.update(attack_random)
        self.declass_symbols.update(attack_random)
        for i in range(0,32):
            self.attack_symbols["cache_observe_%d"%(i)] = [(0,1)]


class Model3PrimeProbeRandom(BaseModel):
    """ offset is 3-bit size
    2^3 * 3 bit secret memory
    """
    def __init__(self):
        BaseModel.__init__(self)
        self.__bits=3
        self.setAttack()
        self.setSecret()
        self.setObserve()
        self.setOther()
    def setAttack(self):
        self.attack_symbols={}
        for i in range(0,4):
            self.attack_symbols["\\top.boom_tile.frontend.bpdpipeline.bpd.counter_table.counter_table_ext.mem_0_0.ram[%d]"%(i)]=[(0,8)]
        self.attack_symbols["\\mem.srams.mem.mem_ext.mem_0_0.ram[64]"]=[(9-self.__bits,self.__bits),(0,9-self.__bits,0)]
        for i in range(0,nWays):
            self.attack_symbols["\\top.boom_tile.dcache.meta_0.tag_array_%d[%d]"%(i,0)]=[(0,sys.maxint)]
 

    def setSecret(self):
        for i in range(192,256):
            if i%8 == 0:
                self.secret_symbols["\\mem.srams.mem.mem_ext.mem_0_0.ram[%d]"%(i)]=[(0,3)]

    def setOther(self):
        self.other_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[3]"]=[(29-self.__bits,self.__bits),(20,9-self.__bits,0),(29,3,0)]
        # size
        self.other_symbols["\\mem.srams.mem.mem_ext.mem_0_0.ram[98]"]=[(9-self.__bits,self.__bits),(0,9-self.__bits,0)]

        for i in range(0,32):
            if nWays:
                self.other_symbols["\\top.boom_tile.dcache.random_map_array_way[%d]"%(i)]=[(0,sys.maxint)]
            self.other_symbols["\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(i)]=[(0,sys.maxint)]
            self.other_symbols["\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(i)]=[(0,sys.maxint)]
        for i in range(16):
            self.other_symbols["\\top.boom_tile.dcache.MaxPeriodFibonacciLFSR.state_%d"%(i)]=[(0,1)]
    def setObserve(self):
        for j in range(0, 1):
            for i in range(0,nWays):
                self.observable_symbols["\\top.boom_tile.dcache.meta_0.tag_array_%d[%d]"%(i,j)]=[(0,sys.maxint)]

class ModelSpectreTargetMemDelay(BaseModel):
    """ offset is 3-bit size
    2^3 * 3 bit secret memory
    """
    def __init__(self):

        BaseModel.__init__(self)
        # secret offset = operands in second instruction
        """
        for i in range(0,32*4):
            
            if nWays>1:
                self.other_symbols["\\top.boom_tile.dcache.random_map_array_way[%d]"%(i)]=[(0,sys.maxint)]
            self.other_symbols["\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(i)]=[(0,sys.maxint)]
#offset
            self.other_symbols["\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(i)]=[(0,sys.maxint)]
        """
        self.attack_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[0]"]=[(20,8)]
        self.secret_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[3]"]=[(20,8)]
        # size
        self.other_symbols["\\mem.srams.mem.mem_ext.mem_0_0.ram[192]"]=[(0,8)]
        for i in range(16):
            self.other_symbols["\\top.boom_tile.dcache.MaxPeriodFibonacciLFSR.state_%d"%(i)]=[(0,1)]
        if not model_observe_counter:
            for i in range(0,nWays*nSets):
                self.other_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i)]=[(0,sys.maxint)]
            for i in range(0,nWays):
                for j in range(0,nSets):
                    self.observable_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i*nSets+j)]=[(0,sys.maxint)]
        for i in range(0,32):
            self.observable_symbols["final_cache_observe_%d"%(i)]=[(0,sys.maxint)]
        for i in range(0,32):
            for way in range(0,nWays):
                if nWays>1:
                    self.observable_symbols["attack_\\top.boom_tile.dcache.random_map_array_way[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                self.observable_symbols["attack_\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]

                self.observable_symbols["attack_\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
        for i in range(0,4):
            self.attack_symbols["\\top.boom_tile.frontend.bpdpipeline.bpd.counter_table.counter_table_ext.mem_0_0.ram[%d]"%(i)]=[(0,8)]
        for i in range(0,32):
            self.attack_symbols["cache_observe_%d"%(i)] = [(0,1)]


class ModelSpectreMemDelay(BaseModel):
    """ offset is 3-bit size
    2^3 * 3 bit secret memory
    """
    def __init__(self):
        BaseModel.__init__(self)
        # secret offset = operands in second instruction
        for i in range(0,32*4):
            if nWays>1:
                self.other_symbols["\\top.boom_tile.dcache.random_map_array_way[%d]"%(i)]=[(0,sys.maxint)]
            self.other_symbols["\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(i)]=[(0,sys.maxint)]
#offset
            self.other_symbols["\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(i)]=[(0,sys.maxint)]
        self.attack_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[0]"]=[(20,8)]
        for i in range(16,17):
            self.secret_symbols["\\mem.srams.mem.mem_ext.mem_0_0.ram[%d]"%(i)]=[(0,8)]
        # size
        self.other_symbols["\\mem.srams.mem.mem_ext.mem_0_0.ram[192]"]=[(0,8)]
        for i in range(16):
            self.other_symbols["\\top.boom_tile.dcache.MaxPeriodFibonacciLFSR.state_%d"%(i)]=[(0,1)]
        if not model_observe_counter:
            for i in range(0,nWays*nSets):
                self.other_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i)]=[(0,sys.maxint)]
            for i in range(0,nWays):
                for j in range(0,nSets):
                    self.observable_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i*nSets+j)]=[(0,sys.maxint)]
        for i in range(0,32):
            self.observable_symbols["final_cache_observe_%d"%(i)]=[(0,sys.maxint)]
        for i in range(0,32):
            for way in range(0,nWays):
                if nWays>1:
                    self.observable_symbols["attack_\\top.boom_tile.dcache.random_map_array_way[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                self.observable_symbols["attack_\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]

                self.observable_symbols["attack_\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
        for i in range(0,4):
            self.attack_symbols["\\top.boom_tile.frontend.bpdpipeline.bpd.counter_table.counter_table_ext.mem_0_0.ram[%d]"%(i)]=[(0,8)]
        for i in range(0,32):
            self.attack_symbols["cache_observe_%d"%(i)] = [(0,1)]

class ModelSpectreTarget(BaseModel):
    """ offset is 3-bit size
    2^3 * 3 bit secret memory
    """
    def __init__(self):
        BaseModel.__init__(self)
        # secret offset = operands in second instruction
        for i in range(0,32*4):
            if nWays>1:
                self.other_symbols["\\top.boom_tile.dcache.random_map_array_way[%d]"%(i)]=[(0,sys.maxint)]
            self.other_symbols["\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(i)]=[(0,sys.maxint)]

            self.other_symbols["\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(i)]=[(0,sys.maxint)]
        #size
        self.other_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[0]"]=[(20,8)]
        #offset
        self.attack_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[0]"]=[(52,8),(60,4,0)]
        #secret val at offset
        self.secret_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[1]"]=[(20,8)]
        for i in range(16):
            self.other_symbols["\\top.boom_tile.dcache.MaxPeriodFibonacciLFSR.state_%d"%(i)]=[(0,1)]
        if not model_observe_counter:
            for i in range(0,nWays*nSets):
                self.other_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i)]=[(0,sys.maxint)]
            for i in range(0,nWays):
                for j in range(0,nSets):
                    self.observable_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i*nSets+j)]=[(0,sys.maxint)]
        for i in range(0,32):
            self.observable_symbols["final_cache_observe_%d"%(i)]=[(0,sys.maxint)]
        self.observable_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[0]"]=[(20,8)]
        for i in range(0,32):
            for way in range(0,nWays):
                if nWays>1:
                    self.observable_symbols["attack_\\top.boom_tile.dcache.random_map_array_way[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                self.observable_symbols["attack_\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                self.observable_symbols["attack_\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
        for i in range(0,4):
            self.attack_symbols["\\top.boom_tile.frontend.bpdpipeline.bpd.counter_table.counter_table_ext.mem_0_0.ram[%d]"%(i)]=[(0,8)]
        for i in range(0,32):
            self.attack_symbols["cache_observe_%d"%(i)] = [(0,1)]

class ModelSpectreRandom(BaseModel):
    """ offset is 3-bit size
    2^3 * 3 bit secret memory
    """
    def __init__(self):
        BaseModel.__init__(self)
        # secret offset = operands in second instruction
        for i in range(0,32*4):
            if nWays>1:
                self.other_symbols["\\top.boom_tile.dcache.random_map_array_way[%d]"%(i)]=[(0,sys.maxint)]
            self.other_symbols["\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(i)]=[(0,sys.maxint)]

            self.other_symbols["\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(i)]=[(0,sys.maxint)]
        #size
        self.other_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[0]"]=[(20,8)]
        self.attack_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[0]"]=[(52,8),(60,4,0)]
        for i in range(16,17):
            self.secret_symbols["\\mem.srams.mem.mem_ext.mem_0_0.ram[%d]"%(i)]=[(0,8)]
        for i in range(16):
            self.other_symbols["\\top.boom_tile.dcache.MaxPeriodFibonacciLFSR.state_%d"%(i)]=[(0,1)]
        if not model_observe_counter:
            for i in range(0,nWays*nSets):
                self.other_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i)]=[(0,sys.maxint)]
            for i in range(0,nWays):
                for j in range(0,nSets):
                    self.observable_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i*nSets+j)]=[(0,sys.maxint)]
        for i in range(0,32):
            self.observable_symbols["final_cache_observe_%d"%(i)]=[(0,sys.maxint)]
        for i in range(0,32):
            for way in range(0,nWays):
                if nWays>1:
                    self.observable_symbols["attack_\\top.boom_tile.dcache.random_map_array_way[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                self.observable_symbols["attack_\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                self.observable_symbols["attack_\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
        for i in range(0,4):
            self.attack_symbols["\\top.boom_tile.frontend.bpdpipeline.bpd.counter_table.counter_table_ext.mem_0_0.ram[%d]"%(i)]=[(0,8)]
        for i in range(0,32):
            self.attack_symbols["cache_observe_%d"%(i)] = [(0,1)]

class ModelCacheModExpRandom(BaseModel):
    """ offset is 3-bit size
    2^3 * 3 bit secret memory
    """
    def __init__(self):
        BaseModel.__init__(self)
        # secret offset = operands in second instruction
        for i in range(0,32*4):
            if nWays>1:
                self.other_symbols["\\top.boom_tile.dcache.random_map_array_way[%d]"%(i)]=[(0,sys.maxint)]
            self.other_symbols["\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(i)]=[(0,sys.maxint)]

            self.other_symbols["\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(i)]=[(0,sys.maxint)]
        self.secret_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[2]"]=[(52,8)]
        # size
        for i in range(16):
            self.other_symbols["\\top.boom_tile.dcache.MaxPeriodFibonacciLFSR.state_%d"%(i)]=[(0,1)]
        if not model_observe_counter:
            for i in range(0,nWays*nSets):
                self.other_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i)]=[(0,sys.maxint)]
            for i in range(0,nWays):
                for j in range(0,nSets):
                    self.observable_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i*nSets+j)]=[(0,sys.maxint)]
        for i in range(0,32):
            self.observable_symbols["final_cache_observe_%d"%(i)]=[(0,sys.maxint)]
        for i in range(0,32):
            for way in range(0,nWays):
                if nWays>1:
                    self.observable_symbols["attack_\\top.boom_tile.dcache.random_map_array_way[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                self.observable_symbols["attack_\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]

                self.observable_symbols["attack_\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
        for i in range(0,4):
            self.attack_symbols["\\top.boom_tile.frontend.bpdpipeline.bpd.counter_table.counter_table_ext.mem_0_0.ram[%d]"%(i)]=[(0,8)]
        for i in range(0,32):
            self.attack_symbols["cache_observe_%d"%(i)] = [(0,1)]



def formatSymLine(line):
    if line.startswith('c') and '->' in line:
        i=line.rfind('[')
        j=line.rfind(']')
        vs=line[i+1:j].split()
        w=line.split()
        name=w[1]
        print(vs)
        return (name,[int(v) for v in vs])
    return None
def display_sol(solfile,cnffile):
    f=open(solfile)
    cnff=open(cnffile)
    outname=solfile+".out"
    outf=open(outname,'w+')
    sym_to_vars={}
    assign={}
    for line in cnff:
        s=formatSymLine(line)
        if s==None:
            continue
        sym_to_vars[s[0]]=s[1]
    for line in f:
        w= line.split()
        #print w[0:-1]
        assign={}
        for v in w[0:-1]:
            assign[int(v)]=1 if v>0 else 0
            assign[-int(v)]=0 if v>0 else 1
        for name in sym_to_vars: 
            val=[]
            for v in sym_to_vars[name]:
                if v not in assign:
                    val.append("x")
                else:
                    val.append(str(assign[v]))
            #print name,val
            outf.write("%s --> [%s]\n"%(name,"".join(val)))
        outf.write("\n")
    outf.close() 
    cnff.close()
    f.close()

class MatchSym(BaseModel):
    def __init__(self,nstate,model,args):
        self.__dict__.update(vars(model))
        self.args=args
        self.assign={}
        self.required_val={}
        if args.stateindex>=0:
            self._init_state= "s%d"%(args.stateindex)
        else:
            self._init_state=None
        self._last_state= "s%d"%(args.nstate-1)
        self._template=re.compile("\(define-fun \|(?P<tmp>[a-zA-Z0-9#_]*)\| "
            "\(\(state \|TestHarness_s\|\)\) \(_ BitVec (?P<size>[0-9]*)\) "
            "\(\(_ extract (?P<end>[0-9]*) (?P<start>[0-9]*)\) state\)\)[ ]*[;]*"
            "[ ]*(?P<symbol>[a-zA-Z0-9_\.\[\]\#\$\\\\]*)")
        self._booltemplate=re.compile("\(define-fun \|(?P<tmp>[a-zA-Z0-9#_]*)\| "
            "\(\(state \|TestHarness_s\|\)\) Bool \(= "
            "\(\(_ extract (?P<end>[0-9]*) (?P<start>[0-9]*)\) state\) #b1\)\)[ ]*[;]*"
            "[ ]*(?P<symbol>[a-zA-Z0-9_\.\[\]\$\#\\\\]*)")
        self.special_symbols={}
        self._nstate=nstate
        self._reserve_symbol=args.reserve_symbol
        self.template_name=['tmp','size','start','end','symbol']
        def key(s):
            if isinstance(s,dict):
                return s.keys()
            return s;
        self._symbols=key(self.secret_symbols)+key(self.attack_symbols)+key(self.observable_symbols)+key(self.other_symbols)+key(self.declass_symbols)
        self._address_map={}
        self.ind_vars=[]
        self.jac_vars=[]
        self._var_to_symbol={}
        self._symbol_to_vars={}
        self.header=[]
        for s in self._symbols:
            self._address_map[s]=[]
    test="""(define-fun |TestHarness#5767| ((state |TestHarness_s|)) (_ BitVec 88) ((_ extract 166427 166340) state)) ; \dut.tile.dcache.meta.tag_array.tag_array_ext.ram[9]
    (define-fun |TestHarness_n dut.tile.dcache.meta.tag_array.tag_array_ext.ram[9]| ((state |TestHarness_s|)) (_ BitVec 88) (|TestHarness#5767| state))"""
    def Search(self,line):
        self.smt2names={}
        match=self._template.match(line)
        if not match:
            match=self._booltemplate.match(line)
        if match:
            match_d=match.groupdict()
            symbol=match_d['symbol']
            #:print(symbol)
            #if symbol in self._symbols:
            start=int(match_d['start'])
            end =int(match_d['end'])
            if 'size' in match_d:
                size =int(match_d['size'])
            else:
                size=1
            if end-start+1!=size:
                raise Exception("wrong size.")
                #for i in range(start,end+1):
            self._address_map[symbol]=range(start,end+1)
            self._var_to_symbol[start]=(end+1,symbol,match_d['tmp'] )
            #self.smt2names[symbol]=
    def dumpVariableSMT(self):
        nextstart=0
        Vars=[]
        lines=[]
        for start in sorted(self._var_to_symbol):
            if start!=nextstart:
                print("missing %d-%d"%(nextstart,start)) 
                Vars.append("(_ bv0 %d)"%(start-nextstart))
            end,name,smt2name = self._var_to_symbol[start]
            Vars.append("(|%s| s0)"%(smt2name))
            nextstart=end
        concatedVars=" \n".join(Vars)
        lines.append("(define-fun s1 () |TestHarness_s| (concat %s));"%concatedVars)
        with open("transition.smt2","w") as f:
            f.write("\n".join(lines))


    def Check(self):
        for s in self._symbols:
            if(len(self._address_map[s])==0):
                raise Exception("not found")
        return True

    def ComposeSelectedVar(self,state_vars,symbols):
        result=[]
        for s in symbols:
            selects = symbols[s];
            for select in selects:
                print(selects)
                offset=select[0]
                size=select[1]
                if not s in self._address_map:
                    continue
                symbol_len=len(self._address_map[s])
                if offset>= symbol_len:
                    continue
                size= min(size,symbol_len-offset)
                val=-1
                if len(select)>2:
                    val = select[2]
                if val>-1:
                    for var in self._address_map[s][offset:offset+size]:
                        self.required_val[var]=val
                    continue
                #print(s,offset,len(state_vars))
                self._symbol_to_vars[s]=[state_vars[i] for i in self._address_map[s]]
                result.extend(self._symbol_to_vars[s][offset:offset+size])
        return result
    def ComposeVarFromSpecial(self,symbols):
        result=[]
        for name in symbols:
            if name in self.special_symbols:
                selects = symbols[name];
                for select in selects:
                    if len(select)>2:
                        continue
                    offset=select[0]
                    size=select[1]
                    result.extend(self.special_symbols[name][offset:offset+size])
        return result

    def ComposeVar(self,state_vars,symbols):
        if isinstance(symbols,dict):
            return self.ComposeSelectedVar(state_vars,symbols)
        result=set()
        for s in symbols:
            self._symbol_to_vars[s]=[state_vars[i] for i in self._address_map[s]]
            select=symbols[s]
            offset=select[0]
            size=select[1]
            result.update(self._symbol_to_vars[s][offset:offset+size])
        return (result)

    def ComposeSelectedSmt2Var(self,state_var,symbols):
        result=[]
        for s in symbols:
            selects = symbols[s];
            for offset,size in selects:
                result.extend(["((_ extract %d %d) %s)"%(i,i,state_var) for i in self._address_map[s][offset:offset+size]])
        return result

    def ComposeSmt2Var(self,state_var,symbols):
        if isinstance(symbols,dict):
            return self.ComposeSelectedSmt2Var(state_var,symbols)
        result=[]
        for s in symbols:
            for i in self._address_map[s]:
                result.append("((_ extract %d %d) %s)"%(i,i,state_var))
        return (result)
    def ComposeConstantVar(self,state_vars,symbol_vars):
        print("finish constant")
        i=0;
        constant_vars=set()
        constant_index={}
        for var in state_vars:
            if var not in symbol_vars:
                constant_vars.add(var)
                constant_index[var]=i
            i=i+1
        print("finish constant")
        return (constant_vars, constant_index)

    def _random_hash(self,all_vars,log2_size):
        var_size=len(all_vars)
        all_vars=numpy.array(all_vars)
        result=[]
        for _ in range(0,var_size-log2_size):
            selected=numpy.random.randint(2,size=var_size)
            selected_vars=all_vars[selected==1]
            r=numpy.random.randint(2,size=1)[0]
            result.append("(assert (= #b%d (bvxor %s)))"%(r,' '.join(selected_vars)))
        return result
    def MarkSMT2(self,out_smt2file,jac_log2_size=1):
        jac_vars=[]
        other_vars=[]
        attack_vars=[]
        ob_vars=[]
        jac_vars.extend(self.ComposeSmt2Var(self._init_state,self.secret_symbols))
        other_vars.extend(self.ComposeSmt2Var(self._init_state,self.other_symbols))
        attack_vars.extend(self.ComposeSmt2Var(self._init_state,self.attack_symbols))
        ob_vars.extend(self.ComposeSmt2Var('s%d'%(self._nstate-1),self.observable_symbols))

        declass_vars.extend(self.ComposeSmt2Var('s%d'%(self._nstate-1),self.declass_symbols))
        with open(out_smt2file,'w') as f:
            f.write('\n'.join(self._random_hash(jac_vars,jac_log2_size)));


    def MarkCNFHelper(self,cnffile):
        jac_vars=[]
        other_vars=[]
        attack_vars=[]
        ob_vars=[]
        declass_vars=[]
        constant=[]
        count=0
        comments=[]
        header=[]
        print("start mark cnf\n")
        with open(cnffile) as f:
            for line in f:
                count=count+1
                if line.startswith("c") or line.startswith("p"):
                    header.append(line)
                if line.startswith('c') and '->' in line:
                    i=line.rfind('[')
                    j=line.rfind(']')
                    vs=line[i+1:j].split()
                    w=line.split()
                    name=w[1]
                    self.special_symbols[name] = vs
                    print(name,len(self.special_symbols[name]))
                    if self._reserve_symbol or len(line)<1000:
                        comments.append(line);
                        #comments.append('c ind '+" ".join(vs)+' 0\n');
                if  line.startswith('c'):
                    print(line[:10])
                    line = line.replace("]","")
                    w=line.split("[")
                    if len(w)<2:
                        continue
                    name=w[0].split()[1]
                    m=re.match("s([0-9]+)",name)
                    if not m:
                        continue
                    if int(m.groups()[0])==self.args.stateindex:
                        state=w[1].replace("]","").split()
                        self.init_state_vars=state;
                        jac_vars.extend(self.ComposeVar(state,self.secret_symbols))
                        other_vars.extend(self.ComposeVar(state,self.other_symbols))
                        print(self.attack_symbols)
                        attack_vars.extend(self.ComposeVar(state,self.attack_symbols))
                        constant,const_index=self.ComposeConstantVar(state,jac_vars+other_vars+attack_vars);
                    print(m.groups())
                    if int(m.groups()[0])==self._nstate-1:
                        state=w[1].replace("]","").split()
                        self.last_state_vars=state
                        ob_vars.extend(self.ComposeVar(state,self.observable_symbols))

                        declass_vars.extend(self.ComposeVar(state,self.declass_symbols))
                        print("end state")
        jac_vars.extend(self.ComposeVarFromSpecial(self.secret_symbols))
        other_vars.extend(self.ComposeVarFromSpecial(self.other_symbols))
        attack_vars.extend(self.ComposeVarFromSpecial(self.attack_symbols))
        initial_ob_vars=[]
        initial_ob_vars.extend(self.ComposeVarFromSpecial(self.observable_symbols))
        declass_vars.extend(self.ComposeVarFromSpecial(self.declass_symbols))
        self.jac_vars=jac_vars
        self.other_vars=other_vars
        self.ob_vars=ob_vars
        self.declass_vars=declass_vars
        self.initial_ob_vars=initial_ob_vars
        self.attack_vars =attack_vars
        self.reserved_vars=set([abs(int(v)) for v in jac_vars+other_vars+ob_vars+attack_vars])
        self.comments=comments
        self.header=header
    def MarkCNF(self,cnffile):
        other_names=",".join(self.other_symbols.keys())
        other_vars_str=' '.join(self.other_vars)
        print(other_names)
        with open(cnffile+'.head','w+') as f:
            f.write("c secret --> [%s]\n"%' '.join(self.jac_vars))
            f.write("c other --> [%s]\n c %s\n"%(other_vars_str,other_names))
            f.write("c control --> [%s]\n"%' '.join(self.attack_vars))
            f.write("c observe --> [%s]\n"%' '.join(self.ob_vars))
            f.write("c initial_observe --> [%s]\n"%' '.join(self.initial_ob_vars))

            f.write("c declass --> [%s]\n"%' '.join(self.declass_vars))
            for s in self.observable_symbols:
                if s in self._symbol_to_vars:
                    vars=self._symbol_to_vars[s]
                    f.write("c ob_%s --> [%s]\n"%(s," ".join(vars)))
            f.write(''.join(self.comments))
        oldcnf=open(cnffile)
        with open(cnffile+'.observe.cnf','w+') as f:
            f.write("c secret --> [%s]\n"%' '.join(self.jac_vars))
            f.write("c other --> [%s]\n c %s\n"%(other_vars_str,other_names))
            f.write("c control --> [%s]\n"%' '.join(self.attack_vars))
            f.write("c observe --> [%s]\n"%' '.join(self.ob_vars))
            f.write("c initial_observe --> [%s]\n"%' '.join(self.initial_ob_vars))
            f.write("c declass --> [%s]\n"%' '.join(self.declass_vars))
            for s in self.observable_symbols:
                if s in self._symbol_to_vars:
                    vars=self._symbol_to_vars[s]
                    f.write("c ob_%s --> [%s]\n"%(s," ".join(vars)))
            for line in oldcnf:
                if line.startswith("c") and self._last_state in line:
                    continue
                f.write(line)
        oldcnf.close()
        oldcnf=open(cnffile)
        with open(cnffile+'.symbol.cnf','w+') as f:
            f.write("c secret --> [%s]\n"%' '.join(self.jac_vars))
            f.write("c other --> [%s]\nc %s\n"%(' '.join(self.other_vars),other_names))
            f.write("c control --> [%s]\n"%' '.join(self.attack_vars))
            f.write("c observe --> [%s]\n"%' '.join(self.ob_vars))
            f.write("c initial_observe --> [%s]\n"%' '.join(self.initial_ob_vars))
            f.write("c declass --> [%s]\n"%' '.join(self.declass_vars))
            for line in oldcnf:
                if line.startswith("c"):
                    continue
                f.write(line)
        oldcnf.close()

    def auto_init(self,var):
        cl=""
        if var in self.required_val or str(-int(var)) in self.required_val:
            print("is a required val", var,self.required_val[var])
            #if(len(var)==0): return ""
            if self.required_val[var]>0:
                lit=int(var)
            else:
                lit=-int(var)
            cl='%d 0'%lit;
        else:
            lit=-int(var)
            cl='%d 0'%lit;
        return cl
    def AnalyzeInit(self,filename,use_init_state):
        symbolic_vars=[]
        all_uninited_ranges,sym_vars,assign=init_analyze.process(filename)
        self.assign=assign.copy()
        if use_init_state:
            state_vars=self.init_state_vars
            state_name=self._init_state
        else:
            state_vars=self.last_state_vars
            state_name=self._last_state
        uninited_ranges=all_uninited_ranges[state_name]
        offset_to_var=sym_vars[state_name]
        lines=[]
        symbol_starts=sorted(self._var_to_symbol.keys())
        skipped=0
        for var in self.reserved_vars:
            if abs(int(var)) in assign:
                print("init sym var %d"%var) 
        for strvar in state_vars:
            lit= int(strvar)
            if abs(lit) in self.reserved_vars:
                skipped=skipped+1
                if lit in assign:
                    del assign[abs(lit)]
                continue
            if  abs(lit) in assign:
                continue
            if self.args.autoinit:
                assign[abs(lit)]=True if lit>0 else False
                lines.append(self.auto_init(str(lit)))
        print("skipped=%d"%skipped)
        if self.args.autoinit:
            print("auto init uninited to zero")
            import shutil
            initfile=filename+".autoinit"
            #shutil.copy(filename,initfile)
            with open(initfile,'w+') as f:
                for name in self._symbol_to_vars:
                    if name in self.secret_symbols or name in self.other_symbols or name in self.attack_symbols:
                        f.write("c %s --> [%s]\n"%(name," ".join(self._symbol_to_vars[name])))
                f.write("".join(self.header))
                for var in self.assign:
                    if var in self.reserved_vars:
                        print(var)
                        continue
                    s="-" if self.assign[var] else ""
                    f.write("%s%d 0\n"%(s,var))
                f.write('\nc c automatically init;\n')
                f.write('\n'.join(lines))
        #self.assign= assign

    def dump(self,names, use_special=False,need_sol=False):
        self.args.autoinit=False
        if need_sol:
            self.AnalyzeInit(self.args.cnffile)
        bonusf= open(self.args.cnffile+".init","a+")
        for var in self.required_val:
            bonusf.write(self.auto_init(var)+"\n")
        with open(self.args.cnffile+".dump",'a+') as f:
            for name in names:
                if use_special:
                    if name not in self.special_symbols:
                        continue
                    vars=self.special_symbols[name]
                else:
                    if name not in self._address_map:
                        continue
                    try:
                        vars=self.last_state_vars[self._address_map[name][0]: self._address_map[name][-1]+1]
                    except:
                        print ("except",name,self._address_map[name], self._address_map[name])
                        
                        continue

                if name in self.secret_symbols or name in self.other_symbols or name in self.attack_symbols:
                    for strvar in vars:
                        var=abs(int(strvar))
                        if var not in self.reserved_vars:
                            bonusf.write(self.auto_init(strvar)+"\n")
                concrete=True
                val=""
                for strvar in vars:
                    var=abs(int(strvar))
                    if var not in self.assign:
                        val="x"+val
                        concrete=False;
                        continue
                    isneg=self.assign[var]
                    if isneg:
                        val = "0"+val
                    else:
                        val = "1"+val
                if concrete:
                    try:
                        val= str(hex(int(val,2)))
                    except:
                        print("invalid %s var=%s val=%s"%(name," ".join(vars),val))
                if not name in self._address_map:
                    print("err",name)
                    embed()
                f.write("c %s: %d %d %s = %s\n"%(name, self._address_map[name][0], self._address_map[name][-1], " ".join(vars),val) )
                f.write("c %s --> [ %s ]\n"%(name,  " ".join(vars)) )
        bonusf.close()
def main(args,model):
    if args.mode=='display':
        display_sol(args.solfile,args.cnffile)
    if args.mode=='victim':
        f=open("victim.cfg","w+")
        symbols={"secret":model.secret_symbols,"control": model.attack_symbols,"observe":model.observable_symbols, "other":model.other_symbols}
        for label in symbols:
            for name in symbols[label]:
                for spec in symbols[label][name]:
                    f.write("%s %s %d %d\n"%(label, name,spec[0],spec[1]))
        f.close()
        return
    ms=MatchSym(args.nstate,model,args)
    with open (args.file) as f:
        for line in f:
            ms.Search(line.replace("\n",""))

    if args.mode=="dump_trans":
        ms.dumpVariableSMT()
        return
    ms.MarkCNFHelper(args.cnffile)
    if args.cnffile:
        if args.mode=='mark':
            ms.MarkCNF(args.cnffile)
        if args.mode == 'init':
            ms.AnalyzeInit(args.cnffile,True)
        if args.mode == "dumpmap":
            ms.AnalyzeInit(args.cnffile,False)
            ms.dump(ms._address_map)
        if args.mode == "dumpsym":
            ms.AnalyzeInit(args.cnffile,False)
            ms.dump(secret_symbols,True)
            ms.dump(attack_symbols,True)
            ms.dump(other_symbols,True)
            ms.dump(observable_symbols)
    if args.smt2file:
        if args.mode =='mark':
            ms.MarkSMT2(args.smt2file,2)


class Model1:
    """ offset is 1-bit size
    2 * 3 bit secret memory
    """
    def __init__(self):
        self.other_symbols=collections.OrderedDict()
        self.secret_symbols=collections.OrderedDict()
        self.attack_symbols=collections.OrderedDict()
        self.observable_symbols=collections.OrderedDict()
        # secret offset 12 bit =6 +1 +5
        self.other_symbols["\\dut.tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.ram[3]"]=[(28,1),(20,8,0),(29,6,0)]
        # bound size , 16 bit= 6+1+9
        self.other_symbols["\\mem.sram.mem.mem_ext.ram[98]"]=[(0,6,0), (6,1),(7,9,0)]
        for i in range(192,256):
            if i%32 == 0:
                self.secret_symbols["\\mem.sram.mem.mem_ext.ram[%d]"%(i)]=[(0,3)]
            else:
                self.secret_symbols["\\mem.sram.mem.mem_ext.ram[%d]"%(i)]=[(0,0)]
        for i in range(0,4):
            self.attack_symbols["\\dut.tile.frontend.bpdpipeline.bpd.counter_table.counter_table_ext.ram[%d]"%(i)]=[(0,8)]
        #16 bit= 6+1+9
        self.attack_symbols["\\mem.sram.mem.mem_ext.ram[64]"]=[(0,6,0),(6,1),(7,9,0)]
        for i in range(0,8):
            self.observable_symbols["\\dut.tile.dcache.meta.tag_array.tag_array_ext.ram[%d]"%(i)]=[(0,100)]

class Model8:
    """ offset is 7-bit size
    2^7 * 3 bit secret memory
    """
    def __init__(self):
        self.other_symbols={}
        self.secret_symbols={}
        # secret offset
        self.other_symbols["\\dut.tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.ram[3]"]=[(21,8),(20,1,0),(29,3,0)]

        # size
        self.other_symbols["\\mem.sram.mem.mem_ext.ram[98]"]=[(1,8),(0,1,0)]
        for i in range(192,256):
            self.secret_symbols["\\mem.sram.mem.mem_ext.ram[%d]"%(i)]=[(0,3),(16,3),(32,3),(48,3)]
 
        self.attack_symbols={}
        for i in range(0,4):
            self.attack_symbols["\\dut.tile.frontend.bpdpipeline.bpd.counter_table.counter_table_ext.ram[%d]"%(i)]=[(0,8)]
        self.attack_symbols["\\mem.sram.mem.mem_ext.ram[64]"]=[(1,8),(0,1,0)]
        self.observable_symbols={}
        for i in range(0,8):
            self.observable_symbols["\\dut.tile.dcache.meta.tag_array.tag_array_ext.ram[%d]"%(i)]=[(0,100)]

class Model7:
    """ offset is 7-bit size
    2^7 * 3 bit secret memory
    """
    def __init__(self):
        self.other_symbols=collections.OrderedDict()
        self.secret_symbols=collections.OrderedDict()
        self.attack_symbols=collections.OrderedDict()
        self.observable_symbols=collections.OrderedDict()
 
        # secret offset
        self.other_symbols["\\dut.tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.ram[3]"]=[(22,7),(20,2,0),(29,3,0)]

        # size
        self.other_symbols["\\mem.sram.mem.mem_ext.ram[98]"]=[(2,7),(0,2,0)]
        for i in range(192,256):
            self.secret_symbols["\\mem.sram.mem.mem_ext.ram[%d]"%(i)]=[(0,3),(32,3)]
 
        for i in range(0,4):
            self.attack_symbols["\\dut.tile.frontend.bpdpipeline.bpd.counter_table.counter_table_ext.ram[%d]"%(i)]=[(0,8)]
        self.attack_symbols["\\mem.sram.mem.mem_ext.ram[64]"]=[(2,7),(0,2,0)]
        for i in range(0,8):
            self.observable_symbols["\\dut.tile.dcache.meta.tag_array.tag_array_ext.ram[%d]"%(i)]=[(0,100)]





class Model6:
    """ offset is 6-bit size
    2^6 * 3 bit secret memory
    """
    def __init__(self):
        self.other_symbols=collections.OrderedDict()
        self.secret_symbols=collections.OrderedDict()
        self.attack_symbols=collections.OrderedDict()
        self.observable_symbols=collections.OrderedDict()
 
        # secret offset
        self.other_symbols["\\dut.tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.ram[3]"]=[(23,6),(20,3,0),(29,3,0)]

        # size
        self.other_symbols["\\mem.sram.mem.mem_ext.ram[98]"]=[(3,6),(0,3,0)]
        for i in range(192,256):
            self.secret_symbols["\\mem.sram.mem.mem_ext.ram[%d]"%(i)]=[(0,3)]
        for i in range(0,4):
            self.attack_symbols["\\dut.tile.frontend.bpdpipeline.bpd.counter_table.counter_table_ext.ram[%d]"%(i)]=[(0,8)]
        self.attack_symbols["\\mem.sram.mem.mem_ext.ram[64]"]=[(3,6),(0,3,0)]
        for i in range(0,8):
            self.observable_symbols["\\dut.tile.dcache.meta.tag_array.tag_array_ext.ram[%d]"%(i)]=[(0,100)]


class Model5:
    """ offset is 5-bit size
    2^5 * 3 bit secret memory
    """
    def __init__(self):
        self.other_symbols=collections.OrderedDict()
        self.secret_symbols=collections.OrderedDict()
        self.attack_symbols=collections.OrderedDict()
        self.observable_symbols=collections.OrderedDict()
        # secret offset
        self.other_symbols["\\dut.tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.ram[3]"]=[(24,5),(20,4,0),(29,3,0)]

        # size
        self.other_symbols["\\mem.sram.mem.mem_ext.ram[98]"]=[(4,5),(0,4,0)]
        for i in range(192,256):
            if i%2==0:
                self.secret_symbols["\\mem.sram.mem.mem_ext.ram[%d]"%(i)]=[(0,3)]
            else:
                self.secret_symbols["\\mem.sram.mem.mem_ext.ram[%d]"%(i)]=[(0,0)]
        for i in range(0,4):
            self.attack_symbols["\\dut.tile.frontend.bpdpipeline.bpd.counter_table.counter_table_ext.ram[%d]"%(i)]=[(0,8)]
        self.attack_symbols["\\mem.sram.mem.mem_ext.ram[64]"]=[(4,5),(0,4,0)]
        for i in range(0,8):
            self.observable_symbols["\\dut.tile.dcache.meta.tag_array.tag_array_ext.ram[%d]"%(i)]=[(0,100)]

class Model4:
    """ offset is 4-bit size
    2^4 * 3 bit secret memory
    """
    def __init__(self):
        self.other_symbols=collections.OrderedDict()
        self.secret_symbols=collections.OrderedDict()
        self.attack_symbols=collections.OrderedDict()
        self.observable_symbols=collections.OrderedDict()
        # secret offset
        self.other_symbols["\\dut.tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.ram[3]"]=[(25,4),(20,5,0),(29,3,0)]

        # size
        self.other_symbols["\\mem.sram.mem.mem_ext.ram[98]"]=[(5,4),(0,5,0)]
        for i in range(192,256):
            if i%4==0:
                self.secret_symbols["\\mem.sram.mem.mem_ext.ram[%d]"%(i)]=[(0,3)]
            else:
                self.secret_symbols["\\mem.sram.mem.mem_ext.ram[%d]"%(i)]=[(0,0)]
 
        for i in range(0,4):
            self.attack_symbols["\\dut.tile.frontend.bpdpipeline.bpd.counter_table.counter_table_ext.ram[%d]"%(i)]=[(0,8)]
        self.attack_symbols["\\mem.sram.mem.mem_ext.ram[64]"]=[(5,4),(0,5,0)]
        for i in range(0,8):
            self.observable_symbols["\\dut.tile.dcache.meta.tag_array.tag_array_ext.ram[%d]"%(i)]=[(0,100)]


class Model3PrimeProbe:
    """ offset is 3-bit size
    2^3 * 3 bit secret memory
    """
    def __init__(self,top="\\dut.tile"):
        self.__bits=3
        self.__top=top
        self.other_symbols=collections.OrderedDict()
        self.secret_symbols=collections.OrderedDict()
        self.attack_symbols=collections.OrderedDict()
        self.observable_symbols=collections.OrderedDict()
        self.setAttack()
        self.setSecret()
        self.setObserve()
        self.setOther()
    def setAttack(self):
        self.attack_symbols={}
        for i in range(0,4):
            self.attack_symbols["%s.frontend.bpdpipeline.bpd.counter_table.counter_table_ext.ram[%d]"%(self.__top,i)]=[(0,8)]
        self.attack_symbols["\\mem.sram.mem.mem_ext.ram[64]"]=[(9-self.__bits,self.__bits),(0,9-self.__bits,0)]

        self.attack_symbols["%s.dcache.meta.tag_array.tag_array_ext.ram[%d]"%(self.__top,0)]=[(0,sys.maxint)]

    def setSecret(self):
        for i in range(192,256):
            if i%8 == 0:
                self.secret_symbols["\\mem.sram.mem.mem_ext.ram[%d]"%(i)]=[(0,3)]

    def setOther(self):
        self.other_symbols["%s.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.ram[3]"]=[(self.__top,29-self.__bits,self.__bits),(20,9-self.__bits,0),(29,3,0)]
        # size
        self.other_symbols["\\mem.sram.mem.mem_ext.ram[98]"]=[(9-self.__bits,self.__bits),(0,9-self.__bits,0)]
        self.other_symbols["%s.dcache.lfsr"%(self.__top)]=[(0,16)]
    def setObserve(self):
        for j in range(0, 1):
            for i in range(0,nWays):
                self.observable_symbols["%s.dcache.meta.tag_array.tag_array_ext.ram[%d]"%(self.__top,j)]=[(0,sys.maxint)]


class ModelCacheSideChannelRandomObserveCounter:
    """ offset is 3-bit size
    2^3 * 3 bit secret memory
    """
    def __init__(self):
        self.other_symbols=collections.OrderedDict()
        self.secret_symbols=collections.OrderedDict()
        self.attack_symbols=collections.OrderedDict()
        self.observable_symbols=collections.OrderedDict()
        nMem=32
        # secret offset = operands in second instruction
        for i in range(0,nMem):
            for way in range(0,nWays):
                if nWays>1:
                    self.other_symbols["\\top.boom_tile.dcache.random_map_array_way[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                self.other_symbols["\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                self.other_symbols["\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                if args.leak==1:
                    if nWays>1:
                        self.observable_symbols["\\top.boom_tile.dcache.random_map_array_way[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                    self.observable_symbols["\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                    self.observable_symbols["\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]

        self.secret_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[0]"]=[(52,8)]
        # size
        for i in range(16):
            self.other_symbols["\\top.boom_tile.dcache.MaxPeriodFibonacciLFSR.state_%d"%(i)]=[(0,1)]
        for i in range(0,32):
            self.observable_symbols["final_cache_observe_%d"%(i)]=[(0,sys.maxint)]
        for i in range(0,32):
            for way in range(0,nWays):
                if nWays>1:
                    self.observable_symbols["attack_\\top.boom_tile.dcache.random_map_array_way[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                self.observable_symbols["attack_\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
                self.observable_symbols["attack_\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(way*nMem+i)]=[(0,sys.maxint)]
        for i in range(0,32):
            self.attack_symbols["cache_observe_%d"%(i)] = [(0,1)]
class ModelCacheSideChannelRandomObserve:
    """ offset is 3-bit size
    2^3 * 3 bit secret memory
    """
    def __init__(self):
        self.other_symbols=collections.OrderedDict()
        self.secret_symbols=collections.OrderedDict()
        self.attack_symbols=collections.OrderedDict()
        self.observable_symbols=collections.OrderedDict()
        # secret offset = operands in second instruction
        for i in range(0,32*4):
            if nWays>1:
                self.other_symbols["\\top.boom_tile.dcache.random_map_array_way[%d]"%(i)]=[(0,sys.maxint)]
            self.other_symbols["\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(i)]=[(0,sys.maxint)]
            self.other_symbols["\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(i)]=[(0,sys.maxint)]
        self.secret_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[0]"]=[(52,8)]
        # size
        for i in range(16):
            self.other_symbols["\\top.boom_tile.dcache.MaxPeriodFibonacciLFSR.state_%d"%(i)]=[(0,1)]
        for i in range(0,nWays):
            for j in range(nSets):
                self.other_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i*nSets+j)]=[(0,sys.maxint)]
        for i in range(0,nWays):
            for j in range(0,nSets):
                self.observable_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i*nSets+j)]=[(0,sys.maxint)]
        for i in range(0,32):
            self.attack_symbols["cache_observe_%d"%(i)] = [(0,1)]


class ModelCacheSideChannelRandomOld:
    """ offset is 3-bit size
    2^3 * 3 bit secret memory
    """
    def __init__(self):
        self.other_symbols=collections.OrderedDict()
        self.secret_symbols=collections.OrderedDict()
        self.attack_symbols=collections.OrderedDict()
        self.observable_symbols=collections.OrderedDict()
        # secret offset = operands in second instruction
        for i in range(0,32):
            if nWays>1:
                self.other_symbols["\\top.boom_tile.dcache.random_map_array_way[%d]"%(i)]=[(0,sys.maxint)]
            self.other_symbols["\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(i)]=[(0,sys.maxint)]
            self.other_symbols["\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(i)]=[(0,sys.maxint)]
        self.secret_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[0]"]=[(52,8)]
        # size
        for i in range(16):
            self.other_symbols["\\top.boom_tile.dcache.MaxPeriodFibonacciLFSR.state_%d"%(i)]=[(0,1)]
        for i in range(0,nWays):
            self.other_symbols["\\top.boom_tile.dcache.meta_0.tag_array_%d[%d]"%(i,0)]=[(0,sys.maxint)]
        for i in range(0,nWays):
            for j in range(0,1):
                self.observable_symbols["\\top.boom_tile.dcache.meta_0.tag_array_%d[%d]"%(i,j)]=[(0,sys.maxint)]


class ModelCacheSideChannelRandomObserve:
    """ offset is 3-bit size
    2^3 * 3 bit secret memory
    """
    def __init__(self):
        self.other_symbols=collections.OrderedDict()
        self.secret_symbols=collections.OrderedDict()
        self.attack_symbols=collections.OrderedDict()
        self.observable_symbols=collections.OrderedDict()
        # secret offset = operands in second instruction
        for i in range(0,32*4):
            if nWays>1:
                self.other_symbols["\\top.boom_tile.dcache.random_map_array_way[%d]"%(i)]=[(0,sys.maxint)]
            self.other_symbols["\\top.boom_tile.dcache.random_map_array_req_idx[%d]"%(i)]=[(0,sys.maxint)]

            self.other_symbols["\\top.boom_tile.dcache.random_map_array_subIdx[%d]"%(i)]=[(0,sys.maxint)]
        self.secret_symbols["\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[0]"]=[(52,8)]
        # size
        for i in range(16):
            self.other_symbols["\\top.boom_tile.dcache.MaxPeriodFibonacciLFSR.state_%d"%(i)]=[(0,1)]
        for i in range(0,nWays*nSets):
            self.other_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i)]=[(0,sys.maxint)]
        for i in range(0,nWays):
            for j in range(0,nSets):
                self.observable_symbols["\\top.boom_tile.dcache.meta_0.tag_array[%d]"%(i*nSets+j)]=[(0,sys.maxint)]



class ModelCacheSideChannelold:
    """ offset is 3-bit size
    2^3 * 3 bit secret memory
    """
    def __init__(self):
        self.other_symbols=collections.OrderedDict()
        self.secret_symbols=collections.OrderedDict()
        self.attack_symbols=collections.OrderedDict()
        self.observable_symbols=collections.OrderedDict()
        # secret offset = operands in second instruction
        self.secret_symbols["\\dut.tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.ram[0]"]=[(52,8)]
        # size
        self.other_symbols["\\dut.tile.dcache.lfsr"]=[(0,16)]
        for i in range(0,1):
            self.other_symbols["\\dut.tile.dcache.meta.tag_array.tag_array_ext.ram[%d]"%(i)]=[(0,sys.maxint)]
        for i in range(0,1):
            self.observable_symbols["\\dut.tile.dcache.meta.tag_array.tag_array_ext.ram[%d]"%(i)]=[(0,sys.maxint)]


class ModelCacheSideChannel:
    """ offset is 3-bit size
    2^3 * 3 bit secret memory
    """
    def __init__(self):
        self.other_symbols=collections.OrderedDict()
        self.secret_symbols=collections.OrderedDict()
        self.attack_symbols=collections.OrderedDict()
        self.observable_symbols=collections.OrderedDict()
        # secret offset = operands in second instruction
        self.secret_symbols["\\TestHarness.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[0]"]=[(52,8)]

        #self.secret_symbols["TestHarness.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[0]"]=[(52,8)]
        # size
        #self.other_symbols["\\TestHarness.boom_tile.dcache.lfsr"]=[(0,16)]
        for i in range(0,nSets):
            for j in range(0,nWays):
                self.other_symbols["\\TestHarness.boom_tile.dcache.meta_0.tag_array.tag_array_ext.mem_0_%d.ram[%d]"%(j,i)]=[(0,sys.maxint)]
        for i in range(0,nSets):
            for j in range(0,nWays):
                self.observable_symbols["\\TestHarness.boom_tile.dcache.meta_0.tag_array.tag_array_ext.mem_0_%d.ram[%d]"%(j,i)]=[(0,sys.maxint)]


class ModelTiny:
    """ offset is 3-bit size
    2^3 * 3 bit secret memory
    """
    def __init__(self):
        self.other_symbols=collections.OrderedDict()
        self.secret_symbols=collections.OrderedDict()
        self.attack_symbols=collections.OrderedDict()
        self.observable_symbols=collections.OrderedDict()
        # secret offset
        self.other_symbols["\\dut.tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.ram[3]"]=[(26,3),(20,6,0),(29,3,0)]
        # size
        self.other_symbols["\\mem.sram.mem.mem_ext.ram[98]"]=[(6,3),(0,6,0)]
        for i in range(192,256):
            if i%8==0:
                self.secret_symbols["\\mem.sram.mem.mem_ext.ram[%d]"%(i)]=[(0,3)]
            else:
                self.secret_symbols["\\mem.sram.mem.mem_ext.ram[%d]"%(i)]=[(0,0)]
 

        for i in range(0,4):
            self.attack_symbols["\\dut.tile.frontend.bpdpipeline.bpd.counter_table.counter_table_ext.ram[%d]"%(i)]=[(0,8)]
        self.attack_symbols["\\mem.sram.mem.mem_ext.ram[64]"]=[(6,3),(0,6,0)]

        for i in range(0,nSets):
            self.observable_symbols["\\dut.tile.dcache.meta.tag_array.tag_array_ext.ram[%d]"%(i)]=[(0,100)]

class ModelComplete:
    def __init__(self):
        self.other_symbols=collections.OrderedDict()
        self.secret_symbols=collections.OrderedDict()
        self.attack_symbols=collections.OrderedDict()
        self.observable_symbols=collections.OrderedDict()
        self.other_symbols["\\dut.tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.ram[3]"]=[(20,9)]
        self.other_symbols["\\mem.sram.mem.mem_ext.ram[98]"]=[(0,9)]
        for i in range(192,256):
            self.secret_symbols["\\mem.sram.mem.mem_ext.ram[%d]"%(i)]=[(0,3),(8,3),(16,3),(24,3),(32,3),(40,3),(48,3),(54,3)]
        for i in range(0,4):
            self.attack_symbols["\\dut.tile.frontend.bpdpipeline.bpd.counter_table.counter_table_ext.ram[%d]"%(i)]=[(0,8)]
        self.attack_symbols["\\mem.sram.mem.mem_ext.ram[64]"]=[(0,9)]
        for i in range(0,nSets):
            self.observable_symbols["\\dut.tile.dcache.meta.tag_array.tag_array_ext.ram[%d]"%(i)]=[(0,100)]

import argparse
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='match symbol')
    parser.add_argument('file',metavar='files',type=str,help='smt file '
    'generated from yosys tool')
    
    parser.add_argument('--solfile',type=str,default="test.cnf",help='solution file ')
    parser.add_argument('--cnffile',type=str,default="test.cnf",help='cnf file '
            'generated from yices-smt2')
    parser.add_argument('--smt2file',type=str,default=None,help='output smt2 file '
            'used to add hash constraint for counting')
    parser.add_argument('--nstate',type=int,default=5,help='the number of '
            'states')
    parser.add_argument('--stateindex',type=int,default=0,help='stateindex e.g., 0 -> s0, 10 ->s10')
    parser.add_argument('--autoinit',type=bool,default=False,help='Auto init unitialized vars')
    parser.add_argument('--mode',type=str,default="mark",help='1. mark cnf file with jac and indze init file and print out uninited symbols, init: init; dumpmap: dump name -> var, dumpsym')
    parser.add_argument('--reserve_symbol',type=bool,default=False,help='reserve symbol')
    parser.add_argument('--model',type=str,default="tiny",help='Victim Model: tiny-> 3-bit offset, complete-> 8-bit offset')

    
    parser.add_argument('--leak',type=int,default=0,help='set to 1 if want to leak randommap')
    parser.add_argument('--model_observe_counter',type=bool,default=False,help='set to false if want to use tag arrays')

    parser.add_argument('--nway',type=int,default=4,help='#Cache set in D-cache')
    parser.add_argument('--nset',type=int,default=8,help='#Cache set in D-cache')
    models={"tiny":ModelTiny,"complete": ModelComplete,'1-bit':Model1,"4-bit": Model4, '5-bit':Model5, '6-bit': Model6, '7-bit':Model7, '8-bit': Model8,"sidechannel_random":ModelCacheSideChannelRandom,"sidechannel":ModelCacheSideChannelold,"sidechannel_new":ModelCacheSideChannel,"3-bit-random": Model3PrimeProbeRandom, "3-bit-prime": Model3PrimeProbe,"sidechannel_observe":ModelCacheSideChannelRandomObserve,"sidechannel_observecounter":ModelCacheSideChannelRandomObserveCounter,"modexp":ModelCacheModExpRandom,"spectre":ModelSpectreRandom, "spectreMemDelay":ModelSpectreMemDelay,"spectreTarget":ModelSpectreTarget,"spectreTargetMemDelay":ModelSpectreTargetMemDelay, "sidechannel_demand":ModelCacheSideChannelDemands, "cachedefense":ModelCacheDefenseRandom }

    args=parser.parse_args()
    nSets=args.nset
    nWays=args.nway
    nEntry=nWays*nSets
    model_observe_counter=args.model_observe_counter
    model=models[args.model]()
    main(args,model)

