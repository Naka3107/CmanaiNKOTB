import detect_faces, httplib
def deletePerson(person,group,body):
    try:
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("DELETE", "/face/v1.0/persongroups/"+group+"/persons/"+person+"?%s" % None, body, detect_faces.headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
        print("Borrado")
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))