def xsort(string):
    charlist = list(string)
    for i in range(len(charlist)-1):
        for j in range(i+1, len(charlist)):
            if charlist[i] > charlist[j]:
                charlist[i], charlist[j] = charlist[j], charlist[i]
    return "".join(map(str,charlist))

print xsort("zyx")
