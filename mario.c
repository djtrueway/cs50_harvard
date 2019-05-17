#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;
    do
    {
        printf("heights of wall:");
        height = get_int();
    }
    while ((height < 0) || (height > 23));

    for (int i = 1; i <= height ; i++)
    {
        for (int b = 0; b <= height ; b++)
        {
            if ((i + b) < height)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        printf("\n");
    }
}