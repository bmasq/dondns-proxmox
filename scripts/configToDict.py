# Receives the output of pct config
def configToDict(string):
    # split the input string by newline characters to get a list of lines
    lines = string.strip().split('\n')
    data = dict()
    for line in lines:
        # split the line by the leftmost colon character to separate the key and value
        key, value = line.split(':', 1)
        # nested dictionary
        if '=' in value:
            valueDict = dict()
            element = value.split(',')
            for item in element:
                keyVal = item.split('=')
                try:
                    valueDict[keyVal[0].strip()] = keyVal[1].strip()
                # if the item does not have a '=', the key will be its index
                except IndexError:
                    valueDict[element.index(item)] = keyVal[0]
            value = valueDict
        data[key.strip()] = value
    return data