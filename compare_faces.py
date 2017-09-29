#coding: UTF-8

import detect_faces, httplib, urllib, json
#Metodos:
#verify
#request

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': detect_faces.subscription_key,
}

verifyparams = urllib.urlencode({
})

def verify(body):
    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/verify?%s" % verifyparams, body, headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        #print ("<<VERIFY>> Response:")
        #print (json.dumps(parsed, sort_keys=True, indent=2))

        return parsed
        # result = (json.dumps(parsed, sort_keys=True, indent=2))

        # print ("Se ha agregado el grupo")

        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.message, e.args))


def request(body):
    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/verify", body, detect_faces.headers)
    response = conn.getresponse()

    # response = requests.request(method, url, params=params, data=data,
    # json=json, headers=detect_faces.headers)

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




