'''Exercise 1: Do a Get request to the url and return its content.
'''
def ex1(url : str)-> str:
    import requests
    response = requests.get(url)
    return response.text

'''Exercise 2: Do a Get request to the url and return its content.
Content should be a json object.
'''
def ex2(url : str)-> str:
    import requests
    headers = {"content-type": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()

'''Exercise 3: Do a Post request to the url with data.
Response should be a either:
{"status":"ok","message":"<something here>"} or
{"status":"error","message":"<error message here>"
Function should return based on this a tuple (True/False, message).
'''
def ex3(url : str, data:dict)-> str:
    import requests
    headers = {"content-type": "application/json"}
    r = requests.post(url, headers=headers, json=data)
    data = r.json()
    return (data['status'] == 'ok', data['message'])