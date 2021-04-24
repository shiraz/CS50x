import math

# Function to return float.


def get_float(value):
    try:
        return float(value)
    except ValueError:
        return None


# Get the change.
while True:
    str_change = input("Change owed: ")

    cents = get_float(str_change)

    if cents is not None:
        cents = round(cents * 100)
        if (cents > 0.0):
            break

counter = 0

while (cents > 0):

    # Deduct quarter.
    if (cents >= 25):
        cents = cents - 25
    # Deduct dime.
    elif (cents >= 10):
        cents = cents - 10
    # Deduct nickel.
    elif (cents >= 5):
        cents = cents - 5
    # Deduct penny.
    else:
        cents = cents - 1

    # Increment coin counter if a deduction is made.
    counter += 1

print(counter)