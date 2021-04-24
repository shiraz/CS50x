while True:
    # Get the height.
    str_height = input("Select a height between 1 and 8: ")
    if str_height.isnumeric():
        height = int(str_height)

        if (height in range(1, 9)):
            break

# Print out the appropriate hashes.
for h in range(height):
    spaces_count = height - h - 1
    for s in range(spaces_count):
        print(' ', end='')
    hashes_count = h + 1
    print(hashes_count * '#')