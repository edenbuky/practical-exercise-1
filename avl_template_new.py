#username - complete info
#id1      - 207482993
#name1    - Yael Yacobovich
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
		s = "value:" + str(self.value)
		t = " size = " + str(self.size)  + " height: " + str(self.height)
		return s + t


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




	"""sets right child

	@type node: AVLNode
	@param node: a node
	"""
	def setRight(self, node):
		self.right = node




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


	"""sets height of the node

	@type h: int
	@param h: the height
	"""
	def setHeight(self, h = None):
		if h is None:
			self.height = 1 + max(self.getLeft().getHeight(), self.getRight().getHeight())
		else:
			self.height = h


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

	"""returns the size (number of nodes) of the subtree

		@rtype: int
		@returns: the height of self, -1 if the node is virtual
		"""

	def getSize(self):
		return self.size


	"""sets Size of the subtree 

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
		self.root = None
		# add your fields here
		self.first_node = self.min(self.root) if self.root else None
		self.last_node = self.max(self.root) if self.root else None



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
		if i < 0 or i > self.size or self.empty():
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
		new_node = AVLNode(val)
		new_node.setHeight(0)
		new_node.setSize(1)
		new_node.setLeft(AVLNode())
		new_node.getLeft().setParent(new_node)
		new_node.setRight(AVLNode())
		new_node.getRight().setParent(new_node)
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
		if i == self.size: #add at end
			max_node = self.max(self.root)
			max_node.setRight(new_node)
			max_node.setSize()
			new_node.setParent(max_node)
		else:
			# i < n
			nxt = self.treeSelect(i + 1)
			if not nxt.left.isRealNode():
				nxt.setLeft(new_node)
				nxt.setSize()
				new_node.setParent(nxt)
			else:
				predecessor = self.predecessor(nxt)
				predecessor.setRight(new_node)
				predecessor.setSize()
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
			rotations = self.delete_node2(self.first_node)
		elif i == self.size - 1:
			rotations = self.delete_node2(self.last_node)
		else:
			rotations = self.delete_node2(self.treeSelect(i + 1))

		return rotations

	"""deletes the The node it gets and return the amount of rotation that needed to be done to balance the tree
			@type node: AVLNode
			@rtype: int
			@returns: the amount of rotation return by update or 0
			"""
	def	delete_node2(self, node):
		if node is None:
			return node

		# First, we need to find the node to delete
		# We can either find it by traversing the tree
		# or we can pass it in as an argument to the delete function
		if not node.getLeft().isRealNode() and not node.getRight().isRealNode():
			# Case 1: Node to delete is a leaf node
			# Simply remove the node and update the parent's child pointer
			if node.getParent():
				new_virtual = AVLNode()
				new_virtual.setParent(node.getParent())
				if node == node.getParent().getLeft():
					node.getParent().setLeft(new_virtual)
				else:
					node.getParent().setRight(new_virtual)
			else: #node is root
				self.root = None
				self.size = 0
				self.first_node = None
				self.last_node = None
				return 0
			rot = self.update(node.getParent())
			return rot

		if not node.getLeft().isRealNode() or not node.getRight().isRealNode():
			# Case 2: Node to delete has one child
			# Replace the node with its child
			if node.getLeft().isRealNode():
				child = node.getLeft()
			else:
				child = node.getRight()

			if node.getParent():
				if node == node.getParent().getLeft():
					node.getParent().setLeft(child)
				elif node == node.getParent().getRight():
					node.getParent().setRight(child)
				rot = self.update(node.getParent())
			else: #node is root
				self.root = child
				child.setSize()
				self.size = child.getSize()
				self.first_node = self.min(self.root)
				self.last_node = self.max(self.root)
				rot = 0

			child.setParent(node.getParent())
			return rot

			# Case 3: Node to delete has two children
			# Find the successor of the node (the leftmost child of the node's right subtree)
			# and move the successor to the node's position
		successor = self.min(node.getRight())
		if successor.getParent() != node and successor.getParent():
			rot = self.delete_node2(successor)
			successor.setLeft(node.getLeft())
			successor.setRight(node.getRight())
			successor.setParent(node.getParent())
			if node.getParent():
				if node == node.getParent().getLeft():
					node.getParent().setLeft(successor)
				elif node == node.getParent().getRight():
					node.getParent().setRight(successor)
			else: #node is root
				self.root = successor
			if node.getLeft() and node.getLeft().isRealNode():
				node.getLeft().setParent(successor)
			if node.getRight() and node.getRight().isRealNode():
				node.getRight().setParent(successor)

			rot = self.update(successor)
			return rot

		else:
			# Special case: Successor is the right child of the node to delete
			# Replace the node with its right child and update the child's parent pointer
			child = node.getRight()
			left = node.getLeft()
			child.setParent(node.getParent())
			child.setLeft(left)
			left.setParent(child)
			if node.getParent():
				if node == node.getParent().getLeft():
					node.getParent().setLeft(child)
				elif node == node.getParent().getRight():
					node.getParent().setRight(child)
			else: #node is root
				self.root = child

			rot = self.update(child)
			return rot


	"""returns the value of the first_node item in the list

	@rtype: str
	@returns: the value of the first_node item, None if the list is empty
	"""
	def first(self):
		return self.first_node.getValue() if self.first_node else None



	"""returns the value of the last_node item in the list

	@rtype: str
	@returns: the value of the last_node item, None if the list is empty
	"""
	def last(self): #Max
		return self.last_node.getValue() if self.last_node else None

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
		current = self.root
		stack = []
		new_tree = AVLTreeList()

		while True:
			if current.isRealNode():
				stack.append(current)
				current = current.getLeft()
			elif (stack):
				current = stack.pop()
				key = current.getValue()
				new_tree.insert_for_sort(key)
				current = current.right
			else:
				break

		return new_tree



	"""permute the info values of the list 

	@rtype: list
	@returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
	"""
	def permutation(self):
		stack = [self.root]
		perm_lst = AVLTreeList()
		while len(stack) > 0:
			node = stack.pop()
			perm_lst.insert(0, node.getValue())
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

		return perm_lst


	"""concatenates lst to self

	@type lst: AVLTreeList
	@param lst: a list to be concatenated after self
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""
	def concat(self, lst):
		if self.empty():
			self.merged(lst)
			self.first_node = lst.first_node
			return lst.root.getHeight() if lst.root else 0
		elif lst.empty():
			return self.root.getHeight() if self.root else 0
		h_self = self.root.getHeight()
		h_lst = lst.root.getHeight()
		h_diff = abs(h_lst - h_self)
		if h_self < h_lst:
			if self.size == 1:
				lst.node_insert(self.root, 0)
				self.merged(lst)
				return h_diff
			c = lst.root
			b = c.getLeft()
			x = self.max(self.root)
			self.delete(self.size - 1)
			for k in range(h_diff - 1):
				c = c.getLeft()
				b = c.getLeft()
			x.setLeft(self.root)
			self.root.setParent(x)
			x.setRight(b)
			b.setParent(x)
			c.setLeft(x)
			x.setParent(c)
			self.merged(lst)
		else:
			if lst.size == 1:
				self.node_insert(lst.root, self.size)
				self.last_node = lst.last_node
				return h_diff
			c = self.root
			b = c.getRight()
			x = self.min(lst.root)
			lst.delete(0)
			for k in range(h_diff - 1):
				c = c.getRight()
				b = c.getRight()
			x.setRight(lst.root)
			lst.root.setParent(x)
			lst.root = self.root
			x.setLeft(b)
			b.setParent(x)
			c.setRight(x)
			x.setParent(c)
			self.last_node = lst.last_node

		self.update(x)
		return h_diff


	"""searches for a *value* in the list

	@type val: str
	@param val: a value to be searched
	@rtype: int
	@returns: the first_node index that contains val, -1 if not found.
	"""
	def search(self, val):
		current = self.root
		stack = []  # initialize stack
		cnt = 0

		while True:
			if current and current.isRealNode():
				stack.append(current)
				current = current.getLeft()
			elif (stack):
				current = stack.pop()
				if current.getValue() == val:
					return cnt
				cnt += 1
				current = current.right
			else:
				break

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

	"""inserts by key at position key in the list

		@type key: str
		@param key: the key we inserts and the position in the tree
		"""
	def insert_for_sort(self, key):
		new_node = AVLNode(key)
		new_node.setHeight(0)
		new_node.setSize(1)
		new_node.setLeft(AVLNode())
		new_node.getLeft().setParent(new_node)
		new_node.setRight(AVLNode())
		new_node.getRight().setParent(new_node)

		def insert_rec(node, new_node):
			if new_node.getValue() < node.getValue():
				if not node.getLeft().isRealNode():
					node.setLeft(new_node)
					new_node.setParent(node)
				else:
					insert_rec(node.getLeft(), new_node)
			else:
				if not node.getRight().isRealNode():
					node.setRight(new_node)
					new_node.setParent(node)
				else:
					insert_rec(node.getRight(), new_node)
			return

		if self.root is None:
			self.root = new_node
		else:
			insert_rec(self.root, new_node)
			self.update(new_node)

	"""Update managed list when other size is bigger than self size
	"""
	def merged(self, other): #other swollows us
		self.root = other.root
		self.size = other.root.getSize() if other.root else 0
		self.last_node = other.last_node


	""""Tree-Select return the k'th smallest element in the list
	@type: (node, int)
	@pre: 1 <= k < T.lenght()
	@rtype: node
	@returns: the k-1'th smallest element of the list (lst[k-1])
	"""
	def treeSelect(T, k):

		def treeSelectRec(x,k):
			r = x.getLeft().getSize() + 1
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
			#print(curr)
			bf = curr.BF()
			height = curr.getHeight()
			if abs(bf) > 1:
				curr, rot = self.balance(curr)
				rotation += rot

			curr.setHeight()
			curr.setSize()
			curr = curr.getParent()

		curr = self.root
		bf = curr.BF()
		height = curr.getHeight()
		if abs(bf) > 1:
			curr, rot = self.balance(curr)
			rotation += rot
		curr.setHeight()
		curr.setSize()
		self.root = curr
		self.size = self.root.getSize()
		self.first_node = self.min(self.root)
		self.last_node = self.max(self.root)
		return rotation

	'''performs a right rotation arround input node.
			@return the "new root" after rotation which is the right child of input node'''

	def rightRotation(self, node):
		left_child = node.getLeft()
		new_left = left_child.getRight()
		parent = node.getParent()

		left_child.setRight(node)
		node.setLeft(new_left)

		# update heights and sizes
		node.setHeight(1 + max(node.getLeft().getHeight(), node.getRight().getHeight()))
		left_child.setHeight(1 + max(left_child.getLeft().getHeight(), left_child.getRight().getHeight()))
		node.setSize()
		left_child.setSize()


		# update parent pointers
		node.setParent(left_child)
		left_child.setParent(parent)
		new_left.setParent(node)

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
		new_right = right_child.getLeft()
		parent = node.getParent()

		right_child.setLeft(node)
		node.setRight(new_right)

		# update heights and sizes
		node.setHeight(1 + max(node.getLeft().getHeight(), node.getRight().getHeight()))
		right_child.setHeight(1 + max(right_child.getLeft().getHeight(), right_child.getRight().getHeight()))
		node.setSize()
		right_child.setSize()

		# update parent pointers

		node.setParent(right_child)
		right_child.setParent(parent)
		new_right.setParent(node)

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
		while parent and parent.isRealNode():
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

	"""///////////////////////////////////////////////////"""



