def computeGCD(x, y):
    gcd=0
    if x > y:
        small = y
    else:
        small = x
    for i in range(1, small+1):
        if((x % i == 0) and (y % i == 0)):
            gcd = i
    return gcd


numbers = [iter for iter in range(31200)]
values=[]
for num in numbers:
    result = computeGCD(31200,num)
    if(result == 1):
        values.append(num)

print(values)
