import os
import json
from collections import Counter
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


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

nested_arrays = [
                 'positive_verb_array',
                 'positive_adjective_array',
                 'positive_noun_array',

                 'neutral_verb_array',
                 'neutral_adjective_array',
                 'neutral_noun_array',

                 'negative_verb_array',
                 'negative_adjective_array',
                 'negative_noun_array',
]

get_file = 'analyzed2.json'

folder_name = get_file.replace(".json", "")

print(folder_name)


def writejson():
    with open(get_file, encoding="utf-8") as file:
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



# print(positive_noun_array, positive_verb_array, positive_adjective_array)

# print(positive_noun_array)


def word_count(list):
    counts = Counter(list)
    return counts


def build_pos_world_cloud():
    fig = plt.figure(figsize=(10, 10))
    columns = 3
    rows = 3

    # xs = np.linspace(0, 2*np.pi, 60)
    # ys = np.abs(np.sin(xs))

    ax = []
    plt.title("Parts of Speech Sentiment of a Popular Alexa Skill", pad=30)
    x = [1.5, 2, 2.5]
    y = [1, 2, 3]
    xlabels = ['Verbs', "Adjectives", "Nouns"]
    ylabels = ['Negative', 'Neutral', 'Positive']
    plt.plot(x, y, 'ro')
    plt.xticks(x, xlabels)
    plt.yticks(y, ylabels)

    for i in range(columns*rows):
        x = np.arange(1)
        print(i)
        img = mpimg.imread(f"{folder_name}/" + nested_arrays[i] + ".png")
        ax.append(fig.add_subplot(rows, columns, i+1))
        ax[i].get_xaxis().set_visible(False)
        ax[i].get_yaxis().set_visible(False)
        # ax[-1].set_title(nested_arrays[i])
        plt.imshow(img, aspect='auto')

    plt.show()


def generate_wordclouds():
    if os.path.isdir(f"{folder_name}"):
        os.remove(f"{folder_name}")
        print(f"{folder_name} folder removed")
        os.mkdir(f'{folder_name}')
        os.chmod(f'{folder_name}', 0o777)
        print(f"{folder_name} folder added")
    else:
        os.mkdir(f'{folder_name}')
        os.chmod(f'{folder_name}', 0o777)
        print(f"{folder_name} folder added")

    def make_word_cloud(description_array, description_label):
        unique_string = (" ").join(description_array)

        wordcloud = WordCloud(width=1500, height=1500, min_font_size=20, background_color="white").generate(
            unique_string)

        plt.figure(figsize=(15, 15))
        plt.imshow(wordcloud)
        plt.axis("off")
        # plt.show()

        wordcloud.to_file(f'{folder_name}/{description_label}.png')
        print(f'{description_label}.png added')

    make_word_cloud(positive_verb_array, 'positive_verb_array')
    make_word_cloud(positive_adjective_array, 'positive_adjective_array')
    make_word_cloud(positive_noun_array, 'positive_noun_array')

    make_word_cloud(neutral_verb_array, 'neutral_verb_array')
    make_word_cloud(neutral_adjective_array, 'neutral_adjective_array')
    make_word_cloud(neutral_noun_array, 'neutral_noun_array')

    make_word_cloud(negative_verb_array, 'negative_verb_array')
    make_word_cloud(negative_adjective_array, 'negative_adjective_array')
    make_word_cloud(negative_noun_array, 'negative_noun_array')

    build_pos_world_cloud()


def legend():
    fig = plt.figure()
    ax1 = fig.add_axes(["pos", "neu", "neg"])
    fig.legend(())


writejson()
generate_wordclouds()