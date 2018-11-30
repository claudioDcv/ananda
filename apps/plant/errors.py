class OwnerError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class GreenhouseSpaceNotExistError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ConstrainError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
