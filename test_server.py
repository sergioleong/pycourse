from flask import Flask,request, jsonify
import json

app = Flask(__name__)

cur_data =[]


required_keys = ['name','age']
            
@app.route("/", methods=['GET'])
def index():
    global cur_data
    return jsonify(error=200, data=cur_data), 200

@app.route("/<int:id>", methods=['GET'])
def get_id(id):
    global cur_data
    try:
        id = int(id)
        print(type(id))
        for i in range(len(cur_data)):
            if cur_data[i]['id']==id:
                return jsonify(data=cur_data[i]), 200
        else:
            return jsonify(error=404, text="Object not found"), 404
    except Exception as e:
        return jsonify(error=400, text="Invalid input"), 400
        
@app.route("/<int:id>", methods=['DELETE'])
def delete_id(id):
    global cur_data
    try:
        id = int(id)
        print(id)
        res = [i for i in cur_data if i['id'] != id]
        if len(res) == len(cur_data):
            return jsonify(error=404, text="Object not found"), 404
        else:
            cur_data = res
            return jsonify(success=True, text="Object deleted", cur_data=res), 202
    except Exception as e:
        print(e)
        return jsonify(error=400, text="Invalid input", exception=e), 400
    

@app.route("/add", methods=['PUT'])
def add():
    global cur_data
    global required_keys
    try:
        data = request.json
        keys = data.keys()

        if 'id' in required_keys:
            return jsonify(error=500, text="Cannot add object with id"), 500

        for key in required_keys:
            if key not in keys:
                return jsonify(error=500, text=f"Missing required key {key}"), 500
                
        id = len(cur_data) + 1
        data['id'] = id
        cur_data.append(data)

        return jsonify(success=True, data=data), 201

    except Exception as e:
        return jsonify(error=500, text=str(e)), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='43560')