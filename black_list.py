class BlackList:
    def __init__(self):
        self.data = list()

    def set(self, item):
        self.data.append(item)

    def remove(self, item):
        if item in self.data:
            self.data.remove(item)
        else:
            return False

    def __contains__(self, item):
        return item in self.data
