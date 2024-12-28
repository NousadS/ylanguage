class YWriter:
    def __init__(self):
        self.filename = "main.oy"
        self.encoding = "utf-8"

    def write(self, filename: str, encoding: str, code: str):
        if filename:
            self.filename = filename

        if encoding:
            self.encoding = encoding

        with open(self.filename, "w", encoding=self.encoding) as file:
            file.write(code)

        return self