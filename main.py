# Author: Breanna Rhodes
import csv

from empath import Empath
import pandas as pd
import operator
import numpy as np
from collections import Counter

# Intro of using Empath
# Create an Empath object that contains the 200 built-in categories
lexicon = Empath()

# Categories can also be added to the lexicon using create_category method
# The first argument should be the category, and the second should be a list of key words associated with that category
# Empath will also create other key words associated with that category using fictional text from online sources
# lexicon.create_category('colors', ['red', 'blue', 'yellow'])

# Empath can then analyze the text based on that particular category
# print(lexicon.analyze('yellow jump cool umbrella', categories=['colors'], normalize=True))
# Output: colors: 0.25  --> 25% of the text has to do with colors
# Taking away normalize will lead to just the number of words associated with that category


# Empath creates categories from fictional text, the ny times and reddit, this can be specified on the call line
# lexicon.create_category('inauguration', ['inauguration'], model='nytimes', size=10)
# Generates a list of keywords associated with inauguration based on contexts from the ny times
# Can also adjust the size of the word bank of the key words (size=10)
# This will result in the most closely related words to the category



print('\n\nAnalyzing Data with Empath\n\n')


# Applying Empath to the data_incl_demographics filtered_SMALL.csv
df = pd.read_csv('rwwd_full.csv')
text_long_df = df['text_long']
emotion_df = df['chosen_emotion']
categories_list = ['anger', 'disgust',
                   'fear', 'anxiety',
                   'sadness', 'happiness',
                   'relaxation', 'desire']


print('\n****Categories of emotions being created based on the seed word of the category****\n')

# First the categories need to be added to the lexicon along with their seeds for keywords
# I limited the size to 35 words because having too many generations through the loop was causing errors
emotion_list = df['chosen_emotion'].unique()
for i in emotion_list:
    lexicon.create_category(i, [i], size= 35)

# Relaxation couldn't be built from the seed word relaxation, so it needs to be manually put in
lexicon.create_category('relaxation', ['calm', 'composure'], size=35)
empath_list = []
print('\n****Analysis of emotion in each text_long****')
# Running Empath with the first 1000 lines of the CSV shows the number of times that emotion appears in the text
for i in range(1000):
    empath_list.append(lexicon.analyze(text_long_df[i],
                                                    categories=['anger', 'disgust',
                                                                'fear', 'anxiety',
                                                                'sadness', 'happiness',
                                                                'relaxation', 'desire']))
counter = 1
max_emotion = []
rate_empath = []
initial_rating = []

for i in empath_list:
    max_emotion.append(max(i.items(), key=operator.itemgetter(1))[0])
    rate_empath.append(max(i.items(), key=operator.itemgetter(1))[1])
    print('\ntext_long # ', counter, ': ', i)
    if max(i.items(), key=operator.itemgetter(1))[1] == 0.0:
        print('no emotion could be determined using Empath')
    else:
        print('Strongest emotion of text_long # ', counter, ': ', max(i.items(), key=operator.itemgetter(1)))
        print('Determined emotion: ', max(i, key=i.get))
    counter += 1

counts = 0
for i in max_emotion:
    initial_rating.append(df[i][counts])
    counts+=1

emotion_counter = Counter(max_emotion)
truncated_text_long_list = []
for i in text_long_df:
    truncated_text_long_list.append(i[0:100])



print('The 3 most common emotions from the sample of 1000 text_longs are: ', emotion_counter.most_common(3))

csvList = [list(item) for item in list(zip(truncated_text_long_list, max_emotion, rate_empath, emotion_df, initial_rating))]


data_dict = [{"text_long": truncated_text_long_list},
             {"Empath Emotion": max_emotion},
             {"Initial Emotion": emotion_df}]
header = ['text_long', 'empath_emotion','empath_rating', 'inital_emotion', 'initial_rating_of_empath_result']

with open('EmpathData.csv', 'w', newline='') as empath_file:
    writer = csv.writer(empath_file)
    writer.writerow(header)
    for row in csvList:
        writer.writerow(row)





