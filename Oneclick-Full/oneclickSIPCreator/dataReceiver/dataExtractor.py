'''
Created on Oct 26, 2021

@author: digitalia-aj
'''
import tarfile
import os
import zipfile
import gzip

def extractTarGz(pathname):
    print("Extract tar.xz")
    tf = tarfile.open(pathname)
    #print(os.path.dirname(pathname))
    extractPath = os.path.join(os.path.dirname(pathname), "extracted")
    tf.extractall(path=extractPath)
    return extractPath

def extractZip(pathname):
    print("Extract zip")
    zf = zipfile.ZipFile(pathname, 'r')
    extractPath = os.path.join(os.path.dirname(pathname), "extracted")
    zf.extractall(path=extractPath)
    return extractPath

