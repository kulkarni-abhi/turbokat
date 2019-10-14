def firstDuplicate(a):
    index = len(a) + 1
    for index1,value1 in enumerate(a[:-1]):
        b = a[index1+1:]
        if value1 in b:
            index2 = b.index(value1)
            if index2+1 < index:
                index = index2+1
    
    if index == len(a) + 1:
        return -1
    return a[index]

def firstDuplicate1(a):
    set_ = set()
    for item in a:
        if item in set_:
            return item
        set_.add(item)
    return None

c = [2, 1, 3, 5, 3, 2]
print firstDuplicate1(c)
