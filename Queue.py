# -*- coding: utf-8 -*-
class Queue:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def enqueue(self, item):
        self.items.insert(0,item)
    def dequeue(self):
        return self.items.pop()
    def first(self):
        return self.items[0]
    def size(self):
        return len(self.items)
    def enqueueItems(self, items):
        for el in items:
            self.enqueue(el)

class BQueue:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def enqueue(self, item):
        self.items.append(item)
    def dequeue(self):
        return self.items.pop()
    def size(self):
        return len(self.items)
    