// Modifies the volume of an audio file

#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // Read the header from the input file
    uint8_t bytes[HEADER_SIZE];
    fread(&bytes, HEADER_SIZE, 1, input);

    // Write the header to the output file
    fwrite(&bytes, HEADER_SIZE, 1, output);

    int16_t sample_bytes;
    
    while (fread(&sample_bytes, sizeof(int16_t), 1, input))
    {
        // Read the sample from the input file
        // Multiply the sample value by the volume factor
        int16_t new_sample_bytes = sample_bytes * factor;

        // Write the new sample to the output file
        fwrite(&new_sample_bytes, sizeof(int16_t), 1, output);
    }


    // Close files
    fclose(input);
    fclose(output);
}
