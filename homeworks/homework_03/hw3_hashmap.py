#!/usr/bin/env python
# coding: utf-8


class HashMap:
    class Entry:
        def __init__(self, key, value):
            self.key = key
            self.value = value

        def get_key(self):
            return self.key

        def get_value(self):
            return self.value

        def __eq__(self, other):
            return self.key == other.key

    def __init__(self, bucket_num=64):
        self.__buckets = [None]*bucket_num
        self.__size = bucket_num
        self.__el_num = 0

    def get(self, key, default_value=None):
        index = self._get_index(self._get_hash(key))
        if self.__buckets[index] is not None:
            for item in self.__buckets[index]:
                if item.get_key() == key:
                    return item.get_value()
        return default_value

    def put(self, key, value):
        index = self._get_index(self._get_hash(key))
        if self.__buckets[index] is not None:
            for item in self.__buckets[index]:
                if item.get_key() == key:
                    item.value = value
                    return

        self.__el_num += 1
        if self.__buckets[index] is None:
            self.__buckets[index] = [self.Entry(key, value)]
            if not(None in self.__buckets):
                self._resize()
            return
        self.__buckets[index].append(self.Entry(key, value))

    def __len__(self):
        return self.__el_num

    @staticmethod
    def _get_hash(key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % len(self.__buckets)

    def values(self):
        return (item.value for el in self.__buckets if el is not None for item in el)

    def keys(self):
        return (item.key for el in self.__buckets if el is not None
                for item in el)

    def items(self):
        return ((item.key, item.value) for el in self.__buckets if el is not None
                for item in el)

    def _resize(self):
        self.__el_num = 0
        items = self.items()
        self.__size *= 2
        self.__buckets = [None]*self.__size
        for item in items:
            self.put(item[0], item[1])

    def __str__(self):
        res = 'buckets: {'
        for item in self.__buckets:
            res += '(' + str(item) + ')'
        res += '} '
        res += 'items: {'
        for item in self.items():
            res += str(item)
        res += '}'
        return res

    def __contains__(self, item):
        index = self._get_index(self._get_hash(item))
        if self.__buckets[index] is not None:
            for el in self.__buckets[index]:
                if el.get_key() == item:
                    return True
        return False
