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
		self.height = 1 + max(node.getLeft().getHeight(), node.getRight().getHeight())
		self.size += 1
		self.left = node


	"""sets right child

	@type node: AVLNode
	@param node: a node
	"""
	def setRight(self, node):
		self.height = 1 + max(node.getLeft().getHeight(), node.getRight().getHeight())
		self.size += 1
		self.right = node


	"""sets parent

	@type node: AVLNode
	@param node: a node
	"""
	def setParent(self, node):
		#node.setHight(node.getHight + 1)
		#node.setSize(node.getSize + 1)
		self.parent = node


	def setSize(self):
		self.size = 1 + self.getRight().getSize() + self.getLeft().getSize()

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
	def setHeight(self):
		self.height = 1 + max(self.getLeft().getHeight(), self.getRight().getHeight())


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
		curr = newNode
		rotation = 0
		while curr != self.root:
			bf = curr.Bf()
			height = curr.getHeight()
			if abs(bf) > 1:
				curr, rot = self.balance(curr)
				rotation += rot
			if curr.getHeight() != height:
				curr.setHeight()
			curr.setSize()
			curr = curr.getParent()

		return rotation

	def _insert(self, node, i):

		if i == self.length():
			max_node = self.max(self.root)
			max_node.setRight(node)
			node.setParent(max_node)
			self.last = node
		else:
			# i < n
			if i == 0:
				self.first = node
			nxt = self.treeSelect(i + 1)
			if not nxt.getLeft().isRealNode():
				nxt.setLeft(node)
				node.setParent(nxt)
			else:
				predecessor = self.max(nxt.getLeft())
				predecessor.setRight(node)
				node.setParent(predecessor)



	def successor(self, node):
		if node.getRight().isRealNode():
			return self.min(node.getRight())
		parent = node.getParent()
		curr = node
		while parent.isRealNode():
			if parent.getRight() != curr:
				break
			curr = parent
			parent = curr.getParent()
		return parent


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

	'''balnces tree rooted in @input node- frot the root to the leaves
	@return is a tuple(AVLNode, int)
	@return[0] = top node after balancing
	@return[1] = number of rotations made'''

	def balance_top_bottom(self, node):
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

	'''balnces @input node
	@return is a tuple(AVLNode, int)
	@return[0] = top node after balancing
	@return[1] = number of rotations made'''

	def balance(self, node):
		balance = node.Bf()
		left_child = node.getLeft()
		right_child = node.getRight()
		rotations = 0

		# Left Left Case
		if balance > 1 and left_child.Bf() >= 0:
			node = self.rightRotation(node)
			rotations += 1

		# Left Right Case
		elif balance > 1 and left_child.Bf() < 0:
			new_left = self.leftRotation(left_child)
			node.setLeft(new_left)
			node = self.rightRotation(node)
			rotations += 2

		# Right Right Case
		elif balance < -1 and right_child.Bf() <= 0:
			node = self.leftRotation(node)
			rotations += 1

		# Right Left Case
		elif balance < -1 and right_child.Bf() > 0:
			new_right = self.rightRotation(right_child)
			node.setRight(new_right)
			node = self.leftRotation(node)
			rotations += 2

		return node, rotations



	"""deletes the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, i):
		if self.empty() or self.size < i or i < 0:
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

		self.min()
		self.max()
		return self.balance()

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
		return self.first.getValue()



	"""returns the value of the last item in the list

	@rtype: str
	@returns: the value of the last item, None if the list is empty
	"""
	def last(self): #Max
		self.last.getValue()

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
		self.quickSort(tree_valuse)
		for i in range(len(tree_valuse)):
			k = sorted_tree.size
			sorted_tree.insert(k,tree_valuse[i])
		return sorted_tree

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


class Tester():
	def test_insertion(self):
		tree = AVLTreeList()
		tree.insert(3)
		tree.insert(7)
		tree.insert(2)
		tree.insert(4)
		tree.insert(6)
		tree.insert(8)
		self.assertEqual(tree.value, 5)
		self.assertEqual(tree.left.value, 3)
		self.assertEqual(tree.right.value, 7)
		self.assertEqual(tree.left.left.value, 2)
		self.assertEqual(tree.left.right.value, 4)
		self.assertEqual(tree.right.left.value, 6)
		self.assertEqual(tree.right.right.value, 8)


