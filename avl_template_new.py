#username - complete info
#id1      - complete info
#name1    - complete info
#id2      - 316444892
#name2    - Eden Buky

import random

"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields.

	@type value: str
	@param value: data of your node/
	"""
	def __init__(self, value = None):
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		self.size = 0

	def __repr__(self):
		s = "value:" + str(self.value) + "right child: " + str(self.right) + "left child: " + str(self.left) + "parent: " + str(self.parent)
		print(s)
		return s


	"""returns the left child
	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child
	"""
	def getLeft(self):
		return self.left


	"""returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child
	"""
	def getRight(self):
		return self.right

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
		return self.value

	"""returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	"""
	def getHeight(self):
		return self.height


	"""sets left child

	@type node: AVLNode
	@param node: a node
	"""
	def setLeft(self, node):
		self.left = node
		self.height = 1 + max(self.getLeft().getHeight(), self.getRight().getHeight())
		self.setSize()



	"""sets right child

	@type node: AVLNode
	@param node: a node
	"""
	def setRight(self, node):
		self.right = node
		self.height = 1 + max(self.getLeft().getHeight(), self.getRight().getHeight())
		self.setSize()



	"""sets parent

	@type node: AVLNode
	@param node: a node
	"""
	def setParent(self, node):
		self.parent = node



	"""sets value
	
	@type value: str
	@param value: data
	"""
	def setValue(self, value):
		self.value = value


	"""sets the balance factor of the node

	@type h: int
	@param h: the height
	"""
	def setHeight(self, k = None):
		if k is None:
			self.height = 1 + max(self.getLeft().getHeight(), self.getRight().getHeight())
		else:
			self.height = k


	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def isRealNode(self):
		if self.height == -1:
			return False
		return True

	'''//////////////////////////////////////////////////////
	_____________________Extra Methods_______________________
	/////////////////////////////////////////////////////////'''

	"""returns the size of the subtree

		@rtype: int
		@returns: the height of self, -1 if the node is virtual
		"""
	def getSize(self):
		return self.size

	"""sets parent

			@type k: int
			@param k: the size
			"""
	def setSize(self, k=None):
		if k is None:
			self.size = 1 + self.getRight().getSize() + self.getLeft().getSize()
		else:
			self.size = k

	"""" BF() @return the Balance factor of a node
	"""
	def BF(self):
		return self.left.getHeight() - self.right.getHeight()


"""
A class implementing the ADT list, using an AVL tree.
"""

class AVLTreeList(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.size = 0
		self.root = AVLNode()
		# add your fields here
		self.root.left = AVLNode()
		self.root.right = AVLNode()
		self.first_node = None
		self.last_node = None



	"""returns whether the list is empty

	@rtype: bool
	@returns: True if the list is empty, False otherwise
	"""
	def empty(self):
		return self.size == 0

	"""retrieves the value of the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: index in the list
	@rtype: str
	@returns: the the value of the i'th item in the list
	"""
	def retrieve(self, i):
		if i < 0 or i > self.size:
			return None
		return self.treeSelect(i+1).getValue()

	"""inserts val at position i in the list

	@type i: int
	@pre: 0 <= i <= self.length()
	@param i: The intended index in the list to which we insert val
	@type val: str
	@param val: the value we inserts
	@rtype: list
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def insert(self, i, val):
		if i < 0 or i > self.size:
			return None
		new_node = AVLNode(val)
		new_node.height = 0
		new_node.left = AVLNode()
		new_node.right = AVLNode()
		if i == 0:
			self.first_node = new_node
		if i == self.size:
			self.last_node = new_node
		return self.node_insert(new_node, i)

	def _insert(self, new_node, i):
		if self.empty():
			self.root = new_node
			self.first_node = new_node
			self.last_node = new_node
			return
		if i == self.size:
			max_node = self.max(self.root)
			max_node.setRight(new_node)
			new_node.setParent(max_node)
		else:
			# i < n
			nxt = self.treeSelect(i + 1)
			if not nxt.left.isRealNode():
				nxt.setLeft(new_node)
				new_node.setParent(nxt)
			else:
				predecessor = self.max(nxt.getLeft())
				predecessor.setRight(new_node)
				new_node.setParent(predecessor)

	def node_insert(self, new_node, i):
		self._insert(new_node, i)
		self.size += 1
		rotation = self.update(new_node)
		return rotation



	"""deletes the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, i):
		if self.empty() or self.size <= i or i < 0:
			return -1
		if i == 0:
			rotations = self.deleteNode(self.first_node)
		elif i == self.size - 1:
			rotations = self.deleteNode(self.last_node)
		else:
			rotations = self.deleteNode(self.treeSelect(i+1))

		return rotations

	def deleteNode(self, node):
		right_child = node.getLeft()
		left_child = node.getRight()
		parent = node.getParent()
		balance_from = None

		if (not right_child.isRealNode()) or (not left_child.isRealNode()):
			if self.root is node:
				if self.size == 1:
					self.size = 0
					self.root = AVLNode()
					self.root.left = AVLNode()
					self.root.right = AVLNode()
					self.first_node = None
					self.last_node = None

				if self.size == 2:
					if left_child.isRealNode():
						self.root = left_child
						self.first_node = left_child
						self.last_node = left_child
					else:
						self.root = right_child
						self.first_node = right_child
						self.last_node = right_child

			else:
				balance_from = self.simpleDelete(node)
				# update first and last
				if node is self.first_node:
					self.first_node = parent
				if node is self.last_node:
					self.last_node = parent

		elif right_child and left_child:
			balance_from = self.twoChildrenDelete(node)

		if balance_from is None:
			return 0
		else:
			return self.update(balance_from)


	def simpleDelete(self, del_node):
		right_son = del_node.getLeft()
		left_son = del_node.getRight()
		parent = del_node.getParent()

		if parent.getLeft() is del_node:
			if left_son.isRealNode():
				parent.setLeft(left_son)
			else:
				parent.setLeft(right_son)
		else:
			if left_son is not None:
				parent.setRight(left_son)
			else:
				parent.setRight(right_son)
		return parent

	def twoChildrenDelete(self, del_node):
		# Find the successor node (the smallest node in the right subtree)
		node_succ = self.successor(del_node)
		# The successor node have one or zero children
		balance_from = self.simpleDelete(node_succ)
		# Replace del_node with his successor
		node_succ.setParent(del_node.getParent())
		node_succ.setLeft(del_node.getLeft())
		node_succ.setRight(del_node.getRight())
		if (node_succ.getParent()) and (node_succ.getLeft().isRealNode()):
			node_succ.getLeft().setParent(node_succ)
		if (node_succ.getParent()) and (node_succ.getRight().isRealNode()):
			node_succ.getRight().setParent(node_succ)
		if (node_succ.getParent()) and (node_succ.getParent().isRealNode()):
			if node_succ.getParent().getLeft() is del_node:
				node_succ.getParent().setLeft(node_succ)
			else:
				node_succ.getParent().setRight(node_succ)
		if del_node is self.root:
			self.root = node_succ

		if balance_from is del_node:
			return None
		return balance_from

	"""deletes the The node, it gets only if it has one or less children 
		@type i: AVLNode
		@rtype: (Boolean, int)
		@returns: True if the node was deleted and 
		the number of rebalancing operation due to AVL rebalancing 
		Otherwise it's return False and 0
		"""




	"""returns the value of the first_node item in the list

	@rtype: str
	@returns: the value of the first_node item, None if the list is empty
	"""
	def first(self):
		return self.first_node.getValue()



	"""returns the value of the last_node item in the list

	@rtype: str
	@returns: the value of the last_node item, None if the list is empty
	"""
	def last(self): # Max
		return self.last_node.getValue()

	"""returns an array representing list 

	@rtype: list
	@returns: a list of strings representing the data structure
	"""
	def listToArray(self):
		if self.empty():
			return []
		def lst_to_arr_rec(node):
			if not node.isRealNode():
				return []
			return lst_to_arr_rec(node.left) + [node.getValue()] + lst_to_arr_rec(node.right)
		return lst_to_arr_rec(self.root)




	"""returns the size of the list 

	@rtype: int
	@returns: the size of the list
	"""
	def length(self):
		return self.size

	"""sort the info values of the list

	@rtype: list
	@returns: an AVLTreeList where the values are sorted by the info of the original list.
	"""
	def sort(self):
		sorted_tree = AVLTreeList()
		if self.empty():
			return sorted_tree
		tree_valuse = self.listToArray()
		self.quickSort(tree_valuse, 0, self.size)
		for i in range(len(tree_valuse)):
			k = sorted_tree.size
			sorted_tree.insert(k,tree_valuse[i])
		return sorted_tree


	"""permute the info values of the list 

	@rtype: list
	@returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
	"""
	def permutation(self):
		print("perm")
		stack = [self.root]
		perm_lst = []
		while len(stack) > 0:
			node = stack.pop()
			perm_lst.append(node.getValue())
			if node.getLeft().isRealNode() and node.getRight().isRealNode():
				rand = random.random()
				if rand >= 0.5:
					stack.append(node.getLeft())
					stack.append(node.getRight())
				else:
					stack.append(node.getRight())
					stack.append(node.getLeft())
			elif node.getLeft().isRealNode():
				stack.append(node.getLeft())
			elif node.getRight().isRealNode():
				stack.append(node.getRight())


		perm = AVLTreeList()
		for i in range(len(perm_lst)):
			val = perm_lst[i]
			perm.insert(i, val)

		return perm


	"""concatenates lst to self

	@type lst: AVLTreeList
	@param lst: a list to be concatenated after self
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""
	def concat(self, lst):
		h_self = self.root.getHeight()
		h_lst = lst.root.getHeight()
		h_diff = abs(h_lst - h_self)
		if h_self < h_lst:
			pointer = lst.root
			x = self.max(self.root)
			self.delete(self.size)
			for k in range(h_diff - 1):
				pointer = pointer.getLeft()
			x.setLeft(self.root)
			self.root.setParent(x)
			x.setRight(pointer.getLeft())
			pointer.getLeft().setParent(x)
			pointer.setLeft(x)
			self.root = lst.root
		else:
			pointer = self.root
			x = lst.min(self.root)
			lst.delete(lst.size)
			for k in range(h_diff - 1):
				pointer = pointer.getRight()
			x.setRight(lst.root)
			lst.root.setParent(x)
			x.setLeft(pointer.getRight())
			pointer.getRight().setParent(x)
			pointer.setRight(x)

		return h_diff

	"""searches for a *value* in the list

	@type val: str
	@param val: a value to be searched
	@rtype: int
	@returns: the first_node index that contains val, -1 if not found.
	"""
	def search(self, val):
		def count_left_nodes(node):
			if not node.isRealNode():
				return 0
			return 1 + count_left_nodes(node.getLeft()) + count_left_nodes(node.getRight())

		queue = [self.root]
		while queue:
			current = queue.pop(0)
			left_count = count_left_nodes(current.getLeft())
			if current.getValue() == val:
				return left_count + 1
			if current.getLeft().isRealNode():
				queue.append(current.getLeft())
			if current.getRight().isRealNode():
				queue.append(current.getRight())
		return -1

	"""returns the root of the tree representing the list

	@rtype: AVLNode
	@returns: the root, None if the list is empty
	"""
	def getRoot(self):
		return self.root

	'''//////////////////////////////////////////////////////
	_____________________Extra Methods_______________________
	/////////////////////////////////////////////////////////'''

	def getTreeHeight(self):
		return self.root.getHeight()

	""""Tree-Select return the k'th smallest element in the list
	@type: (node, int)
	@pre: 1 <= k < T.lenght()
	@rtype: node
	@returns: the k-1'th smallest element of the list (lst[k-1])
	"""
	def treeSelect(T, k):

		def treeSelectRec(x,k):
			r = x.getLeft().getSize() + 1 if x.getLeft() else 0
			if k == r:
				return x
			else:
				if k < r:
					return treeSelectRec(x.getLeft(), k)
				elif k > r:
					return treeSelectRec(x.getRight(), k - r)
		return treeSelectRec(T.root, k)

	"""Update travel at tree in the path From the given note to the root While balancing the tree and updating the size
		@type: AVLNode
		@rtype: int
		@returns: the Amount of rotation that we did While balancing the tree
		"""

	def update(self, node):
		rotation = 0
		curr = node
		while curr != self.root:
			bf = curr.BF()
			height = curr.getHeight()
			if abs(bf) > 1:
				curr, rot = self.balance(curr)
				rotation += rot
			if curr.getHeight() != height:
				curr.setHeight()
			curr.setSize()
			curr = curr.getParent()

		curr = self.root
		bf = curr.BF()
		height = curr.getHeight()
		if abs(bf) > 1:
			curr, rot = self.balance(curr)
			rotation += rot
		if curr.getHeight() != height:
			curr.setHeight()
		curr.setSize()
		self.root = curr
		self.size = self.root.getSize()
		return rotation

	'''performs a right rotation arround input node.
			@return the "new root" after rotation which is the right child of input node'''

	def rightRotation(self, node):
		left_child = node.getLeft()
		new_left = left_child.getRight()
		parent = node.getParent()

		left_child.setRight(node)
		node.setLeft(new_left)

		# update heights
		node.setHeight(1 + max(node.getLeft().getHeight(), node.getRight().getHeight()))
		left_child.setHeight(1 + max(left_child.getLeft().getHeight(), left_child.getRight().getHeight()))

		# update parent pointers
		node.setParent(left_child)
		left_child.setParent(parent)

		if parent is not None:
			if parent.getLeft() == node:
				parent.setLeft(left_child)
			else:
				parent.setRight(left_child)
		return left_child

	'''performs a left rotation arround input node.
    @return the "new root" after rotation which is the left child of input node'''

	def leftRotation(self, node):
		right_child = node.getRight()
		node.setRight(right_child.getLeft())

		right_child.setLeft(node)

		# update heights
		node.setHeight(1 + max(node.getLeft().getHeight(), node.getRight().getHeight()))
		right_child.setHeight(1 + max(right_child.getLeft().getHeight(), right_child.getRight().getHeight()))

		# update parent pointers
		parent = node.getParent()
		node.setParent(right_child)
		right_child.setParent(parent)

		if parent is not None:
			if parent.getLeft() == node:
				parent.setLeft(right_child)
			else:
				parent.setRight(right_child)

		return right_child

	'''balnces @input node
		@return is a tuple(AVLNode, int)
		@return[0] = top node after balancing
		@return[1] = number of rotations made'''

	def balance(self, node):

		node2 = node
		balance = node.BF()
		left_child = node.getLeft()
		right_child = node.getRight()
		rotations = 0

		# Left Left Case
		if balance > 1 and left_child.BF() >= 0:
			node2 = self.rightRotation(node)
			rotations += 1

		# Left Right Case
		elif balance > 1 and left_child.BF() < 0:
			new_left = self.leftRotation(left_child)
			node.setLeft(new_left)
			node2 = self.rightRotation(node)
			rotations += 2

		# Right Right Case
		elif balance < -1 and right_child.BF() <= 0:
			node2 = self.leftRotation(node)
			rotations += 1

		# Right Left Case
		elif balance < -1 and right_child.BF() > 0:
			new_right = self.rightRotation(right_child)
			node.setRight(new_right)
			node2 = self.leftRotation(node)
			rotations += 2

		return node2, rotations

	"""returns the successor of a given
	@type: AVLNode
	@rtype : AVLNode
	@return : treeSelect(nodeRank(node) + 1)"""

	def successor(self, node):
		if node.right.isRealNode():
			return self.min(node.getRight())
		parent = node.getParent()
		curr = node
		while parent.isRealNode():
			if parent.getRight() != curr:
				break
			curr = parent
			parent = curr.getParent()
		return parent

	"""returns the predecessor of a given node
		@type: AVLNode
	@rtype : AVLNode
	@return : treeSelect(nodeRank(node) - 1)"""

	def predecessor(self, node):
		if node.getLeft().isRealNode():
			return self.max(node.getLeft())
		parent = node.getParent()
		curr = node
		while parent.isRealNode():
			if parent.getLeft() != curr:
				break
			curr = parent
			parent = curr.getParent()
		return parent

	"""returns the first node of subtree (or sublist) rooted at node
	@rtype : AVLNode"""

	def min(self, node):
		if (not node.getLeft()) or not node.getLeft().isRealNode():
			return node
		return self.min(node.getLeft())

	"""returns the last_node node of subtree (or sublist) rooted at node
		@rtype : AVLNode"""

	def max(self, node):
		if (not node.getRight()) or not node.getRight().isRealNode():
			return node
		return self.max(node.getRight())

	def partition(self,array, low, high):

		# choose the rightmost element as pivot
		pivot = array[high]

		# pointer for greater element
		i = low - 1

		# traverse through all elements
		# compare each element with pivot
		for j in range(low, high):
			if array[j] <= pivot:
				# If element smaller than pivot is found
				# swap it with the greater element pointed by i
				i = i + 1

				# Swapping element at i with element at j
				(array[i], array[j]) = (array[j], array[i])

		# Swap the pivot element with the greater element specified by i
		(array[i + 1], array[high]) = (array[high], array[i + 1])

		# Return the position from where partition is done
		return i + 1

	def quickSort(self,array, low, high):
		if low < high:
			# Find pivot element such that
			# element smaller than pivot are on the left
			# element greater than pivot are on the right
			pi = array.partition(array, low, high)

			# Recursive call on the left of pivot
			self.quickSort(array, low, pi - 1)

			# Recursive call on the right of pivot
			self.quickSort(array, pi + 1, high)




	'''@@@@@@@@@@@@@@@ for tester @@@@@@@@@@@@@@@'''
	def append(self, val):
		self.insert(self.length(), val)

	### PRINT TREE FUNCTIONS ###

	def printt(self):
		out = ""
		for row in self.printree(self.root):  # need printree.py file
			out = out + row + "\n"
		print(out)

	def printree(self, t, bykey=True):
		# for row in trepr(t, bykey):
		#        print(row)
		return self.trepr(t, False)

	def trepr(self, t, bykey=False):
		if t == None:
			return ["#"]

		thistr = str(t.key) if bykey else str(t.getValue())

		return self.conc(self.trepr(t.left, bykey), thistr, self.trepr(t.right, bykey))

	def conc(self, left, root, right):

		lwid = len(left[-1])
		rwid = len(right[-1])
		rootwid = len(root)

		result = [(lwid + 1) * " " + root + (rwid + 1) * " "]

		ls = self.leftspace(left[0])
		rs = self.rightspace(right[0])
		result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid *
					  " " + "\\" + rs * "_" + (rwid - rs) * " ")

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

	def leftspace(self, row):
		# row is the first_node row of a left node
		# returns the index of where the second whitespace starts
		i = len(row) - 1
		while row[i] == " ":
			i -= 1
		return i + 1

	def rightspace(self, row):
		# row is the first_node row of a right node
		# returns the index of where the first_node whitespace ends
		i = 0
		while row[i] == " ":
			i += 1
		return i




