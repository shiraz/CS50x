#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    string text = get_string("Text: ");
    int letters = 0;
    int words = 0;
    int sentences = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char letter = text[i];

        // Count the number of letters.
        if (isalpha(letter))
        {
            letters = letters + 1;
        }

        // Count the number of words.
        if (isspace(letter))
        {
            words = words + 1;
        }

        int is_end_of_sentence = text[i] == '.' || text[i] == '!' || text[i] == '?';

        // Count the number of sentences.
        if (is_end_of_sentence)
        {
            sentences = sentences + 1;
        }
    }

    words = words + 1;

    // Calculate the Coleman-Liau index.
    float calculatedIndex = (0.0588 * letters / words * 100) - (0.296 * sentences / words * 100) - 15.8;
    int index = round(calculatedIndex);

    // Output the correct statement based on the above calculated index.
    if (index < 0)
    {
        printf("%s\n", "Before Grade 1");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("%s %i\n", "Grade", index);
    }
}