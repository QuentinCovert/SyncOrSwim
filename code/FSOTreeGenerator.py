import types
import FileSystemObject.py

class FSOTreeGenerator():
    def __init__(self):
        
    def generateTree(self, root):
        tree = TreeObject();
        
        if(root.isInstance(File)):
            return root
            
        else if(root.isInstance(Directory)):
            for(file in root.files):
                if(file.isInstance(File)):
                    tree.addFile(file)
                else if(file.isInstance(Directory)):
                    innerTree = generateTree(file)
                    tree.addFile(innerTree)
            return tree
            
        else:
            return false
            
class TreeObject():
    def __init__(self):
        self.files = []
    
    def addFile(file):
        files.append(file)