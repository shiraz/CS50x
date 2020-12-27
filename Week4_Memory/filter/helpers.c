#include "helpers.h"
#include <math.h>

int get_sepia_value(RGBTRIPLE pixel, char color_code);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            RGBTRIPLE current_pixel = image[h][w];
            int r = current_pixel.rgbtRed;
            int g = current_pixel.rgbtGreen;
            int b = current_pixel.rgbtBlue;
            // Calculate the average gray color value of the pixel.
            int gray_color = round((r + g + b) / 3.0);
            // Replace the RGB values with the above calculated "gray" value.
            image[h][w].rgbtRed = gray_color;
            image[h][w].rgbtGreen = gray_color;
            image[h][w].rgbtBlue = gray_color;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            int sepia_red = get_sepia_value(image[h][w], 'r');
            int sepa_green = get_sepia_value(image[h][w], 'g');
            int sepia_blue = get_sepia_value(image[h][w], 'b');
            image[h][w].rgbtRed = sepia_red;
            image[h][w].rgbtGreen = sepa_green;
            image[h][w].rgbtBlue = sepia_blue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width / 2; w++)
        {
            RGBTRIPLE tmp = image[h][w];
            // Switch the positions of pixels from left to right and vice versa.
            int shift_width = width - w - 1;
            image[h][w] = image[h][shift_width];
            image[h][shift_width] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE image_copy[height][width];
    int positions_length = 3;

    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            double r_sum = 0;
            double g_sum = 0;
            double b_sum = 0;
            int pixel_count = 0;

            // Arrays of nearby pixel positions.
            int width_positions[] = {w - 1, w, w + 1};
            int height_levels[] = {h - 1, h, h + 1};

            for (int hp = 0; hp < positions_length; hp++)
            {
                for (int p = 0; p < positions_length; p++)
                {
                    int current_height = height_levels[hp];
                    int current_width = width_positions[p];
                    // Check to see if the surrounding pixels are valid.
                    int check_width = current_width < width && current_width >= 0;
                    int check_height = current_height < height && current_height >= 0;
                    // For all pixels around current one (in the confines of 1 pixel over/under/across/left/right), calculate the total RGB values.
                    if (check_height && check_width)
                    {
                        pixel_count++;
                        r_sum += image[current_height][current_width].rgbtRed;
                        g_sum += image[current_height][current_width].rgbtGreen;
                        b_sum += image[current_height][current_width].rgbtBlue;
                    }
                }
            }

            // Calculate the average of the aggregate RGB values with respect to the pixel counter.
            image_copy[h][w].rgbtRed = round(r_sum / pixel_count);
            image_copy[h][w].rgbtGreen = round(g_sum / pixel_count);
            image_copy[h][w].rgbtBlue = round(b_sum / pixel_count);
        }
    }

    // Replace the pixels in the original image with the new "blurred" calculated ones.
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            image[h][w] = image_copy[h][w];
        }
    }

    return;
}

int get_sepia_value(RGBTRIPLE pixel, char color_code)
{
    int sepia_value = 0;
    int r = pixel.rgbtRed;
    int g = pixel.rgbtGreen;
    int b = pixel.rgbtBlue;

    // Calculate the sepa values based on the given formulae.
    switch (color_code)
    {
        case 'r':
            sepia_value = round((0.393 * r) + (0.769 * g) + (0.189 * b));
            break;

        case 'g':
            sepia_value = round((0.349 * r) + (0.686 * g) + (0.168 * b));
            break;

        case 'b':
            sepia_value = round((0.272 * r) + (0.534 * g) + (0.131 * b));
            break;

    }

    // If the calculated value is over 255, return 255.
    return sepia_value > 255 ? 255 : sepia_value;
}
