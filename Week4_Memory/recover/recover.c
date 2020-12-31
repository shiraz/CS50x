#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Check if arguments were passed correctly.
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open the memory card.
    char *memory_card = argv[1];
    FILE *memory_card_file_pointer = fopen(memory_card, "r");

    // Check if the memory card can be opened for reading.
    if (memory_card == NULL)
    {
        printf("Cannot open %s for reading.\n", memory_card);
        return 1;
    }

    FILE *jpg_file_pointer = NULL;
    int bytes_size = 512;
    unsigned char bytes[bytes_size];
    int count = 0;
    int found = 0;

    // Repeat until end of card. Read 512 bytes at a time.
    while (fread(&bytes, bytes_size, 1, memory_card_file_pointer))
    {
        // Look for jpg file.
        if (bytes[0] == 0xff && bytes[1] == 0xd8 && bytes[2] == 0xff && (bytes[3] & 0xf0) == 0xe0)
        {
            if (found == 1)
            {
                // Close the previous jpg file since a new one has been detected.
                fclose(jpg_file_pointer);
            }
            // Special case for the first jpg file.
            else
            {
                found = 1;
            }
            // Create a new jpg output file.
            char current_jpg_file_name[100];
            sprintf(current_jpg_file_name, "%03i.jpg", count);
            jpg_file_pointer = fopen(current_jpg_file_name, "w");
            count++;
        }

        // Write to the jpg file if detected in bytes.
        if (found)
        {
            fwrite(&bytes, bytes_size, 1, jpg_file_pointer);
        }

    }

    // Close the jpg output file and memory card.
    fclose(jpg_file_pointer);
    fclose(memory_card_file_pointer);

    return 0;

}
