import argparse
import re
from math import sqrt, floor

indexes = ["", "6", "7", "9", "10", "11", "12", "13", "14", "15", "16",
           "17", "18","22", "25"]

vowels = ['a', 'e', 'i', 'o', 'u', 'y']


def syllable_count(word):
    word = word.strip(",.!?;:").lower()
    n_syllables = 0
    if word[-1] == "e":
        word = word[:-1]
    previous_letter = None
    for i, letter in enumerate(word):
        if letter in vowels and (i == 0 or previous_letter not in vowels):
            n_syllables += 1
        previous_letter = letter
    if n_syllables < 1:
        n_syllables = 1
    return n_syllables


parser = argparse.ArgumentParser(description="This program prints Readability index")
parser.add_argument("--infile", "--infile", help="Pass a file which contains text")
parser.add_argument("--words", "--words", help="Pass a file which contains difficult words")

args = parser.parse_args()
file_name = args.infile
text = ""
with open(file_name) as f:
    for line in f:
        text += line
with open(args.words) as d:
    difficult_words = d.read().split()
print("The text is:")
print(text)
characters = sum(1 for c in line if c not in ('\n', ' ', '\t'))
sentences = re.split('[!.?]', text)
num_of_sent = 0
words = 0
syllable = 0
poly = 0
difficult_word = 0
for sentence in sentences:
    if sentence:
        words += len(sentence.split())
        num_of_sent += 1
        for w in sentence.split():
            if w.strip(" ,.?!:;)(").lower() not in difficult_words:
                difficult_word += 1
            c = syllable_count(w.strip(",.!:;?"))
            if c > 2:
                poly += 1
            syllable += c
ari_score = 4.71 * (characters / words) + 0.5 * (words / num_of_sent) - 21.43
fk_score = 0.39 * (words / num_of_sent) + 11.8 * (syllable / words) - 15.59
smog_score = 1.043 * sqrt((poly * 30) / num_of_sent) + 3.1291
colman_score = (0.0588 * ((characters / words) * 100)) - (0.296 * ((num_of_sent / words) * 100)) - 15.8
pb_score = 0.1579 * (difficult_word / words) * 100 + 0.0496 * (words / num_of_sent)
if (difficult_word / words) * 100 > 5:
    pb_score += 3.6365
print("Words:", words)
print("Difficult words:", difficult_word)
print("Sentences:", num_of_sent)
print("Characters:", characters)
print("Syllables:", syllable)
print("Polysyllables:", poly)
choice = input("Enter the score you want to calculate (ARI, FK, SMOG, CL, PB, all): ")
if choice == "ARI" or choice == "all":
    age_ari = indexes[min(round(ari_score), 14)]
    print("\nAutomated Readability Index:", round(ari_score, 2),
          f"(about {age_ari}-year-olds)")
if choice == "FK" or choice == "all":
    age_fk = indexes[min(round(fk_score), 14)]
    print("Flesch–Kincaid readability Index:", round(fk_score, 2),
          f"(about {age_fk}-year-olds)")
if choice == "SMOG" or choice == "all":
    age_sm = indexes[min(round(smog_score), 14)]
    print("Simple Measure of Gobbledygook:", round(smog_score, 2),
          f"(about {age_sm}-year-olds)")
if choice == "CL" or choice == "all":
    age_cl = indexes[min(round(colman_score), 14)]
    print("Coleman–Liau index:", round(colman_score, 2),
          f"(about {age_cl}-year-olds)")
if choice == "PB" or choice == "all":
    year = 0
    score = round(pb_score, 1)
    if score <= 4.9:
        year = 10
    elif score < 6:
        year = 12
    elif score < 7:
        year = 14
    elif score < 8:
        year = 16
    elif score < 9:
        year = 18
    elif score < 10:
        year = 24
    else:
        year = 25
    print("Probability-based score:", round(pb_score, 2), f"(about {year}-year-olds)")
print("This text should be understood in average by",
      (int(age_ari) + int(age_fk) + int(age_cl) + int(age_sm) + year) / 5, "year olds.")
