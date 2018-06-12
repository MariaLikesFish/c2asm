
int main()
{
    int a;
    int b;
    int c;
    int *p;
    a=1;
    p=&a;

    a=+1;
    a=-1;
    a=sizeof(int);
    a=sizeof(double);
    a=sizeof(float);
    a=sizeof(char);

    a=3==7;
    a=3!=7;
    b=3;
    c=7;
    a=b==c;
    a=b!=c;
    a=b==7;
    a=3!=c;
    a=b>c;
    a=b>=c;
    a=b<c;
    a=b<=c;

    return 0;
}

