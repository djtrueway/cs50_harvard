#include <stdio.h>
#include <cs50.c>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if (argc == 2)
    {
        int k = atoi(argv[1]);
        // ask user the plaintext
        char s[100];
        printf("plaintext:  ");
        scanf("%s", s);

        printf("ciphertext: ");
        // loop over the plaintext to generate the ciphertext
        for (int i = 0, n = strlen(s); i < n ; i++)
        {
            if (isupper(s[i])) // Z - A + key % 26
            {
                printf("%c", ((s[i] - 'A' + k) % 26 + 'A'));
            }
            else if (islower(s[i]))
            {
                printf("%c", ((s[i] - 'a' + k) % 26 + 'a'));
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
        printf("Usage: ./caesar k\n");
        return 1;
    }
}