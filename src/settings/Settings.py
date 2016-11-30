import pickle
import os

class Settings:

    def __init__(self):
        #build settings module by readings from settings file
        currentPath = os.path.realpath(__file__)
        #find settings file and load settings dictionary
        with open(currentPath + "settings.p", "rb") as fp:
            data = pickle.load(fp)

        self.data = data

        self.minimum_split_size = data["minimum_split_size"]
        self.block_size = data["block_size"]
        self.rootPath = data["rootPath"]
        self.encryptedFolder = data["encryptedFolder"]
        self.remotePath = data["remotePath"]

    #static class to generate settings file
    def generateSettings(self, minimum_split_size, block_size, rootPath, encryptedFolder, remotePath):

        data = {'minimum_split_size': minimum_split_size, 'block_size': block_size, 'rootPath': rootPath, 'encryptedFolder': encryptedFolder, 'remotePath': remotePath}
        currentPath = os.path.realpath(__file__)
        with open(currentPath + 'settings.p', 'wb') as fp:
            pickle.dump(data, fp)