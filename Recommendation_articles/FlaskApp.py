from flask import Flask, jsonify 


app2 = Flask(__name__)

@app2.route("/test", methods=['POST'])
def main():
    return jsonify('Hellow World')

app2.run(host='127.0.0.1', port=5000)