#include<stdio.h>
int main(){
    int num;
    int y;
    scanf("%d",&num);
    int i;
    i=0;
    for(i;i<num;++i){
        scanf("%d",&y);
        y=y*y;
        printf("%d\n",y);
    }
}
