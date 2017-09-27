import detect_faces, httplib, urllib, json
#Metodos:
#createPerson
#getPerson
#listPersonsinGroup
#addPersonFace

params = urllib.urlencode({
    'personGroupId' : 'semanai'
})

listparams = urllib.urlencode({
    #'personGroupId' : 'cmanai',
    'start' : '',
    'top': '1000'
})

getpersonparams = urllib.urlencode({
    'personGroupId' : 'cmanai',
    #'personId': '30d01b70-e147-4a3a-b77b-37a15c44ece7'
})

def createPerson(body):
    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/persongroups/{personGroupId}/persons?%s" % params, body, detect_faces.headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        print ("Response:")
        print (json.dumps(parsed, sort_keys=True, indent=2))

        # result = (json.dumps(parsed, sort_keys=True, indent=2))

        print ("Se ha agregado el grupo")

        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.message, e.args))


def getPerson():
    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("GET", "/face/v1.0/persongroups/" + "cmanai" + "/persons/{personId}?%s" % getpersonparams, None,
                     detect_faces.headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        print ("Response:")
        print (json.dumps(parsed, sort_keys=True, indent=2))

        # result = (json.dumps(parsed, sort_keys=True, indent=2))

        # print ("Se ha agregado el grupo")

        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.message, e.args))


def listPersonsinGroup():
    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("GET", "/face/v1.0/persongroups/" + 'cmanai' + "/persons?%s" % listparams, None, detect_faces.headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        print ("Response:")
        print (json.dumps(parsed, sort_keys=True, indent=2))

        return parsed

        # result = (json.dumps(parsed, sort_keys=True, indent=2))

        # print ("Se ha agregado el grupo")

        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.message, e.args))


def addPersonFace(person, group, body):
    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/persongroups/" + group + "/persons/" + person + "/persistedFaces?%s" % None,
                     body, detect_faces.headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        print ("Response:")
        print (json.dumps(parsed, sort_keys=True, indent=2))

        # result = (json.dumps(parsed, sort_keys=True, indent=2))

        # print ("Se ha agregado el grupo")

        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.message, e.args))