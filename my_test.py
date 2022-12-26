from avl_template_new import AVLTreeList

T = AVLTreeList()
for i in range(100):
    T.insert(0, str(i))
T.printt()

print("start size:", T.length())
print("First: ", T.first())
print("Last: ", T.last())

T.delete(1)
T.printt()
print("start size:", T.length())
print("First: ", T.first())
print("Last: ", T.last())

T.delete(1)
T.printt()
print("start size:", T.length())
print("First: ", T.first())
print("Last: ", T.last())

T.delete(0)
T.printt()
print("start size:", T.length())
print("First: ", T.first())
print("Last: ", T.last())

T.delete(96)
T.printt()
print("start size:", T.length())
print("First: ", T.first())
print("Last: ", T.last())
#
# for i in range(99):
#     if i % 5 == 0:
#         print("i = " + str(i))
#         T.delete(0)
#     elif i % 5 == 1:
#         print("i = " + str(i))
#         T.printt()
#         T.delete(T.length() - 1)
#     elif i % 5 == 2:
#         print("iiii = " + str(i))
#         print(T.length(), "size")
#         T.delete((T.length() - 1) // 2)
#     elif i % 5 == 3:
#         print("i = " + str(i))
#         T.delete((T.length() - 1) // 3)
#     else:
#         print("i = " + str(i))
#         T.delete((T.length() - 1) // 7)











