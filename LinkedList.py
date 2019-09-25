class Node():
    def __init__(self,data=None):
        self.data = data
        self.next = None

class LinkedList():
    def __init__(self):
        self.head = None

    def insert(self,data):
        new_node = Node(data)
        if self.head == None:
            self.head = new_node
            return 

        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def delete(self, key): 
          
        # Store head node 
        current = self.head 
  
        # If head node itself holds the key to be deleted 
        if (current is not None): 
            if (current.data == key): 
                self.head = current.next
                current = None
                return
  
        # Search for the key to be deleted, keep track of the 
        # previous node as we need to change 'prev.next' 
        prev = None
        while(current is not None): 
            if current.data == key: 
                break 
            prev = current 
            current = current.next 
  
        # if key was not present in linked list 
        if(current == None): 
            return 
  
        # Unlink the node from linked list 
        prev.next = current.next 
  
        current = None 

    def traverse(self):
        current = self.head
        while current:
            print current.data,
            current = current.next
        
    def reverse(self):
        current = self.head
        previous = None
        next = None

        while current:
            next = current.next
            current.next = previous
            previous = current
            current = next
        self.head = previous 

if __name__== "__main__":
    llist = LinkedList()
    for i in range(10):
        llist.insert(i)

    llist.traverse()
    print "\n"
    llist.reverse()
    llist.traverse()
    print "\n"
    llist.delete(4)
    llist.traverse()
