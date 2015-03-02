#include<stdio.h>
int main(){
    int num;
    float y;
    scanf("%d",&num);
    int i;
    i=0;
    for(i;i<num;++i){
        scanf("%f",&y);
        y=y*y;
        int x;
        x=y;
        if(x==y)
            printf("%d\n",x);
        else:
            printf("%.2f\n",y*y);
    }
}
