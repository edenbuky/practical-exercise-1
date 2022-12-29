# Python code for above approach
class Node(object):
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def __repr__(self):
        a = "val: " + str(self.data)
        b = " --> " + str(self.next)
        return a + b


class DoublyLinkedList(object):
    def __init__(self):
        self.head = None

    def __repr__(self):
        h = self.head
        l = []
        while h:
            l.append(h.val)
            h = h.next
        return l

    def insert_at_head(self, value):
        n = Node(value)
        n.next = self.head
        if (self.head != None):
            self.head.prev = n
        self.head = n

    def insert_at_tail(self, value):
        crr = self.head
        for i in range(len(self)):
            crr = crr.next
        crr.next = Node(value)

    def display(self):
        temp = self.head
        while (temp):
            print(temp.data, end=" ")
            temp = temp.next

    def insert_at_index(self, val, i):

        if i == 0:
            self.insert_at_head(val)
            return
        elif i == len(self) and i != 0:
            print("ppppp")
            self.insert_at_tail(val)
            return
        new = Node(val)
        crr = self.head
        for x in range(i - 1):
            crr = crr.next
        nxt = crr.next
        crr.next = new
        new.prev = crr
        new.next = nxt
        if nxt is not None:
            nxt.prev = new

    def delete_first(self):
        new_head = self.head.next
        self.head = new_head
        if new_head:
            new_head.prev = None

    # 0 < i <= self.length()
    def delete_at_index(self, i):
        crr = self.head
        for x in range(i - 1):
            crr = crr.next
        del_node = crr.next
        nxt = del_node.next
        crr.next = nxt
        if nxt:
            nxt.prev = crr

    def __len__(self):
        crr = self.head
        l = 0
        while crr:
            l += 1
            crr = crr.next
        return l

    def delete_last(self):
        crr = self.head
        for i in range(len(self) - 1):
            crr = crr.next
        crr.next = None




