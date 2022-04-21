'''
Created on Nov 5, 2021

@author: digitalia-aj
'''
import uuid

def getuuid4():
    uuid4 = uuid.uuid4()
    return uuid4

def createRootMets():
    """
    rootuuid4 = OBJID
    dmduuid4 = dmdsec ID
    amduuid4 = amdsec ID
    fileuuid4 = filesec ID
    filegrpuuid4 = filegroup ID, common filegroup root
    structuuid4 = strictmap ID
    
    """