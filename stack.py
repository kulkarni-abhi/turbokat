"""
Author: Abhishek Kulkarni
"""

class stack():
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self,data):
        self.items.append(data)

    def pop(self):
        return self.items.pop()

    def display(self):
        for item in self.items:
            print item,
        print "\n"

stk = stack()
for i in range(10):
    stk.push(i)

stk.display()
if not stk.isEmpty():
    print "Popped %d\n" % stk.pop()
stk.display()
