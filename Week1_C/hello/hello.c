#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Ask the user for a name.
    string name = get_string("What is your name?\n");
    // Use the above name in the hello string.
    printf("hello, %s\n", name);
}
