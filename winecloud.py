# Start with loading all necessary libraries
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt

#import

df = pd.read_csv("winemag-data-130k-v2.csv", index_col=0)

# |country|description|designation|points|price|price|region1|region2|tastername|twitterhandle|title|variety|winery|
get_csv_hea1ds = df.head()

# gets head of selected csv columns
table_this = df[["country", "description", "points"]].head()

country = df.groupby("country")

# |country|count|mean|std|min|25%|50%|75%|max|count|mean|std|25|50|75|pricemax|
describe_this = country.describe().head()

# |country|points|price|
get_five = country.mean().sort_values(by="points", ascending=False).head()


def prints():
    # print(get_csv_heads)
    # print(table_this)
    # print(describe_this)
    print(get_five)


# prints()

def makeplot(fig_x, fig_y, rotation):
    plt.figure(figsize=(fig_x, fig_y))
    country.size().sort_values(ascending=False).plot.bar()
    plt.xticks(rotation=rotation)
    plt.xlabel("Country of Origin")
    plt.ylabel("Number of Wines")
    plt.show()


# makeplot(15, 10, 50)


def originplot(fig_x, fig_y, rotation):
    plt.figure(figsize=(fig_x, fig_y))
    country.max().sort_values(by="points",ascending=False)["points"].plot.bar()
    plt.xticks(rotation=rotation)
    plt.xlabel("Country of Origin")
    plt.ylabel("Highest point of wines")
    plt.show()


# originplot(15, 10, 50)


def make_word_cloud(description_array, interpolation, axis):
    text = df.description[description_array]

    wordcloud = WordCloud().generate(text)

    plt.imshow(wordcloud, interpolation=interpolation)

    plt.axis(axis)

    plt.show()


make_word_cloud(0, 'bilinear', "off")
print(df.description[0])
