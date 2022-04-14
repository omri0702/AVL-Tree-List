# username - rosenfeld
# id1      - 206291734
# name1    - alon rosenfeld
# id2      - 313247900
# name2    - omri ravona

###tester
import random
import string


def printree(t, bykey=False):
    """Print a textual representation of t
    bykey=True: show keys instead of values"""
     #for row in trepr(t, bykey):
     #       print(row)
    return trepr(t, bykey)


def trepr(t, bykey=False):
    """Return a list of textual representations of the levels in t
    bykey=True: show keys instead of values"""
    if t == None:
        return ["#"]

    if t.height == -1:
        return ["#"]

    thistr = str(t.key) if bykey else str(t.value)

    return conc(trepr(t.left, bykey), thistr, trepr(t.right, bykey))


def conc(left, root, right):
    """Return a concatenation of textual represantations of
    a root node, its left node, and its right node
    root is a string, and left and right are lists of strings"""

    lwid = len(left[-1])
    rwid = len(right[-1])
    rootwid = len(root)

    result = [(lwid + 1) * " " + root + (rwid + 1) * " "]

    ls = leftspace(left[0])
    rs = rightspace(right[0])
    result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "\\" + rs * "_" + (rwid - rs) * " ")

    for i in range(max(len(left), len(right))):
        row = ""
        if i < len(left):
            row += left[i]
        else:
            row += lwid * " "

        row += (rootwid + 2) * " "

        if i < len(right):
            row += right[i]
        else:
            row += rwid * " "

        result.append(row)

    return result


def leftspace(row):
    """helper for conc"""
    # row is the first row of a left node
    # returns the index of where the second whitespace starts
    i = len(row) - 1
    while row[i] == " ":
        i -= 1
    return i + 1


def rightspace(row):
    """helper for conc"""
    # row is the first row of a right node
    # returns the index of where the first whitespace ends
    i = 0
    while row[i] == " ":
        i += 1
    return i
"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.


    @type value: str
    @param value: data of your node
    """

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        self.size = 0  # this supposed to be maintain in the tree class

    def __repr__(self):
        return "(" + str(self.height) + ":" + str(self.value) + ")"

    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child
    """

    def getLeft(self):
        if self.left.isRealNode():
            return self.left
        return None

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    """

    def getRight(self):
        if self.right.isRealNode():
            return self.right
        return None

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def getParent(self):
        return self.parent

    """return the value

    @rtype: str
    @returns: the value of self, None if the node is virtual
    """

    def getValue(self):
        if self.isRealNode():
            return self.value
        else:
            return None

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def getHeight(self):
        if self.isRealNode():
            return self.height
        return -1

    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def setLeft(self, node):
        self.left = node
        return None

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def setRight(self, node):
        self.right = node
        return None

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def setParent(self, node):
        self.parent = node
        return None

    """sets value

    @type value: str
    @param value: data
    """

    def setValue(self, value):
        self.value = value
        return None

    """sets the balance factor of the node

    @type h: int
    @param h: the height
    """

    def setHeight(self, h):
        self.height = h

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def isRealNode(self):
        if self.height == -1:
            return False
        else:
            return True


"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.root = None
        self.firstNode = None
        self.lastNode = None
        self.lengthOfTree = 0
        self.virtualParent = AVLNode(None)

    def __repr__(self):  # no need to understand the implementation of this one
        out = ""
        for row in printree(self.root):  # need printree.py file
            out = out + row + "\n"
        return out

    """returns whether the list is empty

    @rtype: bool
    @returns: True if the list is empty, False otherwise
    """

    def empty(self):
        if self.lengthOfTree == 0:
            return True
        else:
            return False

    def setVirtualSons(self, node):
        node.left = AVLNode(None)
        node.left.parent = node
        node.right = AVLNode(None)
        node.right.parent = node
        node.height = 0
        node.size = 1

    """retrieves the value of the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: index in the list
    @rtype: str
    @returns: the the value of the i'th item in the list
    """

    def retrieve(self, i):  ## time complexity: O(log(n)) worst case
        def retrieve_rec(root, j):
            if root.left.isRealNode():
                left_subtree_size = root.left.size + 1
                if left_subtree_size == j:
                    return root

                elif j < left_subtree_size:
                    return retrieve_rec(root.left, j)
                else:
                    return retrieve_rec(root.right, j - left_subtree_size)
            elif j == 1:  ##if no sub_tree to the left
                return root
            elif root.right.isRealNode():
                return retrieve_rec(root.right, j - 1)

        if i < 0 or not self.lengthOfTree == 0 or self.root.size > i + 1:
            return None
        return retrieve_rec(self.root, i + 1).value

    """inserts val at position i in the list

    @type i: int
    @pre: 0 <= i <= self.length()
    @param i: The intended index in the list to which we insert val
    @type val: str
    @param val: the value we inserts
    @rtype: list
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, i, val):  ## time complexity: O(log(n)) worst case
        if i == 0 and self.lengthOfTree != 0:
            self.insert_first(val)
            leaf = self.firstNode
        elif i == self.lengthOfTree and self.lengthOfTree != 0:
            self.insert_last(val)
            leaf = self.lastNode
        elif i == 0 and self.lengthOfTree == 0:
            self.insertRoot(val)
            return
        elif i < 0 or i > self.lengthOfTree:
            return
        else:
            leaf = self.insert_middle(i, val)

        leaf = leaf.parent
        self.correctSizeInsert(leaf)
        while leaf.isRealNode():
            ballanceFactor = leaf.left.height - leaf.right.height
            if -2 < ballanceFactor < 2 and leaf.height == max(leaf.right.height, leaf.left.height) + 1:
                break
            elif -2 < ballanceFactor < 2:
                leaf.height = max(leaf.right.height, leaf.left.height) + 1
                leaf = leaf.parent
            elif ballanceFactor == -2:
                self.leftRotation(leaf)
                if leaf == self.root:
                    self.root = leaf.parent
                break
            else:
                self.rightRotaion(leaf)
                if leaf == self.root:
                    self.root = leaf.parent
                break

    def insert_middle(self, i, val): ## time complexity: O(log(n)) worst case - sub-function of insert()
        tmp = self.get_node(i)  ##current at index i at the list
        if tmp.left.isRealNode():
            tmp2 = self.predecessor(tmp)
            tmp2.right = AVLNode(val)
            tmp2.right.height = 0
            tmp2.right.parent = tmp2
            self.setVirtualSons(tmp2.right)
            self.lengthOfTree += 1
            leaf = tmp2.right
        else:
            tmp.left = AVLNode(val)
            tmp.left.height = 0
            self.setVirtualSons(tmp.left)
            self.lengthOfTree += 1
            leaf = tmp.left
            leaf.parent = tmp
        return leaf

    def insert_first(self, val):  ## time complexity: O(log(n)) worst case - sub-function of insert()
        self.firstNode.left = AVLNode(val)
        self.firstNode.left.parent = self.firstNode
        self.setVirtualSons(self.firstNode.left)
        self.firstNode = self.firstNode.left
        self.lengthOfTree += 1
        self.firstNode.height = 0

    def insert_last(self, val):  ## time complexity: O(log(n)) worst case - sub-function of insert()
        self.lastNode.right = AVLNode(val)
        self.lastNode.right.parent = self.lastNode
        self.setVirtualSons(self.lastNode.right)
        self.lastNode = self.lastNode.right
        self.lengthOfTree += 1
        self.lastNode.height = 0

    def insertRoot(self, val):
        self.root = AVLNode(val)
        self.root.parent = self.virtualParent
        self.setVirtualSons(self.root)
        self.lengthOfTree += 1
        self.lastNode = self.root
        self.firstNode = self.root

    def rightRotaion(self, node):  ## time complexity: O(1) worst case
        isLR = False
        if node.left.left.height - node.left.right.height == -1:
            isLR = True
            tmpLeft = node.left
            node.left = node.left.right
            node.left.parent = node  #
            tmpLeft.right = node.left.left
            tmpLeft.right.parent = tmpLeft
            node.left.left = tmpLeft
            tmpLeft.parent = node.left
        boolie = True if node.parent.left == node else False
        node.left.parent = node.parent
        if boolie:
            node.parent.left = node.left
        else:
            node.parent.right = node.left
        node.parent = node.left
        node.left = node.left.right
        node.parent.right = node
        node.left.parent = node
        node.right.parent = node

        node.height = max(node.left.height, node.right.height) + 1  ##fixing heights
        if isLR:
            node.parent.left.height = max(node.parent.left.left.height, node.parent.left.right.height) + 1
            tmpLeft.size = tmpLeft.left.size + tmpLeft.right.size + 1  ####
        node.parent.height = max(node.parent.left.height, node.height) + 1
        node.parent.size = node.size  ##fixing sizes
        node.size = node.left.size + node.right.size + 1

    def leftRotation(self, node):  ## time complexity: O(1) worst case
        isRL = False
        if node.right.left.height - node.right.right.height == 1:
            isRL = True
            tmpright = node.right
            node.right = node.right.left
            node.right.parent = node
            tmpright.left = node.right.right
            tmpright.left.parent = tmpright
            node.right.right = tmpright
            tmpright.parent = node.right
        boolie = True if node.parent.left == node else False
        node.right.parent = node.parent
        if boolie:
            node.parent.left = node.right
        else:
            node.parent.right = node.right
        node.parent = node.right
        node.right = node.right.left
        node.parent.left = node
        node.left.parent = node
        node.right.parent = node

        node.height = max(node.left.height, node.right.height) + 1  ##fixing heights
        if isRL:
            node.parent.right.height = max(node.parent.right.left.height, node.parent.right.right.height) + 1
            tmpright.size = tmpright.left.size + tmpright.right.size + 1  ####
        node.parent.height = max(node.parent.left.height, node.height) + 1
        node.parent.size = node.size  ##fixing sizes
        node.size = node.left.size + node.right.size + 1

    def correctSizeInsert(self, node):  ## time complexity: O(log(n)) worst case
        while node.isRealNode():
            node.size += 1
            node = node.parent

    def successor(self, node):  ## time complexity: O(log(n)) worst case
        if node.right.isRealNode():
            son = node.right
            while son.left.isRealNode():
                son = son.left
            return son
        else:
            father = node.parent
            current = node
            while father.isRealNode() and father.right == current:
                current = father
                father = father.parent
            return father

    def predecessor(self, node):  ## time complexity: O(log(n)) worst case
        if node.left.isRealNode():
            son = node.left
            while son.right.isRealNode():
                son = son.right
            return son
        else:
            father = node.parent
            current = node
            while father.isRealNode() and father.left == current:
                current = father
                father = father.parent
            return father

    def get_node(self, i):  ## time complexity: O(log(n)) worst case
        def get_node_rec(root, j):
            if root.left.isRealNode():
                left_subtree_size = root.left.size + 1
                if left_subtree_size == j:
                    return root

                elif j < left_subtree_size:
                    return get_node_rec(root.left, j)
                else:
                    return get_node_rec(root.right, j - left_subtree_size)
            elif j == 1:  ##if no sub_tree to the left
                return root
            elif root.right.isRealNode():
                return get_node_rec(root.right, j - 1)

        return get_node_rec(self.root, i + 1)

    """deletes the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list to be deleted
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, i):  ## time complexity: O(log(n)) worst case
        if i < 0 or i >= self.lengthOfTree:
            return -1
        wanted = self.get_node(i)
        if wanted.right.isRealNode() and wanted.left.isRealNode():
            node = self.deleteTwoSons(wanted)
        elif wanted.right.isRealNode() or wanted.left.isRealNode():
            node = self.deleteOneSon(wanted)
        else:
            node = self.deleteLeaf(wanted)
        self.lengthOfTree -= 1
        self.correctSizeDelete(node)

        while node.isRealNode():
            ballanceFactor = node.left.height - node.right.height
            if -2 < ballanceFactor < 2 and node.height == max(node.right.height, node.left.height) + 1:
                node = node.parent
            elif -2 < ballanceFactor < 2:
                node.height = max(node.right.height, node.left.height) + 1
                node = node.parent
            elif ballanceFactor == -2:
                self.leftRotation(node)
                if node == self.root:
                    self.root = node.parent
                    break
                node = node.parent
            else:
                self.rightRotaion(node)
                if node == self.root:
                    self.root = node.parent
                    break
                node = node.parent



    def deleteLeaf(self, node):
        if self.root == node:
            self.root = None
            self.firstNode = None
            self.lastNode = None
        elif self.firstNode == node:
            self.firstNode = node.parent
        elif self.lastNode == node:
            self.lastNode = node.parent
        if node.parent.right == node:
            father = node.parent
            node.parent = None
            father.right = node.right
            node.right.parent = father
            node.right = None
            node.left.parent = None
            node.left = None
        else:
            father = node.parent
            node.parent = None
            father.left = node.left
            node.left.parent = father
            node.left = None
            node.right.parent = None
            node.right = None
        return father

    def deleteOneSon(self, node):
        if self.root == node:
            if node.left.isRealNode():
                self.root = node.left
                self.lastNode = node.left
            else:
                self.root = node.right
                self.firstNode = node.right
        elif self.firstNode == node:
            self.firstNode = node.right
        elif self.lastNode == node:
            self.lastNode = node.left
        if node.left.isRealNode():
            son = node.left
        else: son = node.right
        if node.parent.left == node:
            node.parent.left = son
            son.parent = node.parent
        else:
            node.parent.right = son
            son.parent = node.parent
        node.parent = None
        node.right = None
        node.left = None
        return son.parent

    def deleteTwoSons(self, node):
        isRoot = False
        succ = self.successor(node)
        if self.root == node:
            isRoot = True
        if succ.parent == node:
            father = succ
        else:
            father = succ.parent
        if succ.right.isRealNode() or succ.left.isRealNode():
            self.deleteOneSon(succ)
        else:
            self.deleteLeaf(succ)
        succ.parent = node.parent
        node.parent = None
        if succ.parent.left == node:
            succ.parent.left = succ
        else:
            succ.parent.right = succ
        succ.left = node.left
        node.left = None
        succ.left.parent = succ
        succ.right = node.right
        node.right = None
        succ.right.parent = succ
        succ.size = node.size
        succ.height = node.height
        if isRoot:
            self.root = succ
        return father

    def correctSizeDelete(self, node):  ## time complexity: O(log(n)) worst case
        while node.isRealNode():
            node.size -= 1
            node = node.parent

    """returns the value of the first item in the list

    @rtype: str
    @returns: the value of the first item, None if the list is empty
    """

    def first(self):
        return self.firstNode.value

    """returns the value of the last item in the list

    @rtype: str
    @returns: the value of the last item, None if the list is empty
    """

    def last(self):
        return self.lastNode.value

    """returns an array representing list 

    @rtype: list
    @returns: a list of strings representing the data structure
    """

    def listToArray(self):  ## time complexity O(n) at all cases
        def listToArayRec(node, lst, index):
            if not node.isRealNode():
                return
            listToArayRec(node.left, lst, index)
            lst.append(node.value)
            index += 1
            listToArayRec(node.right, lst, index)
            return lst

        lst = []
        i = 0
        if self.lengthOfTree == 0:
            return lst
        return listToArayRec(self.root, lst, i)

    """returns the size of the list 

    @rtype: int
    @returns: the size of the list
    """

    def length(self):
        return self.length

    """splits the list at the i'th index

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list according to whom we split
    @rtype: list
    @returns: a list [left, val, right], where left is an AVLTreeList representing the list until index i-1,
    right is an AVLTreeList representing the list from index i+1, and val is the value at the i'th index.
    """

    def split(self, i):
        return None

    """concatenates lst to self

    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def concat(self, lst):
        return None

    """searches for a *value* in the list

    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    """

    def search(self, val): ## time complexity O(n) at all cases
        avl_list = self.listToArray()
        for i in range(self.lengthOfTree):
            if avl_list[i] == val:
                return i
        return -1

    """returns the root of the tree representing the list

    @rtype: AVLNode
    @returns: the root, None if the list is empty
    """

    def getRoot(self):
        return self.root

##function for testing and debbug
    def check(self):
        tree = self
        for i in range(tree.lengthOfTree):
            node = tree.get_node(i)
            if node.left.parent != node:
                print(node.value + "left son prob")
            if node.right.parent != node:
                print(node.value + "right son prob")

tree = AVLTreeList()
tree.insert(0, "5")
tree.insert(0,"2")
tree.insert(2,"10")
tree.insert(0,"1")
tree.insert(2,"3")
tree.insert(4,"8")
tree.insert(6,"11")
tree.insert(3, "4")
tree.insert(5, "6")
tree.insert(7, "9")
tree.insert(10, "12")
tree.insert(6, "7")
tree.delete(0)
print(tree)
# for i in range(10):
#     tree.delete(0)
#     print(tree)
# tree2 = AVLTreeList()
# for i in range(500000):
#     j = random.randint(0,i)
#     str1 = "".join(random.choice(string.ascii_lowercase))
#     tree2.insert(j, str1)
# # print(tree2)
# for i in range(300000):
#     # j = random.randint(0, 500-i)
#     tree2.delete(0)
