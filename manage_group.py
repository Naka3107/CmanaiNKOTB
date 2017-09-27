import detect_faces, httplib, urllib, json
#Metodos:
#createPersonGroup
#getGroup
#deleteGroup
#listGroup

params = urllib.urlencode({
    'personGroupId' : 'semanai'
})

listparams = urllib.urlencode({
    #'personGroupId' : 'cmanai',
    'start' : '',
    'top': '1000'
})

def creatPersonGroup(body):
    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("PUT", "/face/v1.0/persongroups/{personGroupId}?%s" % params, body, detect_faces.headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        # parsed = json.loads(data)
        # print ("Response:")
        # print (json.dumps(parsed, sort_keys=True, indent=2))

        # result = (json.dumps(parsed, sort_keys=True, indent=2))

        print ("Se ha agregado al grupo")

        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.message, e.args))

        # print parsed


def getGroup():
    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("GET", "/face/v1.0/persongroups/{personGroupId}?%s" % params, None, detect_faces.headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        print ("Response:")
        print (json.dumps(parsed, sort_keys=True, indent=2))

        # result = (json.dumps(parsed, sort_keys=True, indent=2))

        # print ("Se ha creado el grupo")

        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.message, e.args))


def deleteGroup():
    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("DELETE", "/face/v1.0/persongroups/{personGroupId}?%s" % params, None, detect_faces.headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        # print ("Response:")
        # print (json.dumps(parsed, sort_keys=True, indent=2))

        # result = (json.dumps(parsed, sort_keys=True, indent=2))

        print ("Se ha eliminado el grupo")

        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.message, e.args))


def listGroup():
    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("GET", "/face/v1.0/persongroups?%s" % listparams, None, detect_faces.headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        print ("Response:")
        print (json.dumps(parsed, sort_keys=True, indent=2))

        # result = (json.dumps(parsed, sort_keys=True, indent=2))

        print ("Se ha eliminado el grupo")

        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.message, e.args))