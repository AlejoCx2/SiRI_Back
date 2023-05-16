from rest_framework import status
from .models import Students
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import handleAuthToken
from .serializers import StudentsSerializers

import os
import nltk
import ssl
import csv


@api_view(['POST'])
@permission_classes([handleAuthToken])
def generarRanking(req):

    res = {'status': 0, 'result': {}, 'msg': ""}
    vacancy = req.data['vacancy']

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
    stop_words = set(stopwords.words('english'))

    print('---- Vectorizando Vacante ----')
    vacancy_V = [word.lower() for word in nltk.word_tokenize(vacancy) if word.isalpha()]
    vacancy_V = [word for word in vacancy_V if word not in stop_words]
    
    with open('features.csv', 'r') as fr:
        reader = csv.reader(fr)
        for i, fila in enumerate(reader, start=1):
            if i == 1:
                words = set(fila)  # Guarda los valores de la fila en un conjunto
                break

    vacancy_S = [1 if word in vacancy_V else 0 for word in words]

    res['status']=1
    res['result']=sum(vacancy_S)

    return Response(res)
