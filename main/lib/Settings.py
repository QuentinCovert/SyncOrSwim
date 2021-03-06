import pickle
import os

class Settings:

    def __init__(self, resourcePath):
        #build settings module by readings from settings file
        currentPath = resourcePath
        #find settings file and load settings dictionary
        with open(currentPath + "settings.p", "rb") as fp:
            data = pickle.load(fp)

        self.data = data

        self.rootPath = data["rootPath"]
        self.encryptedFolder = data["encryptedFolder"]
        self.remotePath = data["remotePath"]

        #init global settings
        with open(currentPath + "global_settings.p", "rb") as fp:
            global_data = pickle.load(fp)

        self.global_data = global_data

        self.minimum_split_size = global_data["minimum_split_size"]
        self.block_size = global_data["block_size"]
        self.key = global_data["key"]


    #static class to generate settings file
    def generateLocalSettings(resourcePath, rootPath, encryptedFolder, remotePath):

        data = {'rootPath': rootPath, 'encryptedFolder': encryptedFolder, 'remotePath': remotePath}
        currentPath = resourcePath
        with open(currentPath + 'settings.p', 'wb') as fp:
            pickle.dump(data, fp)

    def generateGlobalSettings(resourcePath, minimum_split_size, block_size, key):

        global_data = {'minimum_split_size': minimum_split_size, 'block_size': block_size, 'key': key}
        currentPath = resourcePath
        with open(currentPath + 'global_settings.p', 'wb') as fp:
            pickle.dump(global_data, fp)
