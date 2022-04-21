'''
Created on Oct 5, 2021

@author: digitalia-aj
'''
import os
from bs4 import BeautifulSoup as bs
import json
import magic
import shutil
import datetime
import pytz
import time
import zipfile
from langdetect import detect
#import timeit
import subprocess
import xml.etree.ElementTree as ET
from dataReceiver import dataExtractor
from metadataReader import readMetadata
from IDCreator import uuidCreator
from templating import xmlTemplating
#from pip._vendor.pkg_resources import ZipProvider
from dataReceiver.filenameFixer import checkAndFixFileNames
from dataStorage import storage
#from email.mime import base



metsDCValues = ['Content-Length', 'sha256' ]
#validator = "commons-ip2-cli-2.0.1.jar"

deletePath = True
includeSchemas = False

runtimeDir = "/home/digitalia-aj/extraspace/runtimefiles/"
csversion = "2.0.1"

"""
Creates the basic SIP folder structure, metadata, representations, datauuid and data folder
return the paths (root and datapath) in a list
"""
def createBasicSIPDirStructure(rootUUIDDir, repUUIDDir):
    returnDict = {}
    basePath = os.path.join(os.path.dirname(runtimeDir), str(rootUUIDDir))
    returnDict['basePath']=basePath
    metaPath = os.path.join(basePath, "metadata")
    returnDict['metaPath']=metaPath    
    metaDescPath = os.path.join(metaPath, "descriptive")
    returnDict['metaDescPath']=metaDescPath
    #metaPresPath = os.path.join(metaPath, "preservation")
    #returnDict['metaPresPath']=metaPresPath
    repPath = os.path.join(basePath, "representations")
    returnDict['repPath']=repPath    
    repuuidPath = os.path.join(repPath, str(repUUIDDir))
    returnDict['repuuidPath']=repuuidPath
    dataPath = os.path.join(repuuidPath, "data")    
    returnDict['dataPath']=dataPath
    #/metadata/originals 
    repMetaPath = os.path.join(repuuidPath, "metadata")    
    returnDict['repMetaPath']=repMetaPath
    repOrgMetaPath = os.path.join(repMetaPath, "originals")    
    returnDict['repOrgMetaPath']=repOrgMetaPath
    
    if not (os.path.exists(basePath)):
        os.mkdir(basePath)
        print("created base SIP path {}".format(basePath))
    if (os.path.exists(basePath)):
        os.mkdir(metaPath)
        os.mkdir(metaDescPath) 
        #os.mkdir(metaPresPath)
        os.mkdir(repPath)
        os.mkdir(repuuidPath)
        os.mkdir(dataPath)
        os.mkdir(repMetaPath)
        os.mkdir(repOrgMetaPath)
     
    return returnDict


def getCurrentTime():
    #datetime.datetime.now(pytz.timezone('Europe/Paris')).isoformat()    
    return (datetime.datetime.now(pytz.timezone('Europe/Helsinki')).isoformat())
   

def moveFilesToNewDir(originalPath, newPath):    
    #print(extradir)
    shutil.move(originalPath, newPath)
    fullpath = os.path.join(newPath, os.path.basename(originalPath))
    return fullpath

def getMimeType(pathname):
    return magic.from_file(pathname,mime=True)

def parseXMLData(xmldatafile):
    with open(xmldatafile, "r") as file:
        content = file.readlines()
        # Combine the lines in the list into a string
        content = "".join(content)
        bs_content = bs(content, "xml")        
        retData = ""
        for tag in bs_content.find_all():
            if len(tag.findChildren())>0:
                print("{} Has childs, print nothing".format(tag.name))
            else:
                retData+="{}".format(tag)
        
    return retData

def handleFile(pathname):
    allFiles = []
    print("It's a file with path {}".format(pathname))
    mimetype = getMimeType(pathname)
    #print(mimetype)        
    if (mimetype=="application/x-xz"):                
        allFiles = handleDir(dataExtractor.extractTarGz(pathname))
    if (mimetype=="application/zip"):
        allFiles = handleDir(dataExtractor.extractZip(pathname))    
    if (mimetype=="application/x-gzip"): ##works for tar.gz but not plain gz files
        allFiles = handleDir(dataExtractor.extractTarGz(pathname))
    else:
        allFiles.append(pathname)    
    #if (mimetype=="application/x-7z-compressed"):
    
    return allFiles
    
def handleDir(pathname, repOrgMetaPath, storage):
    print("It is a directory, with path {}".format(pathname))            
    #Browse the directory content and save all files with paths to dictionary
    return getDirectoryContent(pathname, repOrgMetaPath, storage)
    
def getdirSize(pathname):
    dirsize = subprocess.check_output(['du','-sb', pathname]).split()[0].decode('utf-8')
    return dirsize

def createZIPfromFiles(filelist, sipname, basePath):
    print("Zipping {}".format(filelist))
    zipPath = os.path.join(basePath, sipname+"+validation-report.zip")
    print(zipPath)
    with zipfile.ZipFile(zipPath, 'w') as zipper:
        for file in filelist:
            zipper.write(file, os.path.basename(file))
    
    return zipPath

def createZIPfromSIP(basePath, baseName):
    print("Zipping {}".format(os.path.dirname(basePath)))
    zipPath = basePath+".zip"
    shutil.make_archive(basePath, 'zip', os.path.dirname(basePath), str(baseName))
    return zipPath

def doVirusScan(path):
    print("Completing antivirus scan, takes a while..")
    "clamscan -r -o rektori_kaskkirjad/"
    value = -1
    AVProcess = subprocess.Popen(['clamscan', '-r', '-o', path], stdout=subprocess.PIPE, universal_newlines=True)
    results = str(AVProcess.communicate()[0]).strip().splitlines()
    for line in results:
        if line.startswith("Infected"):
            key, value = line.split(":")
            
    return value

def cleanEmptyDirs(basePath):
    deletedFolders = 0
    for root, dirs, files in os.walk(basePath):
        if len(dirs)==0 and len(files)==0:
            shutil.rmtree(root)
            deletedFolders+=1
    if deletedFolders>0:
        cleanEmptyDirs(basePath) #Check if there are any new empty folders
    return

def checkRepMetsFileContent(repMets_file, inputPaths, repuuidPath):
    print("Checking the generated {} file".format(repMets_file))  
    repuuidPath+="/"
    tree = ET.parse(repMets_file)
    root = tree.getroot()
    orgPaths = []
    for orgPath in inputPaths:
        orgPaths.append(str(orgPath).replace(repuuidPath, ""))        
    #print(orgPaths)
    
    for elem in root.iter("{http://www.loc.gov/METS/}FLocat"):        
        #print("{}".format(elem.attrib["{http://www.w3.org/1999/xlink}href"]))
        if elem.attrib["{http://www.w3.org/1999/xlink}href"] in orgPaths:
            orgPaths.remove(elem.attrib["{http://www.w3.org/1999/xlink}href"])
    print("{} files not found in mets.xml -->{}".format(len(orgPaths), orgPaths))

def handleCreationEvent(event, storage):
    """gets the event from watchdog. Only the on_created event gets in here """
    rootMets = {} 
    repMets = {}
    rootDC = {}    
    pathname = event.src_path 
    #print(pathname)
    #stats = os.stat(pathname)
    
    """These are mandatory elements to ensure upload is completed before the processing starts
    So, What ever you do, do not remove these, changes towards better are accepted :)
    """
    if (event.is_directory==False): #It is a file, check it's size changes
        historicalSize = -1
        while (historicalSize != os.path.getsize(pathname)):        
            print("Waiting for a complete file.. size is now {}".format(os.path.getsize(pathname)))
            historicalSize = os.path.getsize(pathname)
            time.sleep(2)
                
    elif(event.is_directory): #It is a folder, check it's size changes
        historicalSize = -1        
        while historicalSize != getdirSize(pathname):
            time.sleep(2) 
            historicalSize = getdirSize(pathname)
            print("Uploading {}.. size is now {}".format(pathname, historicalSize))
        if historicalSize == 0:
            print("Empty folder uploaded, nothing to process..")
            return    
    #sleep 5 more seconds just to ensure that copying is actually finished
    #print("Extra sleeping time")
    #time.sleep(5)
    #print("Continuing")    
    #Viruscheck etc. checks should be made here right after completed upload
    if storage.getConfigItem("dovirusscan") == "True":
        retval = (doVirusScan(pathname).strip())
        print("Antivirus found {} threats - continuing".format(retval))    
    else:
        print("Virus check disabled via config.ini file")
        retval = 0 #This is the value that allows contiuning the process
    
    #print(retval)
    if str(retval) != "0":
        print("Virus scan found {} suspicious files from the uploaded content, stopping the process now".format(retval))
        
    else:
        
        SIPPathNames = {}
        rootuuid4 = repuuid4 = ""     
        #Just a double check that the path truly exists    
        if (os.path.exists(pathname)): 
            #Calls a method that checks and fixes invalid filenames
            pathname = checkAndFixFileNames(pathname)
            
            
            rootuuid4 = uuidCreator.getuuid4() #UUID for the whole sip
            rootMets.update({'rootuuid4':rootuuid4})
            rootDC.update({'rootuuid4':rootuuid4})
            repuuid4 = uuidCreator.getuuid4() ##UUID for the representation directory
            rootMets.update({'repuuid4':repuuid4})
            SIPPathNames = createBasicSIPDirStructure(rootuuid4, repuuid4)
            """After creation SIPPathNames contains, need to add schema and documentation paths also
            basePath, metaPath, metaDescPath, 
            repPath, repuuidPath, dataPath 
            repMetaPath and repOrgMetaPath
            """
            
            pathname = moveFilesToNewDir(pathname, SIPPathNames['dataPath'])
            createTime = getCurrentTime()
            rootMets.update({'creationDate':createTime})
            rootMets.update({'modificationDate':createTime})
            #rootMets.update({'generateRepMapFromFolderStructure':xmlTemplating.generateRepMapFromFolderStructure(SIPPathNames['repPath'])})
            
            rootDC.update({'dc_date':createTime})
            repMets.update({'creationDate':createTime})
            repMets.update({'rootuuid4':rootuuid4})
            repMets.update({'repuuid4':repuuid4})
                    
        else:
            print("Given path does not exists, nothing to do, quitting..")
        
        if (event.is_directory==False):
            allFiles = handleFile(pathname)        
        elif(event.is_directory):
            payloadAndMetaPaths = handleDir(pathname, SIPPathNames['repOrgMetaPath'], storage)
            allFiles = payloadAndMetaPaths[0]
            metaFiles = payloadAndMetaPaths[1] #This contains just the paths to original metadatafiles
            if len(metaFiles)>0:
                allFiles = allFiles+metaFiles #Add metadatafiles to allfiles to ensure those appear in repmets file
                for onemetafile in metaFiles:
                    extraDCData = parseXMLData(onemetafile)
                    #Tries to identify the language of the metadatafile                    
                    rootDC.update({"dc_language":"{}".format(detect(extraDCData))})
                    rootDC.update({"dc_additional":"{}".format(extraDCData)})
        #print("All found files {}".format(allFiles))
        if(len(allFiles)==0):
            print("No files to process, quitting")
            return
        else:
            #print("File list content {}".format(allFiles))
            instantedMetadataReader = readMetadata.readMeta()    
            PayloadMetadataDict = instantedMetadataReader.getMetadataForFileList(allFiles, SIPPathNames['repuuidPath']) #Calls metadata harvester
            #Store the collected files metadata to a storage for later use
            storage.storePayloadMetadata(rootuuid4, PayloadMetadataDict)
            #above dict contains full file path:all its meta in a dict) below is just for testing the content
            
            #for key in FilesMetadataDict:
            #    print("{}---{}".format(key, FilesMetadataDict[key]))
            
            #Use it to generate rootDC infos
            #rootDCMeta = createRootDCDict(PayloadMetadataDict)
            #rootDC.update(rootDCMeta) #Write the found meta to the rootDCMeta
            
            #Last repmets updates
            repMets.update({'generateRepMetsFileSection':xmlTemplating.generateRepMetsFileSection(rootuuid4, storage)})
            repMets.update({'getRepMetsStructMapSection':xmlTemplating.getRepMetsStructMapSection()})
            
            #Write repmets.xml file
            repMets_xml = xmlTemplating.createRepMets(repMets)
            repMets_file = os.path.join(SIPPathNames['repuuidPath'],'METS.xml')
            repMets_writer = open(repMets_file, 'w+')
            repMets_writer.write(repMets_xml)
            repMets_writer.close()
            
            #Not needed, just for testing the repmets content
            checkRepMetsFileContent(repMets_file, allFiles, SIPPathNames['repuuidPath'])
            
            #gets metadata for above created repMETS.xml file
            repMETSMetaDict = instantedMetadataReader.getMetadataForFileList([repMets_file], SIPPathNames['dataPath'])
            #print(len(repMETSMetaDict))
            temprepMETSMeta = list(repMETSMetaDict.values())[0] #Contains meta for just repmets.xml
            for key in temprepMETSMeta:
                #print("repmets for root: {}-->{}".format("repmets_"+key, temprepMETSMeta[key]))        
                #if key in metsrepMETSValues:            
                rootMets.update({str("repmets_"+key).replace(':', '_').replace('-','_'):temprepMETSMeta[key]})   
        
            
            
            #Write root DC.xml file
            print("Content of rootDC meta is {}".format(rootDC))
            rootDC_xml = xmlTemplating.createRootDC(rootDC)
            rootDC_file = os.path.join(SIPPathNames['metaDescPath'],'DC.xml')
            rootDC_writer = open(rootDC_file, 'w+')
            rootDC_writer.write(rootDC_xml)
            rootDC_writer.close()
            
            #gets metadata for above created DC.xml file
            dcMetaDict = instantedMetadataReader.getMetadataForFileList([rootDC_file], SIPPathNames['basePath'])
            tempDCMeta = list(dcMetaDict.values())[0]
            
            for key in tempDCMeta:
                #print("dc for root: {}-->{}".format("dc_"+key, tempDCMeta[key]))        
                #if key in metsDCValues:            
                rootMets.update({str("dc_"+key).replace(':', '_').replace('-','_'):tempDCMeta[key]})             
            
            #print("Root mets content is {}".format(rootMets))
            
            #The last phase is to write rootmets metadata into SIP format
            rootMets_xml = xmlTemplating.createRootMets(rootMets)
            rootMets_file = os.path.join(SIPPathNames['basePath'],'METS.xml')
            rootMets_writer = open(rootMets_file, 'w+')
            rootMets_writer.write(rootMets_xml)
            rootMets_writer.close()
            
            #Cleans empty dirs
            cleanEmptyDirs(SIPPathNames['basePath'])
            
            zipPath = createZIPfromSIP(SIPPathNames['basePath'], rootuuid4)
            print("SIP file in {}".format(zipPath))
            if os.path.isfile(zipPath) and deletePath:
                shutil.rmtree(SIPPathNames['basePath'])    
                #Last step is to validate the SIP file with commons IP
                commonsip = storage.getConfigItem("commonsip")
                #subprocess.call(['java', '-jar', commonsip, "validate", "-i", zipPath, "-r"])
                validateProcess = subprocess.Popen(['java', '-jar', commonsip, "validate", "-i", zipPath, "-r"], stdout=subprocess.PIPE, universal_newlines=True)
                validateReportPath = str(validateProcess.communicate()[0]).strip()
                print("Validate Results = {}".format(validateReportPath))
                try:
                    report = open(validateReportPath)
                    data = json.load(report)
                    validationResult = data["summary"]["result"]
                    if validationResult=="VALID":
                        print("SIP succesfully validated against commons-ip version {}".format(csversion))
                        zipFiles=[zipPath, validateReportPath]
                        createZIPfromFiles(zipFiles, str(rootuuid4), storage.getConfigItem("completeddir"))
                    
                except OSError as err:
                    print("OS error, {}".format(err))
                    pass
            
            return


def getDirectoryContent(pathname, repOrgMetaPath, storage):
    print("Browsing content of dir {}".format(pathname))
    payloadFilePaths = []    
    orgMetadataFilePaths = []
    definedMetaFiles = storage.getConfigItem("metadata").split(';')
    print("Config.ini file defined {} file(s), check if those exists and find metadata".format(definedMetaFiles))
    
    pathcontent = os.scandir(pathname) #Only seeks metadata files within the first folder
    for entry in pathcontent: #Takes care of moving eka digiteek original metadata files
        if entry.is_file():
            if entry.name in definedMetaFiles: #Adds config.ini defined file(s) to org metadatalist
                print("{} file found withing the root folder, read metadata".format(entry.name))
                newPath = moveFilesToNewDir(os.path.join(pathname, entry.name), repOrgMetaPath)
                orgMetadataFilePaths.append(newPath)
                
            #Then check is similarly named folder exists inside the same path
            """
            if (os.path.isdir(os.path.join(pathname, os.path.splitext(entry.name)[0]))):
                print("EKA xml-file & folder combo found {}, move metadata to correct folder".format(entry.name))                
                newPath = moveFilesToNewDir(os.path.join(pathname, entry.name), repOrgMetaPath)
                orgMetadataFilePaths.append(newPath)
            """
            
    #Gets all file paths to a list
    for root, dirs, files in os.walk(pathname, onerror=getDirectoryContentError):        
        for onefile in files:                
            fullpath = os.path.join(root, onefile)
            payloadFilePaths.append(fullpath)
    
    finalPaths = [payloadFilePaths, orgMetadataFilePaths] #orgMetaDataFilePaths is empty if now meta is found    
    return finalPaths    
    

def getDirectoryContentError(quilty):
    print("Error in directory browsing {}".format(type(quilty)))
    pass
    
    
    
"""NOT USED, stored for reference
    idList = []
    createtimeList =[]
    unitnameList = []
    parentidList = []
    restrictedList = []
    descriptionList = []
    coverageList = []
    creatorList = []
    
    #Update rootDC with info from metaFiles
    for onemetafile in metaFiles:
        extraDCData = parseXMLData(onemetafile)
        {'item_id': '3271184', 'item_create_time': '2021-05-26 10:45:00.074964', 
        'item_unit_name': 'Eesti Kunstiakadeemia', 'item_parent_id': '2230652', item_is_restricted:'0'}
        if 'item_id' in extraDCData:
            idList.append(extraDCData['item_id'])
        if 'item_create_time' in extraDCData:
            createtimeList.append(extraDCData['item_create_time'])
        if 'item_unit_name' in extraDCData:
            unitnameList.append(extraDCData['item_unit_name'])
        if 'item_parent_id' in extraDCData:
            parentidList.append(extraDCData['item_parent_id'])
        if 'item_is_restricted' in extraDCData:
            restrictedList.append(extraDCData['item_is_restricted'])
        if 'description' in extraDCData:
            descriptionList.append(extraDCData['description'])
        if 'coverage' in extraDCData:
            coverageList.append(extraDCData['coverage'])
        if 'creator' in extraDCData:
            creatorList.append(extraDCData['creator'])
    #Removes duplicates from the lists
    idList = list(dict.fromkeys(idList))
    createtimeList = list(dict.fromkeys(createtimeList))            
    unitnameList = list(dict.fromkeys(unitnameList))
    parentidList = list(dict.fromkeys(parentidList))
    restrictedList = list(dict.fromkeys(restrictedList))
    descriptionList = list(dict.fromkeys(descriptionList))
    coverageList = list(dict.fromkeys(coverageList))
    creatorList = list(dict.fromkeys(creatorList))
    
    #print(restrictedList)
    try:
        if len(unitnameList)==1:
            rootDC.update({'dc_creator':"{}".format(unitnameList[0])})
        else:
            rootDC.update({'dc_creator':"{}".format(unitnameList)})
        if(len(idList)>0):
            rootDC.update({'dc_description':"Contains IDs: {}".format(idList)})
        if(len(parentidList)>0):
            rootDC.update({'dc_relation':"Parent IDs: {}".format(parentidList)})
        if(len(createtimeList)>0):
            rootDC.update({'dc_coverage':"Temporal coverage {}-{}".format(min(createtimeList), max(createtimeList))})
        if len(restrictedList)>0:
            rootDC.update({'dc_rights':"Restrictions in ID(s): {}".format(restrictedList)})
        else:
            rootDC.update({'dc_rights':"NO restrictions"})
        if(len(descriptionList)>0):
            if "dc_description" in rootDC:
                existing = rootDC.get("dc_description")
                rootDC.update({"dc_description":"{}, {}".format(existing, descriptionList)})
            else:
                rootDC.update({"dc_description":"{}".format(descriptionList)})
        if(len(coverageList)>0):
            if "dc_coverage" in rootDC:
                existing = rootDC.get("dc_coverage")
                rootDC.update({"dc_coverage":"{}, {}".format(existing, coverageList)})
            else:
                rootDC.update({"dc_coverage":"{}".format(coverageList)})
    except:
        pass
    
    #print("item ids {}, creation times {}, unit names {} and parent ids {}".format(idList, createtimeList, unitnameList, parentidList))
    """       
