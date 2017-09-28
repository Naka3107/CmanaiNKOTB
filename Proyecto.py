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
            print "Análisis de cara: "
            print infoPhoto

        # ********************Procesamiento de imagen****************************************

            #Se asigna a Id la variable faceID
            id = infoPhoto[0]['faceId']
            print "¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"
            print id
            #Se crea lista
            lista = (manage_person.listPersonsinGroup())
            print (len(lista))

            #Añade al grupo el rostro si este no se encuentra en él
            j = 0
            found = False
            for i in range(0, len(lista), 1):
                body = {}
                body['personId'] = lista[i]['personId']
                body['faceId'] = id
                body['personGroupId'] = GROUP
                js = json.dumps(body, sort_keys=True)

                print ">>> " + js
                print compare_faces.verify(js)
                print "~~~~~"

                found = (compare_faces.verify(js)['isIdentical'])
                if found:
                    break


            if not found:
                dataPerson = {}
                dataPerson['name'] = 'anon' + str(j)
                jsonpr = json.dumps(dataPerson)
                nP =  manage_person.createPerson(jsonpr)
                newPerson = {}
                newPerson['url'] = filename
                jsonNP = json.dumps(newPerson)
                dataPerson['persistedFaceIds'] = manage_person.addPersonFace(nP['personId'],GROUP,jsonNP)

                j = j + 1

    capture.release()

main(TOTAL_PHOTOS, INTERVAL)