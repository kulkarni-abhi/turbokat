"""
Author: Abhishek Kulkarni

Program to remove all zeros from the list. 
"""

alist = [1,0,1,0,2,3,0,0,1,0,3,4,0,0,0,1]

alen = len(alist)
i=0

while i < alen:
    if alist[i] == 0:
        alen -= 1
        del alist[i]
        continue
    i+=1

print alist
