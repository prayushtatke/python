#!/usr/bin/python

str = raw_input("Enter String: ")

prev_letter = None
curr_letter = None
letter_counts = {}

for ch in str:
    if letter_counts.has_key(ch):
        letter_counts[ch] = letter_counts.get(ch) + 1
    else:
        letter_counts[ch] = 1

print letter_counts
