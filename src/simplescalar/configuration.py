from os import path as ospath

class Configuration:
    def __init__(self, options=[]):
        for name, value in options:
            if name == "-config" and not ospath.exists(value):
                raise FileNotFoundError("Could not find config file '%s'" % value)

        self.options = options
