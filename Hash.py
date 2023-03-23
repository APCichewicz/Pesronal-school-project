class Hash:
    # set up the underlying array architecture. it is done this way so that it can easily scale by changing
    # the hash_value
    def __init__(self):
        self.hash_value = 83
        self.arr = [None] * self.hash_value

    # make a simple hash value from a given key by converting it to a string,
    # then performing transformation operations upon each character of said string.
    # then finally apply the modulo operator to ensure the value returned is within
    # the bounds of our underlying array indexes.
    def __make_hash(self, key):
        key = str(key)
        temp = self.hash_value
        for c in key:
            temp = ((temp << 5) + temp) + ord(c)
        return temp % self.hash_value

    # get the hash value of the key and check that index in the underlying array. if it is not filled,
    # fill it with a nested array. this is done for chaining purposes to handle collisions. if there is a value there,
    # check if the keys match. if they match, update the value. if they dont there is a collission
    # and we append the value to the end of the chain.
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

    # hash the provided key and check the corresponding array index. if that index is empty, return none.
    # else iterate over the stored chain until the index is found. return the found entry or none if not found.
    def get(self, key):
        hashed = self.__make_hash(key)
        if self.arr[hashed] is None:
            return None
        for entry in self.arr[hashed]:
            if entry[0] == key:
                return entry
        return None

    #hash the provided key and check the corresponding array index. if nothing is there, return false.
    # else iterate over the chain until the entry is found. if it is found, pop that index.
    # then if the array is empty, set that index value to none. if the key is not found, return false.
    def remove(self, key):
        hashed = self.__make_hash(key)
        if self.arr[hashed] is None:
            return False
        for i, entry in enumerate(self.arr[hashed]):
            if entry[0] == key:
                self.arr[hashed].pop(i)
                if not self.arr[hashed]:
                    self.arr[hashed] = None
                return True
        return False

    # iterate over the underlying array and return all keys
    def keys(self):
        result = []
        for entry in self.arr:
            if entry is not None:
                for key in entry:
                    result.append(key[0])
        return result

    # iterate over the underlying array and return all values
    def values(self):
        result = []
        for entry in self.arr:
            if entry is not None:
                for value in entry:
                    result.append(value[1])
        return result
