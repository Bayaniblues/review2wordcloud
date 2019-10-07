import json
from collections import Counter
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import pandas as pd
import matplotlib.pyplot as plt

pos_store = []

positive_noun_array = []
positive_verb_array = []
positive_adjective_array = []

neutral_noun_array = []
neutral_verb_array = []
neutral_adjective_array = []

negative_noun_array = []
negative_verb_array = []
negative_adjective_array = []


def writejson():
    with open('analyzed2.json', encoding="utf-8") as file:
        analyzed_json = json.loads(file.read())
        sentiment_id = analyzed_json[0]["Sentiment"]
        parts_of_speech = analyzed_json[0]["POS"]

        for i in range(len(analyzed_json)):

            for x in range(len(analyzed_json[i]["POS"])):
                POS_word = analyzed_json[i]["POS"][x][0]
                POS_classify = analyzed_json[i]["POS"][x][1]

                sentiment = analyzed_json[i]["Sentiment"]

                classify_positive = sentiment == "positive"
                classify_neutral = sentiment == "neutral"
                classify_negative = sentiment == "negative"

                separate_nouns = POS_classify == 'NN' or POS_classify == 'NNP' or POS_classify == 'NNPS'
                separate_verbs = POS_classify == 'VB' or POS_classify == 'VBD' or POS_classify == 'VBG' or POS_classify == 'VBN' or POS_classify == 'VBP' or POS_classify == 'VBZ'
                separate_adj = POS_classify == 'JJ' or POS_classify == 'JJR' or POS_classify == 'JJS'

                def classify_parts_of_speech(noun_array, verb_array, adj_array):
                    if separate_nouns is True:
                        # print(POS_word)
                        # print(separate_nouns)
                        noun_array.append(POS_word)

                    elif separate_verbs is True:
                        verb_array.append(POS_word)

                    elif separate_adj is True:
                        adj_array.append(POS_word)

                    else:
                        pass

                if classify_positive is True:
                    classify_parts_of_speech(positive_noun_array, positive_verb_array, positive_adjective_array)

                if classify_neutral is True:
                    classify_parts_of_speech(neutral_noun_array, neutral_verb_array, neutral_adjective_array)

                if classify_negative is True:
                    classify_parts_of_speech(negative_noun_array, negative_verb_array, negative_adjective_array)


writejson()
# print(positive_noun_array, positive_verb_array, positive_adjective_array)

# print(positive_noun_array)


def word_count(list):
    counts = Counter(list)
    return counts


#print(word_count(positive_noun_array))


def make_word_cloud(description_array):
    unique_string=(" ").join(description_array)

    wordcloud = WordCloud(width=1000, height=1000).generate(unique_string)

    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


def generate_wordclouds():
    make_word_cloud(positive_verb_array)
    make_word_cloud(positive_adjective_array)
    make_word_cloud(positive_noun_array)

    make_word_cloud(neutral_verb_array)
    make_word_cloud(neutral_adjective_array)
    make_word_cloud(neutral_noun_array)

    make_word_cloud(negative_verb_array)
    make_word_cloud(negative_adjective_array)
    make_word_cloud(negative_noun_array)


generate_wordclouds()
