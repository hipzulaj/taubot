import re
import string
import sklearn
import pickle
import csv
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from similarity.levenshtein import Levenshtein
from csv import DictReader

# Load Model
with open("E:\Document\KULIAH\Semester 7\PBA\model.pkl", 'rb') as file:
    model = pickle.load(file)

def preprocessing(dataset):
    stemmer = StemmerFactory().create_stemmer()
    stopwords = StopWordRemoverFactory().create_stop_word_remover()
    for row in dataset:
        row['message'] = row.get('message').casefold()
        row['message'] = re.sub(r"[0-9]", "", row.get('message'))
        row['message'] = re.sub('['+string.punctuation+']', "", row.get('message'))
        row['message_stopwords'] = stopwords.remove(row['message'])
        row['message_stemmed'] = stemmer.stem(row['message_stopwords'])
        row['message_tokenized'] = word_tokenize(row['message_stemmed'])
dataset = []

with open(r'E:\Document\KULIAH\Semester 7\PBA\dataset.csv', 'r') as file:
    reader = csv.DictReader(file, delimiter=';', quoting=csv.QUOTE_NONE)
    for row in reader:
        if row['message'] == "START" or row['message'] == "END":
            pass
        elif row['Tagging'] == '' or row['Tagging'] == '"':
            pass
        else:
            dataset.append(
                    {
                        'message': row['message'],
                        'category' : row['Tagging'],
                        'respond' : row['response']
                    }
                )

preprocessing(dataset)

def respond(strg):
    levenshtein = Levenshtein()
    stemmer = StemmerFactory().create_stemmer()
    stopwords = StopWordRemoverFactory().create_stop_word_remover()

    kategori = model.predict([strg])

    txt = stopwords.remove(strg)
    txt = stemmer.stem(txt)

    best = 1000
    res = []

    for words in dataset:
        if(words['category'] == kategori):
            distance = levenshtein.distance(txt, words['message_stemmed'])

            if (distance < best):
                best = distance
                res = words
    return res['respond']
