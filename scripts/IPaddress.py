class IPaddress():

    # receives a string in CIDR format
    def __init__(self, cidr) -> None:
        ipMask = cidr.split('/')
        self.address = ipMask[0]
        self.mask = ipMask[1]