#!/usr/bin/env python3

from flask import Flask, render_template, jsonify, request
from state import NotifyState
from piResponse import restfulResponse
import json

app = Flask(__name__)
status = NotifyState()
pi_json = restfulResponse('')


@app.route("/")
def index():
    status.state = False
    return render_template('home.html')


@app.route('/data', methods=['GET', 'POST'])
def get_pi_response():
    if (request.method == 'POST'):
        pi_json.Rpi_data = request.get_json()
        print(pi_json.Rpi_data)
        return jsonify({'Status': 'Success'})
    else:
        if (pi_json.Rpi_data == None):
            return 'True'
        else:
            return jsonify(pi_json.Rpi_data)


@app.route('/set-true')
def set_true():
    status.state = True
    return 'True'


@app.route('/set-false')
def set_false():
    status.state = False
    pi_json.Rpi_data = None
    return 'False'


@app.route("/get-status")
def get_status():
    return jsonify({"Status": status.state})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
