t=int(input())
for _ in range(T):
    n=int(input())
    idsum=0
    chldsum=0
    for _ in range(n):
       nid,nsum=input().split()
       idsum+=int(nid)
       chldsum+=int(nsum)
    print(idsum-chlesum)
