import os
import json
import requests
import csv
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

pos_count = 0
neutral_count = 0
neg_count = 0

master_list = []

pos_store = []
neutral_store = []
neg_store = []

# store for sentiment json


def write_json():
    if os.path.isfile("analyzed2.json"):
        os.remove("analyzed2.json")
    with open("analyzed2.json", "w", encoding='utf8', errors='ignore') as write_file:
        json.dump(master_list, write_file)


def printstatus(outputData, scores, description_key, i, x):
    print(outputData[i]["review_description"][x])
    print(scores)
    print(scores[description_key])


def add_counter():
    global pos_count
    global neutral_count
    global neg_count
    statushappy = "😄 positive", + pos_count
    statusneutral = "😐 neutral", + neutral_count
    statusfrown = "😠 negative", + neg_count
    print("Calculating Sentiment: ", statushappy, statusneutral, statusfrown, end="\r")


def nestedarray():
    with open('sirius.json', encoding="utf-8") as file:
        outputData = json.loads(file.read())

        for i in range(len(outputData)):

            for x in range(len(outputData[i]['review_description'])):
                phrase = outputData[i]["review_description"][x]
                # vader
                analyzer = SentimentIntensityAnalyzer()
                scores = analyzer.polarity_scores(outputData[i]["review_description"][x])
                description_key = 'compound'
                # printstatus(outputData, scores, description_key, i, x)

                # textblob
                blob = TextBlob(phrase)

                def add_pos_count():
                    # print('positive')
                    global pos_count
                    pos_count = pos_count + 1
                    master_list.append({
                        "Sentence": outputData[i]["review_description"][x],
                        "Score": scores,
                        "Sentiment": "positive",
                        "POS": blob.tags
                    }
                    )

                def add_neutral_count():
                    # print('neutral')
                    global neutral_count
                    neutral_count = neutral_count + 1
                    master_list.append({
                        "Sentence": outputData[i]["review_description"][x],
                        "Score": scores,
                        "Sentiment": "neutral",
                        "POS": blob.tags
                    })

                def add_neg_count():
                    # print('negative')
                    global neg_count
                    neg_count = neg_count + 1
                    master_list.append({
                        "Sentence": outputData[i]["review_description"][x],
                        "Score": scores,
                        "Sentiment": "negative",
                        "POS": blob.tags
                    })

                def description_value_gates():

                    if description_key in scores:
                        if scores[description_key] >= 0.05:
                            add_pos_count()

                        if scores[description_key] >= -0.05 < scores[description_key] < 0.05:
                            add_neutral_count()

                        if scores[description_key] <= -0.05:
                            add_neg_count()

                description_value_gates()
                add_counter()


nestedarray()
# print(master_list)
add_counter()
write_json()


def countobjects():
    with open('sirius.json', encoding="utf-8") as file:
        outputData = json.loads(file.read())
        print(len(outputData))


