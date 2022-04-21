'''
Created on Oct 6, 2021

@author: digitalia-aj
'''
import configparser
import time
import timeit
import os
#import dataStorage
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from dataReceiver import receiver
from dataStorage import storage
#from _testcapi import instancemethod

uploadDir = "/home/notdefined/sampledir" #This one is monitored if no path is defined in config.ini file
completeddir = "/home/notdefined/sampledir" #Completed SIPs go here if no path is defined in config.ini file


class Watcher:
    def __init__(self, directory=".", handler=FileSystemEventHandler()):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory        

    def run(self):
        self.observer.schedule(self.handler, self.directory, recursive=False)
            
        self.observer.start()
        print("\nWatcher Running in {}/\n".format(self.directory))
        try:
            while True:
                time.sleep(2)
        except:
            self.observer.stop()
        self.observer.join()
        print("\nWatcher Terminated\n")


class HandleUploads(FileSystemEventHandler):
   
    def on_created(self, event):
        """
        <DirCreatedEvent: event_type=created, src_path='/home/digitalia-aj/extraspace/oneclick-rawdata/compressed/test', is_directory=True>
        <FileCreatedEvent: event_type=created, src_path='/home/digitalia-aj/extraspace/oneclick-rawdata/compressed/sample.txt', is_directory=False>
        """        
        start = timeit.default_timer()
        receiver.handleCreationEvent(event, instantedStorage)
        stop = timeit.default_timer()
        print("Process completed in {}s, waiting for next one".format(round(stop-start, 2)))
    """
    def on_any_event(self, event):
        print("{}".format(event))
    """
        
        
if __name__ == '__main__':
    #Seeks ini config file from the main app dir
    mainpath = os.getcwd()
    dircontent = os.listdir(mainpath)
    configFile = ""
    instantedStorage = storage.dataStorage()
    for onefile in dircontent:
        if onefile.endswith(".ini"):            
            configFile = os.path.join(mainpath, onefile)
            break
    if configFile !="":
        print("Found configfile - {}, use values from it".format(configFile))    
        config = configparser.ConfigParser()
        config.read(configFile, encoding='utf8')
        sections = config.sections()
        tempConfigs = {}
        for onesection in sections:            
            #print("All confs {}".format(config.items(onesection)))
            for temp in config.items(onesection):
                tempConfigs[temp[0]] = temp[1]
        
        instantedStorage.storeConfig(tempConfigs)
        #print(tempConfigs)
        uploadDir = instantedStorage.getConfigItem("uploaddir")
        
    #dataPath = "/home/digitalia-aj/extraspace/oneclick-rawdata/compressed/digitaliastore.WordPress.2021-09-21.tar.xz"
    if (uploadDir != 0):
        uploadWatcher = Watcher(uploadDir, HandleUploads())
        uploadWatcher.run()
    else:
        print("Something strange in defined upload dir, please check the config.ini file")
    
    pass
