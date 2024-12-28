class YReader:
    def __init__(self):
        self.source = ""

        self.filename = "main.y"
        self.encoding = "utf-8"

    def read(self, filename: str = None, encoding: str = None):
        if filename:
            self.filename = filename

        if encoding:
            self.encoding = encoding

        with open(self.filename, "r", encoding=self.encoding) as file:
            self.source = file.read()

        return self.source

    def readlines(self, filename: str = None, encoding: str = None):
        if filename:
            self.filename = filename

        if encoding:
            self.encoding = encoding

        with open(self.filename, "r", encoding=self.encoding) as file:
            self.source = file.readlines()
            
        return self.source