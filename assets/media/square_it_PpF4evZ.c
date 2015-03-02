#include<stdio.h>
int main(){
    int num;
    float y;
    scanf("%d",&num);
    int i;
    i=0;
    for(i;i<num;++i){
        scanf("%f",&y);
        printf("%f\n",y*y);
    }
}
