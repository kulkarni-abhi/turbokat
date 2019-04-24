"""
Author: Abhishek Kulkarni
"""

class Queue():
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self,data):
        self.items.append(data)

    def pop(self):
        return self.items.pop(0)

    def display(self):
        for item in self.items:
            print item,
        print "\n"

q = Queue()
for i in range(10):
    q.push(i)

q.display()
if not q.isEmpty():
    print "Popped %d\n" % q.pop()
q.display()
