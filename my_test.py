from avl_template_new import AVLTreeList
from test_avl_skeleton import testAVLList

# inserts at start
test = testAVLList()

emptyList = AVLTreeList()
twentyTree = AVLTreeList()
twentylist = []

T = AVLTreeList()
L = []
for i in range(100):
    T.append(i)
    L.append(i)
cnt = 0
while not T.empty():
    print(cnt)
    test.compare_with_list_by_in_order(T, L)
    print("a")
    test.compare_with_list_by_retrieve(T, L)
    print("b")
    test.check_first(T, L)
    print("c")
    test.check_last(T, L)
    print("d")
    if cnt % 4 == 0:
        T.delete(T.length()//2)
        L.pop(len(L)//2)
    elif cnt % 4 == 1:
        T.delete(0)
        L.pop(0)
    elif cnt % 4 == 2:
        T.delete(T.length()-1)
        L.pop(len(L)-1)
    else:
        T.delete(T.length()//4)
        L.pop(len(L)//4)
    cnt += 1
print("e")
test.assertEqual(len(L), 0)

print("end")









