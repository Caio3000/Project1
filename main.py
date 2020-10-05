import json
import requests
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import main_functions
from pprint import pprint
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# nltk.download("punkt")
# nltk.download("stopwords")

api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
api_key = api_key_dict["my_key"]

# Part A: Requesting user's name:

print("Enter your name:")
user_name = input()
print("Hello," + user_name.title())

# Part A: Requesting user to choose a category.

categories_set = ["arts", "automobiles", "business", "fashion", "food", "health", "home", "insider", "magazine",
                  "movies", "nyregion", "obituaries", "opinion", "politics", "realestate", "science", "sports",
                  "sundayreview", "technology", "theater", "t-magazine", "travel", "upshot", "us", "world"]

while True:
    print("Select one of the following categories:")
    pprint(categories_set)
    cat_selection = input()
    cat_selection = cat_selection.lower()

    if cat_selection not in categories_set:
        print("Your choice", cat_selection, "is not in the supported list")
        continue
    else:
        print("You have chosen", cat_selection)

        url = "https://api.nytimes.com/svc/topstories/v2/" + cat_selection + ".json?api-key=" + api_key
        response = requests.get(url).json()
        main_functions.save_to_file(response, "JSON_Files/response.json")
        my_articles = main_functions.read_from_file("JSON_Files/response.json")
        break

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
print("The top 10 most common words in this category were:")
pprint(fdist3.most_common(10))
wordcloud = WordCloud().generate(str1)

plt.figure(figsize=(12, 12))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

# Part B: Preferred set of articles.

options_set = ["shared", "emailed", "viewed"]

while True:
    print("Select the preferred set of articles:")
    pprint(options_set)
    opt_selection = input()
    opt_selection = opt_selection.lower()

    if opt_selection not in options_set:
        print("Your choice", opt_selection, "is not a supported option")
        continue
    else:
        break


time_set = ["1", "7", "30"]

while True:
    print("Select the period of time:")
    print(time_set)
    time_selection = input()

    if time_selection not in time_set:
        print("Select a valid time period.")
        continue

    if opt_selection == "shared":
        url = "https://api.nytimes.com/svc/mostpopular/v2/shared/" + time_selection + "/facebook.json?api-key=" + api_key
        break

    else:
        url = "https://api.nytimes.com/svc/mostpopular/v2/" + opt_selection + "/" + time_selection + ".json?api-key=" + api_key
        break

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

# fdist2 = FreqDist(words_no_punc)

# stopwords = stopwords.words("english")
clean_words = []

for w in words_no_punc:
    if w not in stopwords:
        clean_words.append(w)

fdist4 = FreqDist(clean_words)
print("The top 10 most common words in this category were:")
pprint(fdist4.most_common(10))
wordcloud = WordCloud().generate(str2)

plt.figure(figsize=(12, 12))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
