__author__ = 'simon'

__all__ = ['namegen']

class Storage:
    def __init__(self):
        self.contents = ''
        self.line = 0

    def store(self, buf):
        self.line = self.line + 1
        self.contents = "%s%s" % (self.contents,buf)

    def __str__(self):
        return self.contents