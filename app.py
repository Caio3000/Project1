import streamlit as st
import numpy as np
import pandas as pd
import json

import requests
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import main_functions
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.title("Project 1")
st.subheader("by Caio Silva")
st.header("Part A - Top Stories API")
st.write("I - Topic Selection")

user_name = st.text_input("Enter your name")
user_name = user_name.title()

categories = st.selectbox("Select one of the following categories:",
                          ("", "arts", "automobiles", "business", "fashion", "food", "health", "home", "insider",
                           "magazine", "movies", "nyregion", "obituaries", "opinion", "politics", "realestate",
                           "science", "sports",
                           "sundayreview", "technology", "theater", "t-magazine", "travel", "upshot", "us", "world")
                          )

if categories:
    st.write("Hello, ", user_name, "you have selected the", categories, "category.")

    api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
    api_key = api_key_dict["my_key"]
    url = "https://api.nytimes.com/svc/topstories/v2/" + categories + ".json?api-key=" + api_key
    response = requests.get(url).json()
    main_functions.save_to_file(response, "JSON_Files/response.json")
    my_articles = main_functions.read_from_file("JSON_Files/response.json")

    obj = {"x": 1, "y": 2}

    str1 = ""
    for i in my_articles["results"]:
        str1 = str1 + i["abstract"]

    sentences = sent_tokenize(str1)
    words = word_tokenize(str1)

    fdist = FreqDist(words)

    words_no_punc = []

    for w in words:
        if w.isalpha():
            words_no_punc.append(w.lower())

    fdist2 = FreqDist(words_no_punc)

    stopwords = stopwords.words("english")
    clean_words = []

    for w in words_no_punc:
        if w not in stopwords:
            clean_words.append(w)

    fdist3 = FreqDist(clean_words)

    ####################################################################

    st.write("II - Frequency Distribution")

    dataset = {'List': fdist3.most_common(10)}

    pos_0 = [x[0] for x in dataset['List']]
    pos_1 = [x[1] for x in dataset['List']]

    y_position = np.arange(len(pos_0))

    plt.figure(figsize=(12, 8))
    plt.xticks(y_position, pos_0)
    plt.plot(y_position, pos_1)
    plt.xlabel("Words")
    plt.ylabel("Count")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(plt.show())

    #####################################################################

    st.write("III - Wordcloud")

    if st.checkbox("Click here to generate wordcloud"):
        st.write("The top 10 most common words in this category were:")
        # pprint(fdist3.most_common(10))
        wordcloud = WordCloud().generate(str1)

        plt.figure(figsize=(12, 12))
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()
        st.pyplot()

    ######################################################################

st.header("Part B - Most Popular Articles")

options_set = st.selectbox("Select the preferred set of articles:",
                           ("", "shared", "emailed", "viewed")
                           )

time_set = st.selectbox("Select the period of time:",
                        ("", "1", "7", "30")
                        )

api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
api_key = api_key_dict["my_key"]

if options_set == "shared":
    url = "https://api.nytimes.com/svc/mostpopular/v2/shared/" + time_set + "/facebook.json?api-key=" + api_key

else:
    url = "https://api.nytimes.com/svc/mostpopular/v2/" + options_set + "/" + time_set + ".json?api-key=" + api_key

if time_set:
    response = requests.get(url).json()
    main_functions.save_to_file(response, "JSON_Files/response2.json")
    my_articles1 = main_functions.read_from_file("JSON_Files/response2.json")

    str2 = ""
    for i in my_articles1["results"]:
        str2 = str2 + i["abstract"]

    words = word_tokenize(str2)

    fdist1 = FreqDist(words)

    words_no_punc = []

    for w in words:
        if w.isalpha():
            words_no_punc.append(w.lower())

    clean_words = []

    for w in words_no_punc:
        if w not in stopwords:
            clean_words.append(w)

    fdist4 = FreqDist(clean_words)
    wordcloud = WordCloud().generate(str2)

    if st.checkbox("Click here to generate the wordcloud"):
        st.write("The top 10 most common words in this category were:")
        wordcloud = WordCloud().generate(str2)

        plt.figure(figsize=(12, 12))
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()
        st.pyplot()
