def rotateImage(a):
    a.reverse()
    transpose = [ [row[i] for row in a] for i in range(len(a[0]))]
    return transpose

matrix = [ [1,2,3],[4,5,6],[7,8,9] ]
print rotateImage(matrix)
