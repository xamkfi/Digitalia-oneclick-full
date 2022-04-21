'''
Created on Nov 16, 2021

@author: digitalia-aj
'''
import hashlib

def calculateSHA256(filePath):
    sha = hashlib.sha256()
    with open (filePath, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha.update(byte_block)
            #print("Sha256 for file {} is {}".format(onePath, sha.hexdigest()))            
    return sha.hexdigest()        
    