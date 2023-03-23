class Hash:
    def __init__(self):
        self.hash_value = 83
        self.arr = [None] * self.hash_value

    def __make_hash(self, key):
        key = str(key)
        temp = self.hash_value
        for c in key:
            temp = ((temp << 5) + temp) + ord(c)
        return temp % self.hash_value

    def set(self, key, value):
        hashed = self.__make_hash(key)
        if self.arr[hashed] is None:
            self.arr[hashed] = [[key, value]]
        else:
            for item in self.arr[hashed]:
                if item[0] == key:
                    item[1] = value
                    return
            self.arr[hashed].append([key, value])

    def get(self, key):
        hashed = self.__make_hash(key)
        if self.arr[hashed] is None:
            return None
        for entry in self.arr[hashed]:
            if entry[0] == key:
                return entry
    def remove(self, key):
        hashed = self.__make_hash(key)
        if self.arr[hashed] is None:
            return False
        for i, entry in enumerate(self.arr[hashed]):
            if entry[0] == key:
                self.arr[hashed][i] = None
                if self.arr[hashed] == [None]:
                    self.arr[hashed] = None
                return True
        return False
    def keys(self):
        result = []
        for entry in self.arr:
            if entry is not None:
                for key in entry:
                    result.append(key[0])
        return result

    def values(self):
        result = []
        for entry in self.arr:
            if entry is not None:
                for value in entry:
                    result.append(value[1])
        return result
