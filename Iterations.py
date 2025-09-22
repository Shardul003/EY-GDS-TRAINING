def multiplications(num):
    print (f" Multiplication of {num})"
    for i in range (1,11):
    print (f"{num} X {i}= {num*i})"
n=int(input("ENTER A NUMBER"))
obj=multiplications(n)
print(obj)