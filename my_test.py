from avl_template_new import AVLTreeList
from test_avl_skeleton import testAVLList

t = testAVLList()
L = []
T = AVLTreeList()

for i in range(10):
    T.insert(0, i)
    L.append(i)
perm1 = T.permutation()
perm2 = T.permutation()
perm3 = T.permutation()

perm1.printt()
perm2.printt()
perm3.printt()
print("end")









