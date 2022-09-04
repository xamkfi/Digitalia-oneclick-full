'''
Created on Oct 19, 2021

@author: digitalia-aj
'''
from  exiftool import ExifToolHelper
import hashlib
import json
import os
import subprocess
import multiprocessing
import pytz
from datetime import datetime
import mimetypes
from multiprocessing import Pool
from IDCreator import shaCalculator, uuidCreator
from dataReceiver import receiver
from _datetime import date
#from exiftool.ExifToolHelper import 

class readMeta:
    def __init__(self):
        self.allFilesMetadata = {}
        self.tikaPath = "/home/software/tika-app-2.1.0.jar"
    
    def useTikaToReadMeta(self, onePath):
        metaProcess = subprocess.Popen(["java", "-jar", self.tikaPath, "-j", onePath], stdout=subprocess.PIPE)
        result, err = metaProcess.communicate()
        if(metaProcess.returncode == 0):            
            tempDict = json.loads(result)
        else:
            print("Error: {}".format(err))   
        return tempDict
    
    
    def useExifToReadMeta(self, onePath):
        #print("Get metadata with exiftool for {} ".format(onePath))
        
        try: #Needed thus exiftool cannot find metadata for all the files
            with ExifToolHelper() as et:
                #print(et.get_metadata(onePath))
                tempDict = et.get_metadata(onePath)[0]
        except:
            tempDict = {}
            #print(os.stat(onePath))
            #As a backup plan gets the size and creation time "manually"
            tempDict["File:FileSize"] = os.path.getsize(onePath)
            tempDict["File:FileModifyDate"]=str(datetime.now()).replace("-",":")
            #isodate = timestamp.isoformat()
            #print("{}".format(timestamp))
            #tempDict["File:FileModifyDate"] = isodate 
            pass
        print("Exifmeta for {} is {}".format(onePath, tempDict))
        
        return tempDict
    
    def fastFixExifDate(self, tobeFixed):
        #exifdates look like 2021:12:10 12:33:26+02:00, replace the fist space
        #Iso dates look like 2021-11-25T11:09:31+01:00        
        fixed = str(tobeFixed).replace(" ", "T", 1).replace(":", "-", 2)
        fixed = fixed.split(".")[0] #In case there's milliseconds 
        print("Before date fix {} and after {}".format(tobeFixed, fixed))
        return fixed
    
    def multiProcessMetadataReader(self, onePath, dataPath): 
        relPath = os.path.relpath(onePath, dataPath)
        tempDict = self.useExifToReadMeta(onePath)
        #print("{}--{}".format(relPath, tempDict))
        if(len(tempDict)==0):
            print("No metadata for {}".format(onePath))
        metaDict = {}
        replaceMimes = ["", "image/x-canon-cr2", "application/vnd.ms-pki.seccat"]
        """Replaces all : with _"""
        for key in tempDict:
        #print("repmets for root: {}-->{}".format("repmets_"+key, temprepMETSMeta[key]))        
        #if key in metsrepMETSValues:           
            
            if "Date" in key:
                tempDict[key] = self.fastFixExifDate(tempDict[key]) 
            
            metaDict.update({str(key).replace(':', '_').replace('-','_'):tempDict[key]}) 
            
                
         
        #Lets check if we are evaluating created dc.xml or repmets.xml file, if so do some naming
        tempDict.clear() #Not needed thus data is copied to metaDict dictionary
        #This part calculates sha256 for the file        
        metaDict['sha256'] = shaCalculator.calculateSHA256(onePath) #Calls sha generator         
        fileid = uuidCreator.getuuid4()
        metaDict['fileID'] = fileid
        #This part adds the last modified time to metadata thus Tika seems to be unable to get that info
        metaDict['relativePath'] = str(relPath)
        #print("After -->{}".format(metaDict))
        
        if 'ExifTool_Error' in metaDict:
            #print("Exiftool error {}".format(onePath))
            metaDict['File_MIMEType'] = "application/octet-stream"
            #print(metaDict)
        guessedMime = mimetypes.guess_type(onePath, True)
        #print("XXXXXXXXX, {}".format(guessedMime))
        
        if "File_MIMEType" not in metaDict:
            metaDict['File_MIMEType'] = guessedMime[0]
        
        #print("Exif MIME {} vs guessed MIME {}".format(metaDict['File_MIMEType'], guessedMime))
        
        if metaDict['File_MIMEType'] in replaceMimes:
            #print("Replacing {} mimetype with a generic application/octet-stream".format(metaDict['File_MIMEType']))
            metaDict['File_MIMEType'] = "application/octet-stream"
        
        #temptime =  (os.stat(onePath)).st_mtime
        #temptime1 = str(datetime.datetime.fromtimestamp(temptime).isoformat()).split('.')[0]
        #tempDict['fileCreated'] = temptime1         
        #print("{}*******************************-->metat {}".format(onePath, metaDict))
        return [onePath, metaDict]
        
    
    def multiProcessResults(self, resultArray):
        #print("Got metadata for {} --> {}".format(resultArray[0], resultArray[1]))
        self.allFilesMetadata[resultArray[0]] = resultArray[1] 
        print("Metadata array lenght is now {}".format(len(self.allFilesMetadata)))
        return
    
    def getMetadataForFileList(self, filePathsList, dataPath):        
        self.allFilesMetadata = {}        
        poolCount = len(filePathsList)
        poolMaxCount = multiprocessing.cpu_count()-1
        poolCount = min(poolCount, poolMaxCount)    
        metadataPool = Pool(poolCount)
        print("Getting metadata for {} files".format(len(filePathsList)))
        result_objs = []
        for onePath in filePathsList:
            #metadataPool.apply_async(self.multiProcessMetadataReader, args=(onePath, dataPath), callback=self.multiProcessResults)
            result = metadataPool.apply_async(self.multiProcessMetadataReader, args=(onePath, dataPath)) 
            #print(result)
            result_objs.append(result)
        print(len(result_objs))
        
        results = [result.get() for result in result_objs]
        metadataPool.close()
        metadataPool.join()    
        print("Returned metadata for {} files".format(len(results)))
        for oneresult in results:
            self.allFilesMetadata[oneresult[0]] = oneresult[1]
        ##self.allFilesMetadata[results[0]] = resultArray[1] 
        
        #print(self.allFilesMetadata)
        return self.allFilesMetadata
