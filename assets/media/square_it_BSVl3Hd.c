#include<stdio.h>
int main(){
    int num;
    float y;
    scanf("%d",&num);
    for(int i=0;i<num;++i){
        scanf("%f",&y);
        printf("%f\n",y*y);
    }
}
