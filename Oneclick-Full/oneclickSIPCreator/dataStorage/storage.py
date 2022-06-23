'''
Created on Oct 6, 2021

@author: digitalia-aj
'''



class dataStorage:
    def __init__(self):
        self.Config = {}
        self.PayloadMetadataDict = {}
        self.Cookies = {}

    def storeConfig(self, content):
        self.Config = content
        print("stored config.ini data {}".format(self.Config))
        
        return
    
    def getCompleteConfig(self):
        return self.Config
    
    def getConfigItem(self, itemname):
        print("Getting {}".format(itemname))
        #print(self.Config)
        try:
            print("Get {} return -->{}".format(itemname, self.Config[itemname]))
            return self.Config[itemname]
        except:
            pass
        return 0
    
    
    def storePayloadMetadata(self, rootuuid4, metadata):
        self.PayloadMetadataDict[rootuuid4] = metadata
        print("Stored SIP {} metadata to a dictionary".format(rootuuid4))
        return 
    
    def getPayloadMetadata(self, rootuuid4):
        print("Getting file metadata for SIP id {}".format(rootuuid4))
        return self.PayloadMetadataDict[rootuuid4]
    
    def storeSessionCookie(self, cookie, rootuuid4):
        print("Storing cookie {} to rootuuid {}".format(cookie,rootuuid4))
        self.Cookies[rootuuid4] = cookie
        
    def getSessionCookie(self, rootuuid4):
        print("Getting session cookie for SIP id {}".format(rootuuid4))
        return self.Cookies[rootuuid4]
    
    