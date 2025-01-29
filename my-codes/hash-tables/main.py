from collections.abc import MutableMapping
from random import randrange


class MapBase(MutableMapping):
    """Our own abstract base class that includes a nonpublic item class"""

    class _item:
        """Lightweight composite to store key-value pairs as map items"""

        __slots__ = "_key", "_value"

        def __init__(self, key, value) -> None:
            self._key = key
            self._value = value

        def __eq__(self, other) -> bool:
            return self._key == other._key

        def __lt__(self, other) -> bool:
            return self._key < other._key

        def __ne__(self, other) -> bool:
            return not (self == other)


class UnsortedTableMap(MapBase):
    def __init__(self) -> None:
        self._table = []

    def __getitem__(self, key):
        """Return value associated with key or raise KeyError if not found"""
        for item in self._table:
            if key == item._key:
                return item._value
        raise KeyError("Key Error: " + repr(key))

    def ___setitem__(self, key, value):
        for item in self._table:
            if key == item._key:
                item._value = value
                return
        self._table.append(self._item(key, value))

    def __delitem__(self, key):
        for j in range(len(self._table)):
            if key == self._table[j]._key:
                self._table.pop(j)
                return
        raise KeyError("Key Error: " + repr(key))

    def __len__(self):
        return len(self._table)

    def __iter__(self):
        for item in self._table:
            yield item._key


class HashMapBase(MapBase):
    def __init__(self, cap=11, p=109345121) -> None:
        """Create an empty hash-table map"""

        self._table = cap * [None]
        self._n = 0
        self._prime = p
        self._scale = 1 + randrange(p - 1)
        self._shift = randrange(p)

    def _hash_function(self, k):
        return (hash(k) * self._scale + self._shift) % self._prime % len(self._table)

    def __len__(self):
        return self._n

    def __getitem__(self, k):
        j = self._hash_function(k)
        return self._bucket_getitem(j, k)

    def __setitem__(self, k, v):
        j = self._hash_function(k)
        self._bucket_setitem(j, k, v)
        if self._n > len(self._table) // 2:
            self._resize(2 * len(self._table) - 1)

    def __delitem__(self, k):
        j = self._hash_function(k)
        self._bucket_delitem(j, k)
        self._n -= 1

    def _resize(self, c):
        old = list(self.items())
        self._table = c * [None]
        self._n = 0

        for k, v in old:
            self[k] = v


class ChainHashMap(HashMapBase):
    """Hash map implemented with separate chaining of collision resolution"""

    def _bucket_getitem(self, j, k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError("Key Error " + repr(k))

        return bucket[k]

    def _bucket_setitem(self, j, k, v):
        if self._table[j] is None:
            self._table[j] = UnsortedTableMap()
        oldsize = len(self._table[j])
        self._table[j][k] = v
        if len(self._table[j]) > oldsize:
            self._n += 1

    def _bucket_delitem(self, j, k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError("Key Error" + repr(k))
        del bucket[k]

    def __iter__(self):
        for bucket in self._table:
            if bucket is not None:
                for key in bucket:
                    yield key


class ProbeHashMap(HashMapBase):
    _AVAIL = object()

    def _is_available(self, j):
        return self._table[j] is None or self._table[j] is ProbeHashMap._AVAIL

    def _find_slot(self, j, k):
        """Search for key k in bucket at index j.

        Return (success index) tuple described as follows:
        if match was found sucess is True and index denotes its locations.
        if no match found success if False and index denotes first available slot.
        """

        firstAvail = None
        while True:
            if self._is_available(j):
                if firstAvail is None:
                    firstAvail = j
                if self._table[j] is None:
                    return (False, firstAvail)
            elif k == self._table[j]._key:
                return (True, j)
            j = (j + 1) % len(self._table)

    def _bucket_getitem(self, j, k):
        found, s = self._find_slot(j, k)
        if not found:
            raise KeyError("Key Error: " + repr(k))
        return self._table[s]._value

    def _bucket_setitem(self, j, k, v):
        found, s = self._find_slot(j, k)
        if not found:
            self._table[s] = self._item(k, v)
            self._n += 1
        else:
            self._table[s]._value = v

    def _bucket_delitem(self, j, k):
        found, s = self._find_slot(j, k)
        if not found:
            raise KeyError("Key Error: " + repr(k))
        self._table[s] = ProbeHashMap._AVAIL

    def __iter__(self):
        for j in range(len(self._table)):
            if not self._is_available(j):
                yield self._table[j]._key


class SortedTableMap(MapBase):
    """Map Implementation using sorted table"""

    def __init__(self):
        self._table = []

    def _find_index(self, k, low, high):
        """Return index of the leftmost item with key greater than or equal to k,
        return high + 1 if not such item qualifies.
        that is, j will be returned such that
            all items of slice table[low:j] have key < k
            all items of slice table[j:high + 1] have key >= k
        """

        if high < low:
            return high + 1
        else:
            mid = (low + high) // 2
            if k == self._table[mid]._key:
                return mid
            elif k < self._table[mid]._key:
                return self._find_index(k, low, mid - 1)
            else:
                return self._find_index(k, mid + 1, high)

    def __len__(self):
        return len(self._table)

    def __getitem__(self, k):
        j = self._find_index(k, 0, len(self) - 1)
        if j == len(self) or self._table[j].key != k:
            raise KeyError("Key Error: " + repr(k))
        return self._table[j]._value

    def __setitem__(self, k, v):
        j = self._find_index(k, 0, len(self) - 1)
        if j < len(self) and self._table[j]._key == k:
            self._table[j]._value = v
        else:
            self._table.insert(j, self._item(k, v))

    def __delitem__(self, k):
        j = self._find_index(k, 0, len(self) - 1)
        if j == len(self) or self._table[j]._key != k:
            raise KeyError('Key Error: ' + repr(k))
        self._table.pop(j)

    def __iter__(self):
        for item in self._table:
            yield item._key

    def find_min(self):
        if len(self) > 0:
            return (self._table[0]._key, self._table[0]._value)
        else:
            return None

    def find_max(self):
        if len(self) > 0:
            return (self._table[-1]._key, self._table[-1]._value)
        else:
            return None
    
    def find_ge(self, k):
        """Return key-value pair with least key greater than or equal to k"""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j < len(self):
            return (self._table[j]._key, self._table[j]._value)
        else:
            return None

    def find_lt(self, k):
        """Return key-value pair with greatest key strictly less than k"""
        j = self._find_index(k, 0, len(self) - 1)
        if j >0:
            return (self._table[j-1]._key, self._table[j-1]._value)
        else:
            return None

    def find_gt(self, k):
        """Return key-value pair with least key strictly greater than k"""
        j = self._find_index(k, 0, len(self)-1)
        if j < len(self) and self._table[j]._key == k:
            j += 1
        if j < len(self):
            return (self._table[j]._key, self._table[j]._value)
        else:
            return None

    def find_range(self, start, stop):
        """Iterate all (key, value) pairs such that start <= key < stop
        if start is None, iteration begins with minimum key of map.
        if stop is None, iteration continues through the maximum key of map
        """

        if start is None:
            j = 0
        else:
            j = self._find_index(start, 0, len(self._table) -1)
        while j < len(self) and (stop is None or self._table[j]._key < stop)
            yield (self._table[j]._key, self._table[j]._value)
            j += 1
        
        
if __name__ == "__main__":
    hash_map = ProbeHashMap()

    dic = {str(i): i for i in range(100)}

    for key, val in dic.items():
        hash_map[key] = val

    for key in dic.keys():
        if key not in hash_map:
            raise KeyError("Code is wrong")

        hash_map[key] = 1
