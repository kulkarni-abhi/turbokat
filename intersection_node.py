from LinkedList import LinkedList

"""
A program to find intersection node of two singly linked lists


list1:	4 ---> 8 ---> 15
                        \ 
                         42 ---> 99
                        /
list2:        16 ---> 23

Intersection Point = 42
"""

def get_length(head):
    current = head
    cnt = 0
    while current:
        cnt += 1
        current = current.next
    return cnt

def find_intersection_node(head1,head2):
    len1 = get_length(head1)
    len2 = get_length(head2)

    if len1 < len2:
        head1,head2 = head2,head1
        len1,len2 = len2,len1

    diff = len1 - len2

    for i in range(diff):
        head1 = head1.next

    while  head1 and head2:
        if  head1.data == head2.data and \
            id(head1.data) == id(head2.data):
            """
            Check if data and memory location of both the values are same.
            """
            return head1.data
        head1 = head1.next
        head2 = head2.next

list1 = LinkedList()
list2 = LinkedList()

for i in [4,8,15,42,99]:
    list1.insert(i)

for i in [16,23,42,99]:
    list2.insert(i)

node = find_intersection_node(list1.head,list2.head)
print "\nIntersection node of two linked list :-"
print "\tData = {0}".format(node)
print "\tMemory Location = {0}\n".format(hex(id(node))) 
