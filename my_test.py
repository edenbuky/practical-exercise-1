from avl_template_new import AVLTreeList
from test_avl_skeleton import testAVLList

# inserts at start
test = testAVLList()

emptyList = AVLTreeList()
twentyTree = AVLTreeList()
twentylist = []

T = AVLTreeList()

for i in range(500):
    if i % 3 == 0:
        T.insert(T.length()//2, i)
    elif i % 3 == 1:
        T.insert(0, i)
    else:
        T.delete(T.length()//2)
    test.in_order(T, T.getRoot(), test.check_BF)











