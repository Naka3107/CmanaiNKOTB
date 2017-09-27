#coding: UTF-8
import detect_facesPollo, os, inspect, webbrowser, cognitive_face, time, httplib, urllib, json, certifi, base64
from PIL import Image
import requests

params = urllib.urlencode({
    'personGroupId' : 'cmanai'
})

listparams = urllib.urlencode({
    #'personGroupId' : 'cmanai',
    'start' : '',
    'top': '1000'
})

getpersonparams = urllib.urlencode({
    'personGroupId' : 'cmanai',
    'personId': '30d01b70-e147-4a3a-b77b-37a15c44ece7'

})

verifyparams = urllib.urlencode({
})


def main():
    isURL = True

    # data ={}
    # data['name'] = 'semanaigroup'
    # json_data = json.dumps(data)


    #createPerson(jsonpr)
    #creatPersonGroup(json_data)
    #getGroup()
    #listGroup()
    #deleteGroup()
    #getPerson()

    # d = {}
    # d['url'] = 'https://blogdesuperheroes.es/wp-content/plugins/BdSGallery/BdSGaleria/2269.jpg'
    # j = json.dumps(d)
    # print j
    # print "RRRRRRRRRRRRRRRRRR"

    #person = '30d01b70-e147-4a3a-b77b-37a15c44ece7'
    #person2 = 'f6f5d8bf-33d6-429a-99ab-361af6ce5dc3'
    group = 'cmanai'

    #addPersonFace(person2, group,j)

    if isURL:
        # Change URL according to uses
        foto1 = "https://pbs.twimg.com/profile_images/902026418355290112/ZaPrOTYn_400x400.jpg"
        foto2 = "https://vignette.wikia.nocookie.net/batman/images/5/56/BruceBale.jpg"

        webbrowser.open(foto1)
        webbrowser.open(foto2)

        jsonFoto1 = "{'url':'" + foto1 + "'}"
        jsonFoto2 = "{'url':'" + foto2 + "'}"
        print "HHHHHHHHHHHHHHHHHHHH"
        print jsonFoto2

    #infoPhoto1 = detect_faces.readFace(jsonFoto1, isURL)
    infoPhoto = detect_facesPollo.readFace(jsonFoto2, isURL)

    id2 = infoPhoto[0]['faceId']

    lista = (listPersonsinGroup())

    print (len(lista))

    j=0
    for i in range(0,len(lista),1):
        body = {}
        body['personId'] = lista[i]['personId']
        body['faceId'] = id2
        body['personGroupId'] = group
        js = json.dumps(body, sort_keys=True)
        if (verify(js)['isIdentical']==False):
            dataPerson = {}
            dataPerson['name'] = 'anon'+j
            jsonpr = json.dumps(dataPerson)
            print createPerson (jsonpr)
            j=j+1


        #print (flag['isIdentical'])

        #if(verify(js)==False):
         #   dataPerson = {}
          #  dataPerson['name'] = 'Santiago Nakakawa'
           # jsonpr = json.dumps(dataPerson)
            #print (jsonpr)
            #createPerson(jsonpr)


    #print id2

def verify(body):
    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/verify?%s" % verifyparams, body, detect_facesPollo.headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        print ("Response:")
        print (json.dumps(parsed, sort_keys=True, indent=2))

        return parsed
        # result = (json.dumps(parsed, sort_keys=True, indent=2))

        #print ("Se ha agregado el grupo")

        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.message, e.args))

def request(body):

    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/verify", body, detect_facesPollo.headers)
    response = conn.getresponse()


    #response = requests.request(method, url, params=params, data=data,
                                #json=json, headers=detect_faces.headers)
 
    result = None
    if response.status_code not in (200, 202):
        print('status_code: {}'.format(response.status_code))
        print('response: {}'.format(response.text))
        error_msg = response.json()['error']

    if response.text:
        result = response.json()
    else:
        result = {}
 
    print (result)



def creatPersonGroup(body):
    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("PUT", "/face/v1.0/persongroups/{personGroupId}?%s" % params, body, detect_facesPollo.headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        #parsed = json.loads(data)
        #print ("Response:")
        #print (json.dumps(parsed, sort_keys=True, indent=2))

        # result = (json.dumps(parsed, sort_keys=True, indent=2))

        print ("Se ha agregado al grupo")

        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.message, e.args))

    #print parsed

def getGroup():

    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("GET", "/face/v1.0/persongroups/{personGroupId}?%s" % params, None, detect_facesPollo.headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        print ("Response:")
        print (json.dumps(parsed, sort_keys=True, indent=2))

        # result = (json.dumps(parsed, sort_keys=True, indent=2))

        #print ("Se ha creado el grupo")

        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.message, e.args))

def deleteGroup():

    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("DELETE", "/face/v1.0/persongroups/{personGroupId}?%s" % params, None, detect_facesPollo.headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        #print ("Response:")
        #print (json.dumps(parsed, sort_keys=True, indent=2))

        # result = (json.dumps(parsed, sort_keys=True, indent=2))

        print ("Se ha eliminado el grupo")

        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.message, e.args))

def listGroup():

    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("GET", "/face/v1.0/persongroups?%s" % listparams, None, detect_facesPollo.headers)
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


def createPerson(body):

    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/persongroups/{personGroupId}/persons?%s" % params, body, detect_facesPollo.headers)
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
        conn.request("GET", "/face/v1.0/persongroups/"+"cmanai"+"/persons/{personId}?%s" % getpersonparams, None, detect_facesPollo.headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        print ("Response:")
        print (json.dumps(parsed, sort_keys=True, indent=2))

        # result = (json.dumps(parsed, sort_keys=True, indent=2))

        #print ("Se ha agregado el grupo")

        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.message, e.args))

def listPersonsinGroup():

    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("GET", "/face/v1.0/persongroups/"+'cmanai'+"/persons?%s" % listparams, None, detect_facesPollo.headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        print ("Response:")
        print (json.dumps(parsed, sort_keys=True, indent=2))

        return parsed

        # result = (json.dumps(parsed, sort_keys=True, indent=2))

        #print ("Se ha agregado el grupo")

        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.message, e.args))

def addPersonFace(person, group, body):

    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/persongroups/"+group+"/persons/"+person+"/persistedFaces?%s" % None, body, detect_facesPollo.headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        print ("Response:")
        print (json.dumps(parsed, sort_keys=True, indent=2))

        # result = (json.dumps(parsed, sort_keys=True, indent=2))

        #print ("Se ha agregado el grupo")

        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.message, e.args))


main()
