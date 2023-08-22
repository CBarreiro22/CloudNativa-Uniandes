from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/users/me', methods=['GET'])
def mock_response():
    response_data = {
        "id": "468dca05-3aa5-4d84-8e70-93b8b54f7a15"
    }
    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(host='localhost', port=3000)
