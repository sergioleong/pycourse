import requests
import json

def main(argv) :
    server_url = 'http://localhost:5000/'
    data = readAll(server_url)
    print(data)
    
    insert(server_url, name="John", age=32)
    insert(server_url, name="Paul", age=80)
    insert(server_url, name="George", age=70)
    last_id = insert(server_url, name="Ringo", age=56)

    data = get(server_url, last_id)
    print(data)
    
    data = update(server_url, last_id, "MJ", age=60)
    print(data)

    data = get(server_url, last_id)
    print(data)

    delete(server_url, last_id)
    data = get(server_url, last_id)
    print(data)

def readAll(server_url):
    print("Read all objects")
    headers = {"content-type": "application/json"}
    r = requests.get(server_url, headers=headers)
    if r.status_code == 200:
        return r.json()['data']
    else:
        print(f'Error: {r.status_code}')

def get(server_url, id):
    print(f"Read object {id}")
    headers = {"content-type": "application/json"}
    r = requests.get(f'{server_url}/{id}', headers=headers)
    if r.status_code == 200:
        return r.json()['data']
    else:
        print(f'Error: {r.status_code}')

def delete(server_url, id):
    print(f"Delete object {id}")
    headers = {"content-type": "application/json"}
    r = requests.delete(f'{server_url}/{id}', headers=headers)
    if r.status_code == 202:
        print(r.json())
        return r.json()['text']
    else:
        print(f'Error: {r.status_code}')

def insert(server_url, name, age):
    print("Insert Object")
    headers = {"content-type": "application/json"}
    new_object = {
        "name": name,
        "age": age
    }
    r = requests.put(f'{server_url}/add', headers=headers, json=new_object)
    if r.status_code == 201:
        data = r.json()['data']
        print(data)
        return data['id']
    else:
        print(f'Error: {r.status_code}')
        return None
        
def update(server_url, id, name, age):
    print(f"Update Object {id}")
    headers = {"content-type": "application/json"}
    new_object = {
        "name": name,
        "age": age
    }
    r = requests.post(f'{server_url}/{id}', headers=headers, json=new_object)
    if r.status_code == 201:
        data = r.json()['data']
        print(data)
        return data['id']
    else:
        print(f'Error: {r.status_code}')
        return None