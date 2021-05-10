import re

# Get the text.
text = input("Text: ")

# Count the number of letters in the text.
num_letters = sum(x.isalpha() for x in text)

# Count the number of words in a sentence.
num_words = sum(x.isspace() for x in text) + 1
# Calculate the average letters per words.
avg_letters_count_per_words = num_letters / num_words
# Calculate the average number of letters per 100 words.
avg_letters_count_per_100_words = avg_letters_count_per_words * 100

# Count the number of sentences.
num_sentences = len(re.findall('[.!?]+', text))
# Calculate the average number of sentences per words.
avg_sentences_count_per_words = num_sentences / num_words
# Calculate the average number of sentences per 100 words.
avg_sentences_count_per_100_words = avg_sentences_count_per_words * 100

coleman_index = 0.0588 * avg_letters_count_per_100_words - 0.296 * avg_sentences_count_per_100_words - 15.8
index = round(coleman_index)

if index < 1:
    grade = "Before Grade 1"
elif index >= 16:
    grade = "Grade 16+"
else:
    grade = "Grade {0}".format(index)

print(num_letters, "letter(s)")
print(num_words, "word(s)")
print(num_sentences, "sentence(s)")
print("Average letters count per words:", avg_letters_count_per_words)
print("Average letters count per 100 words:", avg_letters_count_per_100_words)
print("Average sentences count per words:", avg_sentences_count_per_words)
print("Average sentences count per 100 words:", avg_sentences_count_per_100_words)
print(grade)
