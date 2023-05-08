from math import isclose
class Node:
    '''Node for use with doubly-linked list'''
    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None

class OrderedList:
    '''A doubly-linked ordered list of items, from lowest (head of list) to highest (tail of list)'''

    def __init__(self):
        '''Use ONE dummy node as described in class
           ***No other attributes***
           DO NOT have an attribute to keep track of size'''
        self.head = Node(None)
        self.head.next = self.head
        self.head.prev = self.head

    def is_empty(self):
        '''Returns True if OrderedList is empty
            MUST have O(1) performance'''
        return self.head.next == self.head

    def add(self, item):
        '''Adds an item to OrderedList, in the proper location based on ordering of items
           from lowest (at head of list) to highest (at tail of list) and returns True.
           If the item is already in the list, do not add it again and return False.
           MUST have O(n) average-case performance.  Assume that all items added to your 
           list can be compared using the < operator and can be compared for equality/inequality.
           Make no other assumptions about the items in your list'''
        if self.search(item):
            return False
        new = Node(item)
        if self.is_empty() or self.head.next.item > item:
            new.next = self.head.next
            self.head.next = new
            new.next.prev = new
            new.prev = self.head
        else:
            temp = self.head.next
            while temp != self.head:
                if temp.item > item:
                    break
                temp = temp.next
            new.prev = temp.prev
            new.next = temp
            temp.prev.next = new
            temp.prev = new
        return True

    def remove(self, item):
        '''Removes the first occurrence of an item from OrderedList. If item is removed (was in the list) 
           returns True.  If item was not removed (was not in the list) returns False
           MUST have O(n) average-case performance'''
        if self.is_empty():
            return False
        if not self.search(item):
            return False
        want = self.head.next
        while want.item is not None:
            if want.item == item:
                break
            want = want.next
        prev_n = want.prev
        next_n = want.next
        if prev_n.item is not None:
            prev_n.next = next_n
        else:
            self.head.next = next_n
            self.head.prev = prev_n
        if next_n.item is not None:
            next_n.prev = prev_n
        return True


    def index(self, item):
        '''Returns index of the first occurrence of an item in OrderedList (assuming head of list is index 0).
           If item is not in list, return None
           MUST have O(n) average-case performance'''
        if self.is_empty():
            return None
        if not self.search(item):
            return None
        i = -1
        temp = self.head.next
        found = False
        while temp.item is not None:
            i += 1
            if temp.item == item:
                found = True
                break
            temp = temp.next
        return i
        

    def pop(self, index):
        '''Removes and returns item at index (assuming head of list is index 0).
           If index is negative or >= size of list, raises IndexError
           MUST have O(n) average-case performance'''
        if index < 0 or index >= self.size():
            raise IndexError
        i = 0
        want = self.head.next
        while (want != self.head) and (i != index):
            want = want.next
            i += 1 
        prev_n = want.prev
        next_n = want.next
        if prev_n != self.head:
            prev_n.next = next_n
        else:
            self.head.next = next_n
            #self.head.prev = prev_n
        if next_n != self.head:
            next_n.prev = prev_n
        else:
            self.head.prev = prev_n
        return want.item

    def search(self, item):
        '''Searches OrderedList for item, returns True if item is in list, False otherwise"
           To practice recursion, this method must call a RECURSIVE method that
           will search the list
           MUST have O(n) average-case performance'''
        return self.search_help(self.head.next, item)

    def search_help(self, node, item):
        if node == self.head:
            return False
        if node.item == item:
            return True
        return self.search_help(node.next, item)

    def python_list(self):
        '''Return a Python list representation of OrderedList, from head to tail
           For example, list with integers 1, 2, and 3 would return [1, 2, 3]
           MUST have O(n) performance'''
        result = []
        temp = self.head.next
        while temp.item is not None:
            result.append(temp.item)
            temp = temp.next
        return result

    def python_list_reversed(self):
        '''Return a Python list representation of OrderedList, from tail to head, using recursion
           For example, list with integers 1, 2, and 3 would return [3, 2, 1]
           To practice recursion, this method must call a RECURSIVE method that
           will return a reversed list
           MUST have O(n) performance'''
        return self.reverse_help(self.head.next)

    def reverse_help(self, node):
        if node.item is not None:
            item = self.reverse_help(node.next)
            return item + [node.item]
        else:
            return []

    def size(self):
        '''Returns number of items in the OrderedList
           To practice recursion, this method must call a RECURSIVE method that
           will count and return the number of items in the list
           MUST have O(n) performance'''
        return self.size_helper(self.head.next)
        
    def size_helper(self, node):
        if node == self.head:
            return 0
        return self.size_helper(node.next) + 1

 
