order = {'A': ['B', 'C'], 'B': ['D', 'E'], 'D': ['E', 'F'], 'F': ['X', 'Y']}
result = []

def add_to_list(item, add_before=None, key=None):
    if item not in result:
        if not add_before:
            result.insert(0, item)
            return
        if not key:
            for k,v in order.items():
                if item in v:
                   key=k
        indexs = []
        for x in add_before:
            if x in result:
               indexs.append(result.index(x))
        if indexs:
            result.insert(max(indexs), item)
        else:
            if key and result.index(key) is not None:
                result.insert(result.index(key), item)
            else:
                result.append(item)

def printServiceStartOrder():
    for key, value in order.items():
        add_to_list(key, add_before=value)
        for item in value:
            if item in order.keys():
                add_to_list(item, add_before=order[item], key=key)
            else:
                add_to_list(item, add_before=None)
    return result

print printServiceStartOrder()
