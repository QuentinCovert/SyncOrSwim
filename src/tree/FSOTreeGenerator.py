import types
import FileSystemObject

class FSOTreeGenerator:
    
    def generateTree(self, root):
        tree = TreeObject(root)
        
        if(isinstance(root, FileSystemObject.File)):
            return tree
            
        elif(isinstance(root, FileSystemObject.Directory)):
            for file in root:
                if(isinstance(file, FileSystemObject.File)):
                    tree.children.append(file)
                elif(isinstance(file, FileSystemObject.Directory)):
                    subTree = self.generateTree(file)
                    tree.children.append(subTree)
            return tree
            
        return tree

class TreeObject:
    #The TreeObject holds files and directories. It's root can be a file or a directory, but its children can only be files or other TreeObjects.
    #Use the FSOTreeGenerator.generateTree method to create proper TreeObjects. Otherwise functionality is not guaranteed to work.
    def __init__(self, root):
        self.root = root
        self.children = []
        
    def getRoot(self):
        return self.root
        
    def getChildren(self):
        return self.children
        
    #Adds the given file to the given directory (represented as a TreeObject) in the tree that calls it.
    def addFileToDirectory(self, file, directory):
        if(self.root == directory):
            self.addFile(file)
            return
        for child in self.children:
            if(child == directory):
                directory.addFile()
            elif(isinstance(child, TreeObject)):
                bool = child.findChild(directory)
                if(bool != False):
                    child.addFileToDirectory(file, directory)
                

    #Returns the given child if it is found. False otherwise.
    def findChild(self, child):
        root = self.getRoot()
        if(child == root):
            return root
        else:
            children = self.getChildren()
            for kid in children:
                if(kid == child):
                    return kid
                elif(isinstance(kid, TreeObject)):
                    recSearchValue = kid.findChild(child)
                    if(recSearchValue == False):
                        temp = "Do Nothing"
                    elif(recSearchValue == child):
                        return recSearchValue
                elif(isinstance(kid, FileSystemObject.File)):
                    if(child == kid):
                        return kid
        return False
        
    #Finds and returns the child which has the given filepath. False if it cannot be found.
    def findChildByFilepath(self, path):
        rootPath = self.getRoot().getPath()
        if(path == rootPath):
            return self.getRoot()
        else:
            children = self.getChildren()
            for kid in children:
                if(isinstance(kid, TreeObject)):
                    kidPath = kid.getRoot().getPath()
                    if(kidPath == path):
                        return kid.getRoot()
                    else:
                        recSearchValue = kid.findChildByFilepath(path)
                        if(recSearchValue != False):
                            return recSearchValue
                elif(isinstance(kid, FileSystemObject.File)):
                    kidPath = kid.getPath()
                    if(kidPath == path):
                        return kid
        return False
        
    def removeChildByFilepath(self, path):
        self.removeChild(self.findChildByFilepath(path))
    
    def removeChild(self, child):
        root = self.getRoot()
        if(child == root):
            self.root = None
            self.children = None
        else:
            children = self.getChildren()
            for kid in children:
                if(isinstance(kid, TreeObject)):
                    kidRoot = kid.getRoot()
                    if(kidRoot == child):
                        children.remove(kid)
                        return True
                    else:
                        recValue = kid.removeChild(child)
                        if(recValue == True):
                            return True
                elif(isinstance(kid, FileSystemObject.File)):
                    if(kid.getPath() == child.getPath()):
                        children.remove(kid)
                        return True
        return False
        
    
    #Adds the given file to the topmost level of the tree that calls it.
    def addFile(self, file):
        if(isinstance(self.root, FileSystemObject.File)):
            return False
        else:
            self.getRoot().addFile(file)
            if(isinstance(file, FileSystemObject.File)):
                self.children.append(file)
            else:
                FSOGenerator = FSOTreeGenerator()
                subTree = FSOGenerator.generateTree(file)
                self.children.append(subTree)
            return True
            
        return False
        
    def printTree(self):
        if(isinstance(self.root, FileSystemObject.File)):
            print("File:")
            self.root.printFile()
        elif(isinstance(self.root, FileSystemObject.Directory)):
            self.root.printDirectoryNoChildren()
            for kid in self.getChildren():
                if(isinstance(kid, FileSystemObject.File)):
                    kid.printFile()
                elif(isinstance(kid, TreeObject)):
                    kid.printTree()