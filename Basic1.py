def check_number(num):
    if num%2==0:
        return f"{num} is even"
    else:
        return f"{num} is odd"
n=int(input("ENTER A NUMBER"))
check=check_number(n)
print(check)