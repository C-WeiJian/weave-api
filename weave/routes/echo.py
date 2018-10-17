# import logging

from flask import request, jsonify

from weave import application as app
from weave import db

# logger = logging.getLogger(__name__)


@app.route('/echo', methods=['POST'])
def evaluate():
    data = request.get_json()
    return jsonify(data)

@app.route('/form', methods=['POST'])
def submitform():
    user_id = 'form'
    data = request.get_json()
    db.get(user_id)
    db.update(user_id, data)
    return jsonify(data)

@app.route('/form', methods=['GET'])
def getform():
    user_id = 'form'
    data = db.get(user_id)
    return jsonify(data)

@app.route('/alarm')
def alarm():
    result = db.get_alarm()
    return jsonify(result)


@app.route('/alarm/on')
def alarm_on():
    user_id = 'alarm'
    json_data = db.get_alarm()
    json_data['switch'] = 1
    db.update(user_id, json_data)
    return jsonify(json_data)


@app.route('/alarm/off')
def alarm_off():
    user_id = 'alarm'
    json_data = db.get_alarm()
    json_data['switch'] = 0
    db.update(user_id, json_data)
    return jsonify(json_data)
