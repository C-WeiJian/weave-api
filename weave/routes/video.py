import os
from flask import jsonify, request, send_from_directory
from faker import Faker
# import twilio
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ConversationsGrant, VideoGrant

import sys

from weave import application as app

# fake = Factory.create()
fake = Faker()


@app.route('/video')
def video_html():
    # root_dir = os.path.dirname(os.getcwd())
    # print(root_dir)

    return send_from_directory(app.static_folder, 'index.html')


@app.route('/token')
def token():
    # get credentials for environment variables
    # account_sid = os.environ['TWILIO_ACCOUNT_SID']
    # api_key = os.environ['TWILIO_API_KEY']
    # api_secret = os.environ['TWILIO_API_SECRET']

    account_sid = os.environ['account_sid']
    api_key = os.environ['api_key']
    api_secret = os.environ['api_secret']

    # Create an Access Token
    token = AccessToken(account_sid, api_key, api_secret)

    # Set the Identity of this token
    token.identity = fake.user_name()

    # Grant access to Video
    # grant = VideoGrant(room='cool room')
    grant = VideoGrant()
    token.add_grant(grant)

    # Return token info as JSON
    return jsonify(identity=token.identity, token=token.to_jwt().decode('utf-8'))