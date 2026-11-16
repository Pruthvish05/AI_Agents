#include <stdio.h>
#include <setjmp.h>
jmp_buf buffer;
void function()
{
printf("inside function\n");
longjmp(buffer,1);
}
int main()
{
if(setjmp(buffer)==0)
{
printf("First Execution\n");
function();
}
else
{
printf("Return using longjmp\n");
}
return 0;
}

