import json
import os
import ubinascii

class jsonHandler():

    def getFile(self,file):
        with open(f'{file}', 'r') as jsonFile:
            data = json.load(jsonFile)
            return data
        
    def OverwriteJsonFile(self, filePath, data):
        with open(filePath, 'w') as file:
            json.dump(data, file)
            

    def HashHandler(self,hash,root=None):

        if root is not None:
            jsonString = {root:hash}
            self.OverwriteJsonFile("configMeta.json",jsonString)
        return ubinascii.a2b_base64(hash).decode().split("/%20/")



