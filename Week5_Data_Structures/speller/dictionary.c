// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = LENGTH *'z';

// Total words.
unsigned int word_count = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash word to obtain a hash value.
    int hash_value = hash(word);

    // Access linked list at that index in the hash table.
    // Start with cursor set to the first item in linked list.
    node *cursor = table[hash_value];

    // Keep moving cursor until you get to NULL, checking each node for the word.
    while (cursor != NULL)
    {
        // Traverse linked list, looking for the word (strcasecmp).
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }

        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int total = 0;

    for (int i = 0; i < strlen(word); i++)
    {
        total += tolower(word[i]);
    }

    return (total % N);
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open up the dictionary file.
    FILE *dictionary_file_pointer = fopen(dictionary, "r");
    // Check if the dictionary can be opened for reading.
    if (dictionary_file_pointer == NULL)
    {
        printf("Cannot open the dictionary %s for reading.\n", dictionary);
        return 1;
    }

    char word[LENGTH + 1];

    // Read strings from the file one at a time.
    while (fscanf(dictionary_file_pointer, "%s", word) != EOF)
    {
        // Create a new node for each word.
        // Use malloc.
        node *word_node = malloc(sizeof(node));
        // Remember to check if return value is NULL.
        if (word_node == NULL)
        {
            return false;
        }

        // Copy word into node using strcpy.
        strcpy(word_node->word, word);

        // Hash word to obtain a hash value.
        int word_hash = hash(word);

        // Insert node into hash table at that location.
        if (table[word_hash] == NULL)
        {
            word_node->next = NULL;
        }
        else
        {
            word_node->next = table[word_hash];
        }
        table[word_hash] = word_node;

        // Increment word count. Easier to implement size method this way.
        word_count++;

    }

    fclose(dictionary_file_pointer);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Go through each linked list in the hash table.
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        node *temp = cursor;

        while (cursor != NULL)
        {
            // Go to the next node.
            cursor = cursor->next;
            // Free the memory of the current node.
            free(temp);
            // Update the temp variable (the one that clears memory) with the next node.
            temp = cursor;
        }

        // Check to see if all nodes are cleared.
        if (cursor == NULL && i == N - 1)
        {
            return true;
        }

    }
    return false;
}
