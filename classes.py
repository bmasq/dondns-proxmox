from IPaddress import IPaddress

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

class Container():
    
    def __init__(self, id, hostname, rawConfig) -> None:
        config = configToDict(rawConfig)
        self._id = id
        self._hostname = hostname
        self._ip = IPaddress(config["net0"]["ip"])

    @property
    def id(self):
        return self._id
    
    @property
    def hostname(self):
        return self._hostname

    @property
    def ip(self):
        return self._ip.address
