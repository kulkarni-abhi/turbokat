"""
Problem: 
	Write function to find all possible combinations of given coins that adds upto given sum.
"""
 
def get_change(amount, coins, change):
    if sum(change) == amount:
        yield change
    elif sum(change) > amount:
        pass
    elif coins == []:
        pass
    else:
        for c in get_change(amount, coins, change + [coins[0]]):
            yield c
        for c in get_change(amount, coins[1:], change):
            yield c

total = 100
denominations = [25, 50]

solutions = [s for s in get_change(total, denominations, [])]
i = 1
for s in solutions:
    print str(i) + " : " + str(s)
    i += 1

print 'optimal solution:', min(solutions, key=len)
