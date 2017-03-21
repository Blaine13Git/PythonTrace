# 取商
print("商是：")
print(5 // 2)

# 取余数
print("余数是：")
print(5 % 2)

# 进制转换
print(0xAF)
# 175
print(0o10)
# 8
print(0b1011010010)
# 722

# 输入
# a = input("a = ")
# print(a)

# if
if 1 == 2:
    print("1等于1")
else:
    print("没啥")

# n次方
print(2 ** 8)
print(pow(2, 3))

# index
name = "Blaine"
print(name[-1])
print(name[1])
print(name[1:3])

full_name = "Blaine.Lion"
print(len(full_name))
print(full_name[-4:len(full_name)])

# 打开（新建）文件，写入内容
# my_file = open("test.txt", "w")
# my_file.write("qwert\n")
# my_file.write("123321")
# my_file.close()

read_file = open("test.txt", "r")
print(read_file.read(2))
