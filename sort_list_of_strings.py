"""
Give a list of strings.
Sort each string alphabetically and then sort the list too
"""

def xsort(string):
    charlist = list(string)
    for i in range(len(charlist)-1):
        for j in range(i+1, len(charlist)):
            if charlist[i] > charlist[j]:
                charlist[i], charlist[j] = charlist[j], charlist[i]
    return "".join(map(str,charlist))

def sort_list(strlist):
    for i in range(len(strlist)-1):
        for j in range(i+1,len(strlist)):
            str1 = xsort(strlist[i])
            str2 = xsort(strlist[j])
            if str1 > str2:
                strlist[i], strlist[j] = str2, str1
    return strlist

mylist = ["strings", "in", "python", "are", "immutable"]
new_list = sort_list(mylist)
print new_list
