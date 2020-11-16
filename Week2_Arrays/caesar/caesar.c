#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{

    // Check if arguments were passed correctly.
    if (argc != 2 || strcmp(argv[1], "0") == 0)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Check to see if the key argument is valid and only numbers. This is done to prevent exceptions.
    string argKey = argv[1];
    for (int i = 0, n = strlen(argKey); i < n; i++)
    {
        if (!isdigit(argKey[i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    // Convert the key argument to an int.
    int key = atoi(argKey);

    // Get the plain text.
    string plainTxt = get_string("plaintext: ");

    for (int i = 0, n = strlen(plainTxt); i < n; i++)
    {
        if (isalpha(plainTxt[i]))
        {
            // Rotate the character.
            int rotate = plainTxt[i] + key;
            int maxAsciiNum = isupper(plainTxt[i]) ? 90 : 122;
            // If an overflow occurs, execute the wraparound logic.
            if (rotate > maxAsciiNum)
            {
                // Store the index mapping based on whether the character is upper case or lower case.
                int asciiIndexDiff = isupper(plainTxt[i]) ? 65 : 97;
                // Calculate the new character index, rotate the character and revert it back to the original ASCII index.
                int newPlainTxtCharInt = plainTxt[i] - asciiIndexDiff;
                int calcNewIndex = (newPlainTxtCharInt + key) % 26;
                rotate = calcNewIndex + asciiIndexDiff;
            }
            // Store the rotated character.
            plainTxt[i] = rotate;
        }

    }

    printf("ciphertext: %s", plainTxt);
    printf("\n");
    return 0;
}