def generate_permutations(A):
    if len(A) <= 1:
        return [A]
    first = A[-1]
    result = generate_permutations(A[:-1])
    permutations = []
    for p in result:
        for i in range(len(A)):
            left = p[:i]
            right = p[i:]
            permutations.append(left + [first] + right)
    return permutations

xList = [3,1,5,6]
result =generate_permutations(xList)

for entry in result:
    print entry

