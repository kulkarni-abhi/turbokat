class Node():
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


class BinarySearchTree():
    def __init__(self):
        self.root = None

    def get_root(self):
        return self.root

    def insert(self, data):
        node = Node(data)
        if self.root is None:
            self.root = node
        else:
            root = self.root
            while root:
                if data < root.data:
                    #insert left
                    if root.left is None:
                        root.left = node
                        return
                    else:
                        root = root.left
                else:
                    #insert right
                    if root.right is None:
                        root.right = node
                        return
                    else:
                        root = root.right

    def delete(self, root, data):
        if root is None:
            return None
        if data < root.data:
            root.left = self.delete(root.left, data)
        elif data > root.data:
            root.right = self.delete(root.right, data)
        else:
            #delete node with one child
            if root.left is None:
                temp = root.right
                del root.left
                del root.right
                del root.data
                del root
                return temp
            elif root.right is None:
                temp = root.left
                del root.left
                del root.right
                del root.data
                del root
                return temp
            else:
                temp = self.get_successor(root.right)
                root.data = temp.data
                root.right = self.delete(root.right, temp.data)
        return root

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print root.data,
            self.inorder(root.right)

    def preorder(self, root):
        if root:
            print root.data,
            self.preorder(root.left)
            self.preorder(root.right)

    def postorder(self, root):
        if root:
            self.postorder(root.left)
            self.postorder(root.right)
            print root.data,

    def search(self, root, data):
        if root is None:
            return False
        if root.data == data:
            return True
        elif root.data < data:
            return self.search(root.right, data)
        elif root.data > data:
            return self.search(root.left, data)

    def size(self, root):
        if root is None:
            return 0
        return 1 + self.size(root.left) + self.size(root.right)

    def get_min(self, root):
        if root.left is None:
            return root.data
        else:
            return self.get_min(root.left)

    def get_max(self, root):
        if root.right is None:
            return root.data
        else:
            return self.get_max(root.right)

    def get_successor(self, node):
        current = node
        while current.left:
            current = current.left
        return current

mylist = [8,3,1,6,4,7,10,14,13]
mylist = [20,15,25,10,18,12,17,19,16]

tree = BinarySearchTree()
for xdata in mylist:
    tree.insert(xdata)

node = tree.get_root()
print node.data
print "\n"
tree.inorder(node)
print "\n"
tree.preorder(node)
print "\n"
tree.postorder(node)
print "\n"
print tree.search(node, 19)
print "\n"
print tree.size(node)
print "\n"
print tree.get_min(node)
print "\n"
print tree.get_max(node)

tree.delete(node, 15)
node = tree.get_root()
print tree.preorder(node)
