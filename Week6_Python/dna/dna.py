import csv
import os.path
import sys


def main():
    # Ensure correct usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # Check if argument paths are valid.
    check_paths = os.path.isfile(sys.argv[1]) and os.path.isfile(sys.argv[2])
    if not check_paths:
        sys.exit('No match')

    # Open the CSV file and DNA sequence, then read contents into memory.
    with open(sys.argv[1], newline='') as csv_file, open(sys.argv[2], "r") as txt_file:
        reader = csv.DictReader(csv_file)
        dna_sequence = get_text(txt_file)
        str_headers = get_str_headers(reader)
        str_counts = get_str_count_obj(dna_sequence, str_headers)
        # Compare the STR counts against each row in the CSV file.
        results = get_str_db_comparision_results(reader, str_counts)
        print(results)


def get_str_count(dna, str_seq):
    dna_len = len(dna)
    str_seq_len = len(str_seq)
    index = 0
    counts = []
    str_count = 0
    last_index = 0

    # For each STR, compute the longest run of the consecutive repeats in the DNA sequence.
    # For each position in the sequence, compute how many times the STR repeats starting at that position.
    while index < dna_len:
        if index == 0:
            index = dna.find(str_seq)
        else:
            last_index = index
            index = dna.find(str_seq, index, index + str_seq_len)

        # For each position, keep checking successive substrings until the STR repeats no longer.
        if index > -1:
            str_count = str_count + 1
            index = index + str_seq_len
        else:
            if str_count > 0:
                counts.append(str_count)
            str_count = 0
            index = last_index + 1

    if len(counts) > 0:
        highest_str_repeat_count = max(counts)
        return highest_str_repeat_count
    return 0


def get_str_count_obj(dna, headers):
    str_count_obj = {}
    # For each STR header, get the repeated counts and store it in a data structure.
    for header in headers:
        header_str_count = get_str_count(dna, header)
        str_count_obj[header] = str(header_str_count)
    return str_count_obj


def get_str_db_comparision_results(reader, str_counts):
    # For each person in the database, compare the STR counts and output the person that matches the counts.
    for row in reader:
        name = row.pop("name")
        if str_counts == row:
            return name
    return "No match"


def get_str_headers(reader):
    # Get the STR headers from the reader. We are creating a copy so that the "name" header is not removed by reference.
    str_headers = reader.fieldnames.copy()
    str_headers.remove("name")
    return str_headers


def get_text(txt_file):
    final_text = ""
    # Grab the text without the extra line and return it.
    for line in txt_file:
        stripped_line = line.rstrip()
        if stripped_line:
            final_text = final_text + stripped_line
    return final_text


if __name__ == "__main__":
    main()
