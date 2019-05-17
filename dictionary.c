// Implements a dictionary's functionality

#include <stdbool.h>


#include "dictionary.h"

typedef struct node
{
    char word[LENGTH + 1];
    struct node* next;
}
node;

// create array of pointer-to-nodes of size HASHTABLE_SIZE
node* hashtable[HASHTABLE_SIZE];

/**
 * Hash function via reddit user delipity:
 * https://www.reddit.com/r/cs50/comments/1x6vc8/pset6_trie_vs_hashtable/cf9nlkn
 */
int hash_it(char* needs_hashing)
{
    unsigned int hash = 0;
    for (int i=0, n=strlen(needs_hashing); i<n; i++)
        hash = (hash << 2) ^ needs_hashing[i];
    return hash % HASHTABLE_SIZE;
}

bool load2 = false;

int count = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int size = strlen(word);
    char word_n[size + 1];

    for (int i = 0 ; i < size; i++)
    {
        word_n[i] = tolower(word[i]);
    }

    word_n[size] = '\0';

    //hast it the word in dictionary
    int h = hash_it(word_n);
    node *cursor = hashtable[h];

    while(cursor != NULL)
    {
        if(strcmp(word_n ,cursor->word ) == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }
    // it's not in table 
    return false;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //put hashtable to NULL
    for(int i = 0; i < HASHTABLE_SIZE; i++)
    {
        hashtable[i] = NULL;
    }
    // open the dictionary
    FILE *ptr = fopen(dictionary, "r");
    if (ptr == NULL)
    {
        fprintf(stderr, "file does not exist!");
        return false;
    }
    char words[LENGTH + 1];
    node *head = NULL;

    //read word by word in dictionary !!
    while (fscanf(ptr,"%s" ,words) != EOF)
    {
        //malloc for new list
        node* new_node = malloc(sizeof(node));

        //check is malloc success
        if(new_node == NULL)
        {
            fprintf(stderr,"malloc faill!\n");
            return false;
        }

        //copy word into node
        strcpy(new_node->word, words);

        //next egal to NULL!!
        new_node->next = NULL;

        //word to hash fonction
        int z = hash_it(words);
        hashtable[z] = head;

        // check for empty list
        if (head == NULL)
        {
            hashtable[z] = new_node;
        }
        else 
        {
            new_node->next = hashtable[z];
            hashtable[z] = new_node;
        }
            //count word !!!!
        count++;
    }
    fclose(ptr);
    load2 = true;
    return true;

}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if(load2)
    {
    return count;
    }
    else
    {
    return 0;
    }
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < HASHTABLE_SIZE; i++)
    {
        node *cursor = hashtable[i];
        while(cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    // TODO
    load2 = false;
    return true;
}
