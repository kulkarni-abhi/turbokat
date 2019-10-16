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

    def get_height(self, root):
        if root is None:
            return 0

        leftHeight = self.get_height(root.left)
        rightHeight = self.get_height(root.right)

        if leftHeight < rightHeight:
            return rightHeight + 1
        else:
            return leftHeight + 1

    def get_node_count(self, node, current, level):
        if node is None:
            return 0

        if current == level:
            return 1

        return self.get_node_count(node.left, current + 1,
                                   level) + self.get_node_count(
                                       node.right, current + 1, level)

    def get_node_count_per_level(self, root):
        height = self.get_height(root)
        for i in range(height):
            print "Node count at level #{0} = {1}".format(
                i + 1, self.get_node_count(root, 0, i))

    def kth_smallest(self, root, k):
        self.count = 0
        self.result = 0

        def limited_inorder(root):
            if self.count < k:
                if root.left is not None:
                    limited_inorder(root.left)
                self.count += 1
                if self.count == k:
                    self.result = root.data
                    return
                if root.right is not None:
                    limited_inorder(root.right)
        if root is not None:
            limited_inorder(root)
        return self.result

    def kth_largest(self, root, k): 
        curr = root  
        Klargest = None
  
        # count variable to keep count  
        # of visited Nodes  
        count = 0
  
        while (curr != None): 
            # if right child is None  
            if (curr.right == None):  
                # first increment count and 
                # check if count = k 
                count += 1
                if (count == k):  
                    Klargest = curr  
  
                # otherwise move to the left child  
                curr = curr.left 
            else:  
                # find inorder successor of  
                # current Node  
                succ = curr.right  
                while (succ.left != None and succ.left != curr):  
                    succ = succ.left  
  
                if (succ.left == None):  
                    # set left child of successor  
                    # to the current Node  
                    succ.left = curr  

                    # move current to its right  
                    curr = curr.right 
  
                # restoring the tree back to   
                # original binary search tree 
                # removing threaded links  
                else: 
                    succ.left = None
                    count += 1
                    if (count == k):  
                        Klargest = curr  
  
                    # move current to its left child  
                    curr = curr.left 
        return Klargest 

mylist = [8, 3, 1, 6, 4, 7, 10, 14, 13]
mylist = [20, 15, 25, 10, 18, 12, 17, 19, 16]
mylist = [15, 10, 20, 8, 12, 18, 30, 16, 19]

tree = BinarySearchTree()
for xdata in mylist:
    tree.insert(xdata)

node = tree.get_root()
print "Root Node = {0}".format(node.data)

print "\nIn-order ==> ",
tree.inorder(node)

print "\n\nPre-order ==> ",
tree.preorder(node)

print "\n\nPost-order ==> ",
tree.postorder(node)

print "\n\nData {0} found = {1}".format(19, tree.search(node, 19))

print "\nSize of a Tree = {0}".format(tree.size(node))

print "\nSmallest Node = {0}".format(tree.get_min(node))

print "\nLargest Node = {0}".format(tree.get_max(node))

print "\nHeight of the Tree = {0}\n".format(tree.get_height(node))

tree.get_node_count_per_level(node)

print "\n3rd Smallest element = {0}".format(tree.kth_smallest(node, 3))

print "\n3rd Largest element = {0}".format(tree.kth_largest(node, 3).data)


print "\nDelete node with data 20"
tree.delete(node, 20)

node = tree.get_root()
print "\nNew root after delete node = {0}".format(node.data)

print "\nIn-order after delete node",
tree.inorder(node)

print "\n\nPre-order after delete node",
tree.preorder(node)

print "\n\nPost-order after delete node",
tree.postorder(node)
