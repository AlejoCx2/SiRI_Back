import os
import nltk
import ssl
import csv
import json
import pickle

def downloadResources():
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

    from nltk.corpus import stopwords
    stop_words_es = set(stopwords.words('spanish'))
    stop_words_en = set(stopwords.words('english'))

    return stop_words_es.union(stop_words_en)

def vacancyToVector(id,update,justString):
    stop_words = downloadResources()
    vacantes = getVacantes()

    try:
        vacancy = vacantes[id]
        if vacancy['update'] == update:
            vacancy_S = vacancy['vector']
            print('---- Vacante Existente ----')
        else:
            print('---- Actualizando Vacante ----')
            vacancy_S = makeVacancy_S(justString,stop_words)
            vacantes[id] = {'update':update, 'vector':vacancy_S}
            with open('vacantes.pkl', 'wb') as file:
                pickle.dump(vacantes, file)
    except KeyError:
        vacancy_S = makeVacancy_S(justString,stop_words)
        vacantes[id] = {'update':update, 'vector':vacancy_S}

        with open('vacantes.pkl', 'wb') as file:
                pickle.dump(vacantes, file)

    #print(vacancy_S)
    return vacancy_S

def studentToVector(subKey,profile,experiences,certifications,skills):

    students = getStudents()
    try:
        student_S = students[subKey]
        print('---- Estudiante Existente ----')
        #print(student_S)
    except KeyError:
        student_S = makeVector(profile,experiences,certifications,skills)
        students[subKey] = student_S
        #print(student_S)



        with open('student.pkl', 'wb') as file:
            pickle.dump(students, file)

    return student_S


def getStudents():
    print('---- Obtenendo Estudiantes ----')
    with open('student.pkl', 'rb') as file:
        dict_recuperado = pickle.load(file)
    return dict_recuperado

def getVacantes():
    print('---- Obtenendo Vacantes ----')
    with open('vacantes.pkl', 'rb') as file:
        dict_recuperado = pickle.load(file)
    return dict_recuperado

def makeVacancy_S(justString,stop_words):
    print('---- Vectorizando Vacante ----')
    vacancy_V = [word.lower() for word in nltk.word_tokenize(justString) if word.isalpha()]
    vacancy_V = [word for word in vacancy_V if word not in stop_words]
    
    with open('vector.pkl', 'rb') as file:
        words = pickle.load(file)
        #with open('features.csv', 'r') as fr:
        #    reader = csv.reader(fr)
        #    for i, fila in enumerate(reader, start=1):
        #        if i == 1:
        #            words = set(fila)  # Guarda los valores de la fila en un conjunto
        #            break

    return [1 if word in vacancy_V else 0 for word in words]

def makeVector(profile,experiences,certifications,skills):
    stop_words = downloadResources()

    print('---- Unir Informacion ----')
    justString = profile['description']

    for e in experiences:
        justString += " " + e['description']
        for r in e['roles']:
            justString += " " + r
        
    for c in certifications:
        justString += " " + c['name']

    for s in skills:
        justString += " " + s['name']

    print('---- Vectorizar Estudiante ----')
    student_V = [word.lower() for word in nltk.word_tokenize(justString) if word.isalpha()]
    student_V = [word for word in student_V if word not in stop_words]
        
    with open('vector.pkl', 'rb') as file:
        words = pickle.load(file)
    #with open('features.csv', 'r') as fr:
    #    reader = csv.reader(fr)
    #    for i, fila in enumerate(reader, start=1):
    #        if i == 1:
    #            words = set(fila)  # Guarda los valores de la fila en un conjunto
    #            break

    return [1 if word in student_V else 0 for word in words]

def updateStudent(subKey,profile,experiences,certifications,skills):
    students = getStudents()
    try:
        old_student_S = students[subKey]
        print('---- Estudiante Encontrado ----')
        student_S = makeVector(profile,experiences,certifications,skills)
        students[subKey] = student_S
        print(old_student_S==student_S)

        with open('student.pkl', 'wb') as file:
            pickle.dump(students, file)

        return {'msg':"Actualizado",'vector':student_S}
    except KeyError:
        # No ha aplicado a alguna vacante aun
        return {'msg':"No Existe"}

def compareSkills(vSkl, sSkl):
    total = len(vSkl)
    cumplidas = 0
    vSkl = loweCase(vSkl)
    sSkl = loweCase(sSkl)
    for s in vSkl:
        if s in sSkl:
            print(s)
            cumplidas += 1
    
    return cumplidas / total

def loweCase(slist):
    lowerArr = []
    for s in slist:
        try:
            lowerArr.append(s.lower())
        except AttributeError:
            lowerArr.append(s['name'].lower())
    return lowerArr

def verifyExperience(reqExp,stdExpList):
    reqArr = reqExp.split(" ") #['cantidad' 'unidad']

    if reqArr[1] == "años" or reqArr[1] == "año":
        req = int(reqArr[0])*12
    else:
        req = int(reqArr[0])

    std = 0
    for stdExp in stdExpList:
        stdArr = stdExp['experience_time'].split(" ")
        if stdArr[1] == "years" or stdArr[1] == "year":
            std += int(stdArr[0])*12
        else:
            std += int(stdArr[0])
    #print(std)
    #print(req)
    return {'std':std,'req':req}
    