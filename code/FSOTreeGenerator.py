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
                    tree.addFile(file)
                elif(isinstance(file, FileSystemObject.Directory)):
                    tree.addFile(self.generateTree(file))
            return tree
            
        return tree

class TreeObject:
    
    def __init__(self, root):
        self.root = root
        self.children = []
        
    def getRoot(self):
        return self.root
        
    def getChildren(self):
        return self.children
        
    def addFile(self, file):
        self.children.append(file)

    def printTree(self):
        print("Tree:")
        if(isinstance(self.root, FileSystemObject.File)):
            print("File:")
            self.root.printFile()
        elif(isinstance(self.root, FileSystemObject.Directory)):
            print("Directory:")
            self.root.printDirectory()

FSOGenerator = FSOTreeGenerator()
FileOne = FileSystemObject.File("path1", True, False, False, "Today", "ePath")
FileTwo = FileSystemObject.File("path2", False, False, False, "Today", "ePath")
FileThree = FileSystemObject.File("path3", True, True, False, "Today", "ePath")
Files = [FileOne, FileTwo, FileThree]
AboveFiles = [FileSystemObject.Directory("path4", False, False, True, "Earlier", Files)]
TestDirectory = FileSystemObject.Directory("path5", False, False, True, "Earlier", AboveFiles)
Tree = FSOGenerator.generateTree(TestDirectory)
Tree.printTree()

