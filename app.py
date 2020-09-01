from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name':"My wonderful store",
        'items':[
            {
                'name':"My item",
                'price': 15.99
            }
        ]
    }
]


@app.route("/", methods=['GET'])
def handler():
    return "hello word"

@app.route("/store", methods=["POST"])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items':[]
    }
    stores.append(new_store)
    return jsonify(new_store)

@app.route("/store/<string:name>", methods=["GET"])
def get_store(name):
    print(name)
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message':"not found"})

@app.route("/store", methods=["GET"])
def get_stores():
    return jsonify({'store': stores})

@app.route("/store/<string:name>/item", methods=["POST"])
def create_store_item(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message':"not found"})

@app.route("/store/<string:name>/item", methods=["GET"])
def get_store_item(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store['items'])
    return jsonify({'message': 'not found'})

app.run(port=3000)