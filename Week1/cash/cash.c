#include <cs50.h>
#include <math.h>
#include <stdio.h>

int main(void)
{

    // Calculate the number of cents.
    float change;
    int cents;
    do
    {
        change = get_float("Change owed: ");
        cents = round(change * 100);
    }
    while (cents <= 0);

    // Calculate the number of coins required to return.
    int counter = 0;
    while (cents > 0)
    {
        // Deduct quarter.
        if (cents >= 25)
        {
            cents = cents - 25;
        }
        // Deduct dime.
        else if (cents >= 10)
        {
            cents = cents - 10;
        }
        // Deduct nickel.
        else if (cents >= 5)
        {
            cents = cents - 5;
        }
        // Deduct penny.
        else
        {
            cents = cents - 1;
        }
        // Increment coin counter if a deduction is made.
        counter++;

    }

    printf("%i\n", counter);

}
