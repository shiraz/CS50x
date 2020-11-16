#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get the height.
    int height;
    do
    {
        height = get_int("Select a height between 1 and 8: ");
    }
    while (height <= 0 || height >= 9);

    // Print out the rest of the hashes.
    for (int i = 0; i < height; i++)
    {
        // Insert space based on calculated logic.
        int dotNum = height - (i + 1);
        for (int k = 0; k < dotNum; k++)
        {
            printf(" ");
        }
        // Insert/add hashes.
        printf("#");
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }
        printf("\n");
    }

}
