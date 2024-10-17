{
int i;
int n;
int f;
n = 10;
i = 2;
f = 1;
if(n==5){
printf(1);
}
else{
    n = 5;
}
while (i < n + 1) {
f = f * i;
i = i + 1;
}
printf(f);
}