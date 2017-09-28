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
# -----------------------------------------

PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PATH = PATH.replace('\\', '/')
imgPATH = PATH + "/Images/"
vidPATH = PATH + "/Videos/"

capture = cv2.VideoCapture(0)


# Procesa Caras a partir de video
def main(limit, interval):

    limit -= 1
    group = 'cmanai'

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

            # Otorga un nombre de archivo
            filename = imgPATH + "image_" + str(delta / interval) + ".jpg"
            cv2.imwrite(filename, frame)
            print "Fotografía guardada en: " + filename

            # Otorga un face Id y respectivas caracteristicas del rostro
            infoPhoto = detect_faces.readFace(filename)
            print "Análisis de cara: "
            print infoPhoto

        # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

            #Se asigna a Id la variable faceID
            id = infoPhoto[0]['faceId']

            #Se crea lista
            lista = (manage_person.listPersonsinGroup())
            print (len(lista))

            #Añade al grupo el rostro si este no se encuentra en él
            j = 0
            finded = False
            for i in range(0, len(lista), 1):
                body = {}
                body['personId'] = lista[i]['personId']
                body['faceId'] = id
                body['personGroupId'] = group
                js = json.dumps(body, sort_keys=True)

                print ">>> " + js
                print compare_faces.verify(js)
                print "~~~~~"

                finded = (compare_faces.verify(js)['isIdentical'])
                if finded:
                    break


            if not finded:
                dataPerson = {}
                dataPerson['name'] = 'anon' + str(j)
                jsonpr = json.dumps(dataPerson)
                print manage_person.createPerson(jsonpr)
                j = j + 1

    capture.release()

main(TOTAL_PHOTOS, INTERVAL)