'''
Created on Nov 5, 2021

@author: digitalia-aj
First experiment with Jinja template engine https://genshi.edgewall.org/
'''
import jinja2
import os
from jinja2.runtime import Undefined
#from dataReceiver import receiver
#from dataStorage import storage
import metadataReader
#from pip._vendor.distlib.util import tempdir
#from idlelib.idle_test.test_configdialog import root
#from mainapp import instantedStorage
#from importlib.resources import path

templateLoader = jinja2.FileSystemLoader(searchpath=os.path.dirname(os.path.abspath(__file__)))
templateEnv = jinja2.Environment(loader=templateLoader, undefined=Undefined)
#Mets template
rootMETSTemplateFile = "rootMETS_template.xml"
rootMETSTemplate = templateEnv.get_template(rootMETSTemplateFile)
#DC template
rootDCTemplateFile = "rootDC_template.xml"
rootDCTemplate = templateEnv.get_template(rootDCTemplateFile)

#repMets template
repMETSTemplateFile = "repMETS_template.xml"
repMETSTemplate = templateEnv.get_template(repMETSTemplateFile)

#repMets file section template, used in a loop going through the available files
repFileTemplateFile = "repMETS-file_template.xml"
repFileTemplate = templateEnv.get_template(repFileTemplateFile)

#repMets structmap section template, used in a loop going through the available files
repStructTemplateFile = "repMETS-struct_template.xml"
repStructTemplate = templateEnv.get_template(repStructTemplateFile)

repmetsValues = ['File_MIMEType', 'File_FileModifyDate', 'sha256', 'fileID', 'File_FileSize', 'relativePath']

tempStructMap = ""

def createRootMets(data):
    print("Creating root METS.xml file")
    mets = rootMETSTemplate.render(data)
    return mets

def createRepMets(data):
    print("Creating root METS.xml file")
    repmets = repMETSTemplate.render(data)
    return repmets

def createRootDC(data):
    print("Creating root DC.xml file")
    dc = rootDCTemplate.render(data)
    return dc

def generateRepMetsFileSection(rootuuid4, storage):
    print("Generating repmets.xml filesection and structmap for id, {}".format(rootuuid4))
    metaDic = storage.getPayloadMetadata(rootuuid4) # structure {rootuuid:{key:value}}
    #print("File(s) metadata IS {}".format(metaDic))
    xmlfileSec = ""
    xmlStructMapSec = ""
    for key in metaDic:
        tempDic = metaDic[key]
        #print("{}".format(tempDic))
        fileDic = {}
        for onekey in tempDic:            
            if onekey in repmetsValues:                
                    
                #print("{}--{}".format(str(onekey).replace('-','_'), tempDic[onekey]))
                fileDic[str(onekey).replace('-','_')] = tempDic[onekey]
                #fileDic[str(key).replace(':', '_').replace('-','_')]=tempDic[key]
                #fileDic.update({str(key).replace(':', '_').replace('-','_'):fileDic[onekey]}) 
        xmlfileSec += repFileTemplate.render(fileDic)
        xmlStructMapSec +=repStructTemplate.render(fileDic)
        #print("{}---{}".format(key, metaDic[key]))
        tempDic = fileDic = {}
    #xmlFileSec goes directly to correct place, store the structmap so the below function can get it when needed
    global tempStructMap 
    tempStructMap = xmlStructMapSec
    return xmlfileSec    


def getRepMetsStructMapSection():       
    return tempStructMap
