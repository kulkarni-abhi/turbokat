arr = [2,1,4,5]

total = 0
all = []
for i in range(len(arr)):
    temp = [arr[i]]
    total += sum(temp[:])
    all.append(temp[:])
    for j in range(i+1, len(arr)):
        temp.append(arr[j])
        total += sum(temp[:])
        all.append(temp[:])
print  total
