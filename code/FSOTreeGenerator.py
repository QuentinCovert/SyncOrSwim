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

FSOGenerator = FSOTreeGenerator()
FileOne = FileSystemObject.File("path1", True, False, False, "Today", "ePath")
FileTwo = FileSystemObject.File("path2", False, False, False, "Today", "ePath")
FileThree = FileSystemObject.File("path3", True, True, False, "Today", "ePath")
Files = [FileOne, FileTwo]
InnerDirectory = FileSystemObject.Directory("path4", False, False, True, "Earlier", Files)
AboveFiles = [FileThree, InnerDirectory]
TestDirectory = FileSystemObject.Directory("path5", False, False, True, "Earlier", AboveFiles)
Tree = FSOGenerator.generateTree(TestDirectory)
Tree.printTree()
print("")
Tree.addFileToDirectory(FileThree, InnerDirectory)
Tree.printTree()
