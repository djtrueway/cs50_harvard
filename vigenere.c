#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <math.h>
#include <stdio.h>
int main(int argc, string argv[])
{
    if (argc == 2)
    {
        for (int i = 0, n = strlen(argv[1]); i < n ; i++)
        {
            if (isdigit(argv[1][i]))
            {
                printf("error\n");
                return 1;
            }
        }

        printf("plaintext:  ");
        string s = get_string();

        string k = argv[1];

        printf("ciphertext: ");
        for (int i = 0, key = 0, n = strlen(s), p = strlen(k); i < n; i++)
        {
            if (isupper(s[i]))
            {
                printf("%c", ((s[i]) - 'A' + toupper(k[key]) - 'A') % 26 + 'A');
                key = (key + 1) % p;
            }
            else if (islower(s[i]))
            {
                printf("%c", ((s[i]) - 'a' + toupper(k[key]) - 'A') % 26 + 'a');
                key = (key + 1) % p ;
            }
            else
            {
                printf("%c", (s[i]));
            }
        }
        printf("\n");
    }
    else
    {
        printf("missing commande ligne argument\n");
        return 1;
    }
}

