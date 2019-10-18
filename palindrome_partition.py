
def checkPalindrome(string): 
	
	# Returns true if str is palindrome, 
	# else false 
	length = len(string) 
	length -= 1
	for i in range(length): 
		if string[i] != string[length]: 
			return False
		length -= 1
	return True

def filterValidPartitions(partitions, xstr):
    partition = partitions[0]
    for parts in partitions[1:]:
        if len(partition) > len(parts):
            if len(parts) == 1:
                if parts[0] == xstr:
                    continue
            if "".join(parts) != xstr:
                continue
            partition = parts
    if len(partition) == len(xstr):
        partition = list()
    return partition

def addPartitions(partitions, xstr, temp, index): 	
	length = len(xstr) 
	string = "" 

	current = temp[:] 

	if index == 0: 
		temp = [] 
	for i in range(index, length): 
		string += xstr[i] 
		if checkPalindrome(string): 
			temp.append(string) 
			if i + 1 < length: 
				addPartitions(partitions, xstr, temp[:], i + 1) 
			else: 
				partitions.append(temp) 
			temp = current

def partition(xstr, partitions): 
    temp = [] 
    addPartitions(partitions, xstr, temp[:], 0) 
    parts = filterValidPartitions(partitions, xstr)
    print("Total Partitions = {0}".format(len(parts)))


if __name__ == "__main__": 
	mystr = "aacbbcaa"
	parts = [] 
	partition(mystr, parts) 



