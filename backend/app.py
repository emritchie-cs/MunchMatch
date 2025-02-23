from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/api/test', methods=['POST', 'OPTIONS'])
def test():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        return jsonify({'num': '13'})
    else:
        return jsonify({'message': 'This is a CORS-enabled response for OPTIONS requests.'})

#send to user data

@app.route('/api/intake', methods=['POST'])
def intake():
    data = request.get_json()
    print(data)
    return jsonify({'num': 999})
#run query to return 5 most suited restaurants

#query google maps shittycrap

#do fuckityshitcrapmeow

if __name__ == '__main__':
    app.run()