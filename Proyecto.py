#coding: UTF-8

#pip install mumpy
#pip install vc2
#pip install pillow

import cv2, os, inspect, time, json, io
from PIL import Image
# LOCAL
import compare_faces, detect_faces, manage_person, blob_storage

# -----------------------------------------
TOTAL_PHOTOS = 5                            # Fotos en memoria
FperM = 10                                  # Fotos por minuto
INTERVAL = 60 / FperM                       # Intervalo entre fotos
GROUP = 'cmanai'
# -----------------------------------------

stuck = True

PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PATH = PATH.replace('\\', '/')
imgPATH = PATH + "/Images/"
vidPATH = PATH + "/Videos/"

capture = cv2.VideoCapture(0)


# Procesa Caras a partir de video
def main(limit, interval):
    global stuck

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
            picName = "image_" + str(delta / interval) + ".jpg"
            filename = imgPATH + picName
            cv2.imwrite(filename, frame)
            print "Fotografía guardada en: " + filename

            # Sube la foto a AZURE
            # ASEGURARSE QUE EL NOMBRE INCLUYE .jpg
            blob_storage.uploadImage(picName, picName)

            # Otorga un face Id y respectivas caracteristicas del rostro
            while stuck:
                infoPhoto = detect_faces.readFace(filename)
                preventError(infoPhoto)
            stuck = True

            print "Análisis de cara: "
            print infoPhoto

        # *************************Procesamiento de imagen***********************************

            #Se asigna a Id la variable faceID

        if len(infoPhoto) > 0:
            id = infoPhoto[0]['faceId']
            print "¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"
            print id
            #manage_person.addPersonFace(id, GROUP, filename)

            #Se crea lista
            while stuck:
                lista = (manage_person.listPersonsinGroup())
                preventError(lista)
            stuck = True

            print len(lista)
            #Añade al grupo el rostro si este no se encuentra en él
            found = False
            for i in range(0, len(lista), 1):
                body = {}
                body['personId'] = lista[i]['personId']
                body['faceId'] = id
                body['personGroupId'] = GROUP
                js = json.dumps(body, sort_keys=True)

                while stuck:
                    found = (compare_faces.verify(js)['isIdentical'])
                    preventError(found)
                stuck = True

                if found:
                    #Elimina del grupo a la persona que relacionó con el rostro
                    manage_person.deletePerson(body['personId'], GROUP)
                    break

            if not found:
                dataPerson = {}
                dataPerson['name'] = "anonymus"
                jsonpr = json.dumps(dataPerson)

                while stuck:
                    personidpo = manage_person.createPerson(jsonpr)
                    preventError(personidpo)
                stuck = True

                print (personidpo['personId'])

                image = {}
                image['url'] = blob_storage.URL + picName
                img = json.dumps(image)

                # img = Image.open(filename, mode='r')
                #
                # imgByteArr = io.BytesIO()
                # img.save(imgByteArr, format='PNG')
                # imgByteArr = imgByteArr.getvalue()

                # f = open(filename, "rb")
                # body = f.read()

                # f.close()

                while stuck:
                    result = manage_person.addPersonFace(personidpo['personId'], 'cmanai', img)
                    preventError(result)
                stuck = True

                print result


    capture.release()

def clean():
    result = manage_person.deletePerson('6666e429-3577-430c-aecb-4e123b854864', GROUP)
    preventError(result)

def print_list():
    manage_person.listPersonsinGroup()

def preventError(error):
    global stuck

    print ">>>>>>>>>>>>>>>>>>>>> "
    print error

    try:
        print error['error']
        message = error['error']['message']

        if message == 'Rate limit is exceeded. Try again later.':
            print "Waiting for 1 minute... (DEMO version)"
            time.sleep(60)
            stuck = True
    except Exception as e:
        print "Respuesta dentro del limite"
        stuck = False

main(TOTAL_PHOTOS, INTERVAL)
# clean()
# print_list()

