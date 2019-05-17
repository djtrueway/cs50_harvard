#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int water;
    do
    {
        printf("minutes : ");
        water = get_int();
    }
   while (water <= 0);
   
   int bottle = 12;
   {
       printf("bottles : %i\n", water*bottle);
   }
}
