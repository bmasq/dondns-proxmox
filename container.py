from IPaddress import IPaddress
from configToDict import configToDict

class Container():

    configToDict = staticmethod(configToDict)
    
    def __init__(self, id, hostname, rawConfig) -> None:
        config = Container.configToDict(rawConfig)
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
