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
	def __init__(self, value):
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.size = 0
		self.height = -1
		

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

	"""returns the size of the subtree

		@rtype: int
		@returns: the height of self, -1 if the node is virtual
		"""
	def getSize(self):
		return self.size
	"""sets left child

	@type node: AVLNode
	@param node: a node
	"""
	def setLeft(self, node):
		self.height += 1
		self.size += 1
		self.left = node
		return None

	"""sets right child

	@type node: AVLNode
	@param node: a node
	"""
	def setRight(self, node):
		self.height += 1
		self.size += 1
		self.right = node
		return None

	"""sets parent

	@type node: AVLNode
	@param node: a node
	"""
	def setParent(self, node):
		node.setHight(node.getHight + 1)
		node.setSize(node.getSize + 1)
		self.parent = node
		return None

	def setSize(self, k):
		self.size = k
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
		return None

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def isRealNode(self):
		if self.height == -1:
			return False
		return True

	"""" BF() @return the Balance factor of a node
	"""
	def Bf(self):
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
		self.first = None
		self.last = None
		# add your fields here


	"""returns whether the list is empty

	@rtype: bool
	@returns: True if the list is empty, False otherwise
	"""
	def empty(self):
		return self.size == 0

	""""Tree-Select return the k'th smallest element in the list
	"""
	def treeSelect(T, k):
		def treeSelectRec(x,k):
			r = x.left.size + 1
			if k == r:
				return x
			elif k < r:
				return treeSelectRec(x.left,k)
			else:
				return treeSelectRec(x.right, k - r)
		return treeSelectRec(T.root,k)

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
		self.size += 1
		newNode = AVLNode(val)
		self._insert(newNode, i)
		self.root, rotation = self.balance(self.root)
		#self.update_sizes(self.root)
		return rotation

	def _insert(self, node, i):

		if i == self.length():
			max_node = self.max(self.root)
			max_node.setRight(node)
		else:
			# i < n
			nxt = self.treeSelect(i + 1)
			if not nxt.getLeft().isRealNode():
				nxt.setLeft(node)
			else:
				predecessor = self.max(nxt.getLeft())
				predecessor.setRight(node)



	def suc(self):
		pass

	def predecessor(self, node):
		pass

	def balance(self, node):
		rotations = 0
		if node.Bf() > 1:
			if node.getLeft().Bf() < 0:
				node.setLeft(self.leftRotation(node.getLeft()))
				rotations += 1
			node = self.rightRotation(node)
			rotations += 1
		elif node.Bf() < -1:
			if node.getRight().Bf() > 0:
				node.setRight(self.rightRotation(node.getRight()))
				rotations += 1
			node = self.leftRotation(node)
			rotations += 1

		return node, rotations



	'''update all sizes of the nodes'''

	def update_sizes(self, node):
		if node.isRealNode():
			self.update_sizes(node.getLeft())
			new_size = 1 + node.getLeft().getSize() + node.getLeft().getSize()
			node.setSize(new_size)
			self.update_sizes(node.getRight())



	"""deletes the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, i):
		if self.root is None:
			return -1
		virtual = AVLNode()
		# del_node is a pointer to the node we wish to delete
		del_node = self.treeSelect(self, i + 1)
		def simpleDelete(T, del_node):
			right_son = del_node.getLeft()
			left_son = del_node.getRight()
			parent = del_node.getParent()

			# Case 1: The node to delete has no children
			if (right_son is None or ( not right_son.isRealNode())) and (left_son is None or (not left_son.isRealNode())):
				if parent is None:
					self.root = None
					self.size = 0
				elif parent.getLeft() is del_node:
					parent.setLeft(virtual)

				else:
					parent.setRight(virtual)
				parent.setHeight(parent.getHeight() - 1)
				parent.setSize(parent.getSize() - 1)

			# Case 2: The node to delete has one child
			elif (right_son is None or ( not right_son.isRealNode())) or (left_son is None or (not left_son.isRealNode())):
				if parent is None:
					if left_son is not None:
						self.root = left_son
					else:
						self.root = right_son
					self.size = 1
					self.root.setSize(1)
				elif parent.getLeft() is del_node:
					if left_son is not None:
						parent.setLeft(left_son)
					else:
						parent.setLeft(right_son)
					parent.setSize(parent.getSize() - 1)
				else:
					if left_son is not None:
						parent.setRight(left_son)
					else:
						parent.setRight(right_son)
					parent.setSize(parent.getSize() - 1)
			else:
				return False
			return True
		not_case3 = simpleDelete(self, del_node)
		# Case 3: The node to delete has two children
		if not not_case3:
			# Find the successor node (the smallest node in the right subtree)
			node_succ = del_node.getRight()
			while node_succ.getLeft().isRealNode():
				node_succ = node_succ.getLeft()
			# The successor node have one or zero children
			simpleDelete(self,node_succ)
			# Replace del_node with his successor
			node_succ.setParent(del_node.getParent())
			node_succ.setLeft(del_node.getLeft())
			del_node.getLeft().setParent(node_succ)
			del_node.getRight(del_node.getRight())
			del_node.getRight().setParent(node_succ)
			if del_node.getParent().getLeft() is del_node:
				del_node.getParent().setLeft(node_succ)
			else:
				del_node.getParent().setRight(node_succ)



		return -1

	'''performs a right rotation arround input node.
		@return the "new root" after rotation which is the right child of input node'''

	def rightRotation(self, node):
		left_child = node.getLeft()
		node.setLeft(left_child.getRight())

		left_child.setRight(node)

		#update heights
		node.height = 1 + max(node.getLeft().getHeight(), node.getRight().getHeight())
		left_child.height = 1 + max(left_child.getLeft().getHeight(), left_child.getRight().getHeight())

		#update parent pointers
		node.setParent(left_child)
		left_child.setParent(node.getParent())

		parent = node.getParent()
		if parent.isRealNode():
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
		node.height = 1 + max(node.getLeft().getHeight(), node.getRight().getHeight())
		right_child.height = 1 + max(right_child.getLeft().getHeight(), right_child.getRight().getHeight())

		# update parent pointers
		node.setParent(right_child)
		right_child.setParent(node.getParent())

		parent = node.getParent()
		if parent.isRealNode():
			if parent.getLeft() == node:
				parent.setLeft(right_child)
			else:
				parent.setRight(right_child)

		return right_child


	"""returns the first node of subtree (or sublist) rooted at node
	@rtype : AVLNode"""

	def min(self, node):
		current = node
		while current.left.isRealNode():
			current = current.left
		return current

	"""returns the last node of subtree (or sublist) rooted at node
		@rtype : AVLNode"""

	def max(self, node):
		current = node
		while current.right.isRealNode():
			current = current.left
		return current


	"""returns the value of the first item in the list

	@rtype: str
	@returns: the value of the first item, None if the list is empty
	"""
	def first(self): #Min
		node = self.min(self.root)
		return node.getValue()



	"""returns the value of the last item in the list

	@rtype: str
	@returns: the value of the last item, None if the list is empty
	"""
	def last(self): #Max
		node = self.max(self.root)
		return node.getValue()

	"""returns an array representing list 

	@rtype: list
	@returns: a list of strings representing the data structure
	"""
	def listToArray(self):
		lst = []
		self.lst_to_arr_rec(self.root, lst)
		return lst

	def lst_to_arr_rec(self, node, lst):
		if ~node.isRealNode():
			return
		self.lst_to_arr_rec(node.left, lst)
		lst.append(node.getValue())
		self.lst_to_arr_rec(node.right, lst)
		return None

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
		return None

	"""permute the info values of the list 

	@rtype: list
	@returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
	"""
	def permutation(self):
		stack = [self.root]
		perm = AVLTreeList()
		i = 0
		while len(stack) > 0:
			node = stack.pop()
			perm.insert(i, node.getValue())
			i += 1
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
		return perm




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
	def search(self, val):
		return None



	"""returns the root of the tree representing the list

	@rtype: AVLNode
	@returns: the root, None if the list is empty
	"""
	def getRoot(self):
		return None


"class Tester():"


