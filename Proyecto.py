#coding: UTF-8

#pip install mumpy
#pip install vc2
#pip install pillow

import cv2, os, inspect, time
# LOCAL
import detect_faces

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


# Record from live video
def main(limit, interval):

    limit -= 1

    # Changeable variable according to desired time
    INITIAL = int(time.time())

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

            filename = imgPATH + "image_" + str(delta / interval) + ".jpg"
            cv2.imwrite(filename, frame)

            infoPhoto = detect_faces.readFace(filename)

        print infoPhoto


    capture.release()

main(TOTAL_PHOTOS, INTERVAL)