import requests
import random
import re
from bs4 import BeautifulSoup
from pymystem3 import Mystem

CORPUS_SIZE = 20
ENGLISH_LETTERS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower())
NUMBERS = set("1234567890")


def make_corpus(corpus_number):
    f = open("data/{}_corpus_links.txt".format(corpus_number), 'r')
    corpus = []
    for s in f.readlines():
        page = requests.get(s)
        soup = BeautifulSoup(page.content, 'html.parser')
        text = soup.text
        list_of_terms = list(filter(lambda x: x != '' and len(set(x) & ENGLISH_LETTERS) == 0 and len(set(x) & NUMBERS) == 0, re.split(''' |,|:|;|"|-|\n|<|>|\*|#|@|\(|\)|_ +''', text)))
        sentences = ' '.join(list_of_terms).split('.')
        corpus = corpus + sentences
    f.close()
    return corpus

first_corpus = make_corpus(1)
second_corpus = make_corpus(2)


def analyze_corpus(corpus, number):
    f = open("result_mystem/{}_ans.txt".format(number), "w")
    for _ in range(20):
        i = random.randint(0, CORPUS_SIZE - 1)
        m = Mystem()
        lemmas = m.lemmatize(corpus[i])
        res = "".join(lemmas).strip()
        ms = Mystem()
        analyze = ms.analyze(corpus[i])
        f.write("Предложение = {}\n, Результат = {}\n\n".format(corpus[i], res))
        for j, x in enumerate(analyze):
            if not 'analysis' in x or len(x['analysis']) == 0:
                continue
            if 'gr' not in x['analysis'][0]:
                continue
            f.write("анализ = {}\n".format(x['analysis'][0]['gr']))
        f.write("====================\n")
    f.close()

analyze_corpus(first_corpus, 1)
analyze_corpus(second_corpus, 2)

