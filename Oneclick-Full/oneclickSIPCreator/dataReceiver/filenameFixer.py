'''
Created on Jan 17, 2022

@author: digitalia-aj
'''
import os
import shutil
import re

def checkAndFixFileNames(inputName):
    if os.path.isfile(inputName):
        print("It is a file")
        orgfilename = os.path.basename(inputName)
        newfilename = str(orgfilename).strip().replace(' ', '_')
        newfilename = re.sub(r'(?u)[^-\w.]', '', newfilename)
        print(newfilename)
        newFullPath = os.path.join(os.path.dirname(inputName),newfilename)
                
        shutil.move(inputName, newFullPath)
        #fullpath = os.path.join(newPath, os.path.basename(originalPath))
        return newFullPath
    elif os.path.isdir(inputName):        
        for root, dirs, files in os.walk(inputName):
            for file in files:    
                newfilename = str(file).strip().replace(' ', '_')
                newfilename = re.sub(r'(?u)[^-\w.]', '', newfilename)
                if str(file)!=str(newfilename):
                    shutil.move(os.path.join(root,file), os.path.join(root,newfilename))
        return inputName #The path name is not changed, just filenames so return the original
    
    else:
        #should newer happen but just in case return the original path
        return inputName
        
    