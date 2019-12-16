def printServiceStartOrder(deps):
    xdict = dict((key, set(deps[key])) for key in deps)
    result = list()
    
    while xdict:
        #values not in keys (items without dependencies)
        element = set(item for val in xdict.values() for item in val) - set(xdict.keys())
        
        #Keys without value (items without dependencies)
        element.update(member for member, val in xdict.items() if not val)

        #can be added right away
        result.append(element)

        #cleanup traces from other lists
        xdict = dict(((member, val-element) for member, val in xdict.items() if val))
    return result

dict1 = dict(
    A=('B', 'C'),
    B=('D', 'E', 'G'),
    D=('E', 'F'),
    F=('X', 'Y')
)

print printServiceStartOrder(dict1)
