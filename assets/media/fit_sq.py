t=int(input())
while t>0:
    b=eval(input())
    if b<4:print('0')
    else:
        n=int((b-2)/2)
        s=0
        for i in range(n):
            s+=(i+1)
        print(s)
    t-=1
