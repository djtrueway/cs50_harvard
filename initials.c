#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    //input
    string s = get_string();
        for (int i = 0 , n = strlen(s); i < n ; i++ )
        {
            if(i == 0)
            {
                printf("%c", toupper(s[0]));  
            }
            else if (s[i] == ' ')
            {
                printf("%c", toupper(s[i+1]));
            }
            
        }
    printf("\n");
} 