# import logging

from flask import request, jsonify

from weave import application as app
from weave import db

# logger = logging.getLogger(__name__)


@app.route('/echo', methods=['POST'])
def evaluate():
    data = request.get_json()
    app.logger.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input")
    result = inputValue * inputValue
    app.logger.info("My result :{}".format(result))
    return jsonify(result)


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
