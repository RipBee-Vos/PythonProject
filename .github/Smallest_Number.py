# Equal ==
# Not equal !=
# Greater than >
# Less than <
# Greater than or equal >=
# Less than or equal <=
# And
# Or

input1 = int(input())
input2 = int(input())
input3 = int(input())

if int(input1) <= int(input2) and int(input1) <= int(input3):
    print(int(input1))

elif int(input2) <= int(input1) and int(input2) <= int(input3):
    print(int(input2))

elif int(input3) <= int(input1) and int(input3) <= int(input2):
    print(int(input3))

else:
    Print(input1)