#coding: UTF-8

#pip install mumpy
#pip install vc2
#pip install pillow

import cv2, os, inspect, time, json
# LOCAL
import compare_faces, detect_faces, manage_person

# -----------------------------------------
TOTAL_PHOTOS = 5                            # Fotos en memoria
FperM = 20                                  # Fotos por minuto
INTERVAL = 60 / FperM                       # Intervalo entre fotos
GROUP = 'cmanai'
# -----------------------------------------

PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PATH = PATH.replace('\\', '/')
imgPATH = PATH + "/Images/"
vidPATH = PATH + "/Videos/"

capture = cv2.VideoCapture(0)


# Procesa Caras a partir de video
def main(limit, interval):

    limit -= 1

    # Changeable variable according to desired time
    INITIAL = int(time.time())

    # Ciclo donde se mantiene el video activo
    while capture.isOpened():

        infoPhoto = ""


        # Current frame number
        delta = int(time.time()) - INITIAL

        if delta >= limit * interval:
            INITIAL = int(time.time())

        ret, frame = capture.read()

        if not ret:
            break

        if (delta % interval == 0):

        # ***************************Analisis de imagen**************************************

            # Otorga un nombre de archivo
            filename = imgPATH + "image_" + str(delta / interval) + ".jpg"
            cv2.imwrite(filename, frame)
            print "Fotografía guardada en: " + filename

            # Otorga un face Id y respectivas caracteristicas del rostro
            infoPhoto = detect_faces.readFace(filename)
            preventError(infoPhoto)
            print "Análisis de cara: "
            print infoPhoto

        # ********************Procesamiento de imagen****************************************

            #Se asigna a Id la variable faceID

        if len(infoPhoto) > 0:
            id = infoPhoto[0]['faceId']
            print "¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"
            print id
            #manage_person.addPersonFace(id, GROUP, filename)
            #Se crea lista
            lista = (manage_person.listPersonsinGroup())
            preventError(lista)
            print len(lista)
            #Añade al grupo el rostro si este no se encuentra en él
            found = False
            for i in range(0, len(lista), 1):
                body = {}
                body['personId'] = lista[i]['personId']
                body['faceId'] = id
                body['personGroupId'] = GROUP
                js = json.dumps(body, sort_keys=True)

                found = (compare_faces.verify(js)['isIdentical'])
                preventError(found)
                if found:
                    #Elimina del grupo a la persona que relacionó con el rostro
                    manage_person.deletePerson(body['personId'],GROUP)
                    break

            personidpo = ''
            if not found:
                dataPerson = {}
                dataPerson['name'] = "Debbie<3"
                jsonpr = json.dumps(dataPerson)
                personidpo = manage_person.createPerson(jsonpr)
                preventError(personidpo)
                print (personidpo['personId'])
                image = {}
                image['url'] = filename
                # debbie = json.dumps(image)
                result = manage_person.addPersonFace(personidpo['personId'], 'cmanai', filename)
                print result
                preventError(result)


    capture.release()

def clean():
    result = manage_person.deletePerson('c3c4091d-1d64-41e6-93ef-0216846f638f', GROUP)
    preventError(result)

def print_list():
    manage_person.listPersonsinGroup()

def preventError(error):

    try:
        message = error['error']['message']

        if message == 'Rate limit is exceeded. Try again later.':
            time.sleep(30)
    except Exception as e:
        print "Respuesta sin error"

def test():

    print "ANTES"
    print manage_person.listPersonsinGroup()

    dataPerson = {}
    dataPerson['name'] = "TEST"
    jsonpr = json.dumps(dataPerson)
    personidpo = manage_person.createPerson(jsonpr)
    preventError(personidpo)

    result = manage_person.addPersonFace(personidpo['personId'], 'cmanai', imgPATH + "c2.jpg")
    print "###########"
    print result
    preventError(result)

    print "DESPUES"
    print manage_person.listPersonsinGroup()

    print personidpo['personId']
    # result = manage_person.deletePerson(personidpo['personId'], GROUP)
    # preventError(result)

#main(TOTAL_PHOTOS, INTERVAL)
#clean()
print_list()
#test()

