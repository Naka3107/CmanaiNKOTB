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
                print "\nAnálisis de cara: "
                infoPhoto = detect_faces.readFace(filename)
                preventError(infoPhoto)
                print infoPhoto
            stuck = True


        #*************************Procesamiento de imagen***********************************

        #
        if len(infoPhoto) > 0:
            # Se asigna a Id la variable faceID
            id = infoPhoto[0]['faceId']
            print "\n<<Person ID asignado>>"
            print id

            #manage_person.addPersonFace(id, GROUP, filename)

            #Se crea lista
            while stuck:
                lista = (manage_person.listPersonsinGroup())
                preventError(lista)
            stuck = True

            print "\nPersonas registradas: "
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
                    #Elimina del grupo a la persona que relacionó con el
                    print "\n<<Se ha registrado salida del usario con ID:" + body['personId'] + ">>"
                    manage_person.deletePerson(body['personId'], GROUP)
                    print "**********************************************************************************"
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
                #print "*******Peristed face ID:*********"
                #print result
                print "\n<<Se ha resigistrado persona en el edificio>>\n\n\n"
                print "\n*******************************************************************************************"


    capture.release()

def clean():
    result = manage_person.deletePerson('8f65e0e7-29bb-45a9-8e87-d78492ded7d9', GROUP)
    preventError(result)

def print_list():
    manage_person.listPersonsinGroup()

def preventError(error):
    global stuck

    #print ">>>>>>>>>>>>>>>>>>>>> "
    #print error

    try:
        #print error['error']
        message = error['error']['message']

        if message == 'Rate limit is exceeded. Try again later.':
            print "Waiting for 1 minute... (DEMO version)"
            time.sleep(60)
            stuck = True
    except Exception as e:
        #print "Respuesta dentro del limite"
        stuck = False

main(TOTAL_PHOTOS, INTERVAL)
#clean()
#print_list()

