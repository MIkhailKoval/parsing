import pymorphy2
import re
import requests
import random
from bs4 import BeautifulSoup
CORPUS_SIZE = 20
ENGLISH_LETTERS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower())
NUMBERS = set("1234567890")

MAPPING_POS = {
    "NOUN":	"существительное",	
    "ADJF":	"прилагательное (полное)",
    "ADJS":	"прилагательное (краткое)",
    "COMP":	"компаратив",
    "VERB":	"глагол (личная форма)",
    "INFN":	"глагол (инфинитив)",
    "PRTF":	"причастие (полное)",
    "PRTS":	"причастие (краткое)",
    "GRND":	"деепричастие",
    "NUMR":	"числительное",
    "ADVB":	"наречие",
    "NPRO":	"местоимение-существительное",
    "PRED":	"предикатив",
    "PREP":	"предлог",
    "CONJ":	"союз",
    "PRCL":	"частица",
    "INTJ":	"междометие",
    None  : "ошибка",
}

MAPPING_GENDER = {
    "masc":	"мужской",
    "femn":	"женский",
    "neut": "средний",
    None  : "ошибка",
}

MAPPING_NUMBER = {
    "sing": "ед.",
    "plur": "мн.",
    None  : "ошибка",
}

MAPPING_CASE = {
    "nomn":	"именительный",
    "gent":	"родительный",
    "datv":	"дательный",
    "accs":	"винительный",
    "ablt":	"творительный",
    "loct":	"предложный",
    "voct":	"звательный",
    "gen2":	"родительный",
    "acc2":	"винительный",
    "loc2": "предложный",
    None: "ошибка",
}

def make_corpus(corpus_number):
    f = open("data/{}_corpus_links.txt".format(corpus_number), 'r')
    corpus = []
    for s in f.readlines():
        page = requests.get(s)
        soup = BeautifulSoup(page.content, 'html.parser')
        text = soup.text
        list_of_terms = list(filter(lambda x: x != '' and len(set(x) & ENGLISH_LETTERS) == 0 and len(set(x) & NUMBERS) == 0, re.split(''' |\.|,|:|;|\?|"|-|\n|<|>|\*|!|#|@|\(|\)|_ +''', text)))
        corpus.append(list_of_terms)
    f.close()
    return corpus

first_corpus = make_corpus(1)
second_corpus = make_corpus(2)


def analyze_corpus(corpus, number):
    morph = pymorphy2.MorphAnalyzer()
    f = open("result/{}_ans.txt".format(number), "w")
    for _ in range(20):
        i = random.randint(0, CORPUS_SIZE - 1)
        j = random.randint(0, len(corpus[i]) - 1) 
        res = morph.parse(corpus[i][j])[0].tag
        f.write("Слово = {}\n часть речи = {}\n род = {}\n число = {}\n падеж = {}\n\n".format(corpus[i][j], MAPPING_POS[res.POS], MAPPING_GENDER[res.gender], MAPPING_NUMBER[res.number], MAPPING_CASE[res.case]))
        f.write("контекст = {}\n".format(corpus[i][max(0, j - 3) : min(j + 3, len(corpus[i]))]))
        f.write("====================\n")
    f.close()

analyze_corpus(first_corpus, 1)
analyze_corpus(second_corpus, 2)

