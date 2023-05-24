import os
import nltk
import ssl
import csv

def vacancyToVector(justString):
    try:
        _create_unverified_https_context = ssl._create_unverified_context
        print('---- Try ssl ----')
    except AttributeError:
        print('---- Except ssl ----')
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    print('---- Descargando recursos ----')
    nltk.download('punkt')
    nltk.download('stopwords')

    print('---- Let`s Go ----')

    from nltk.corpus import stopwords
    stop_words_es = set(stopwords.words('spanish'))
    stop_words_en = set(stopwords.words('english'))
    stop_words = stop_words_es.union(stop_words_en)

    print('---- Vectorizando Vacante ----')
    vacancy_V = [word.lower() for word in nltk.word_tokenize(justString) if word.isalpha()]
    vacancy_V = [word for word in vacancy_V if word not in stop_words]
    
    with open('features.csv', 'r') as fr:
        reader = csv.reader(fr)
        for i, fila in enumerate(reader, start=1):
            if i == 1:
                words = set(fila)  # Guarda los valores de la fila en un conjunto
                break

    vacancy_S = [1 if word in vacancy_V else 0 for word in words]
    
    return vacancy_S