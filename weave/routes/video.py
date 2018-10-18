import os
from flask import jsonify, request, send_from_directory
from faker import Faker
# import twilio
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ConversationsGrant, VideoGrant
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

import sys

from weave import application as app

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


@app.route('/token/<device_type>')
def token_phone(device_type):
    # get credentials for environment variables
    # account_sid = os.environ['TWILIO_ACCOUNT_SID']
    # api_key = os.environ['TWILIO_API_KEY']
    # api_secret = os.environ['TWILIO_API_SECRET']

    create_room('hello')

    account_sid = os.environ['account_sid']
    api_key = os.environ['api_key']
    api_secret = os.environ['api_secret']

    # Create an Access Token
    token = AccessToken(account_sid, api_key, api_secret)

    # Set the Identity of this token
    token.identity = device_type

    # Grant access to Video
    # grant = VideoGrant(room='cool room')
    grant = VideoGrant()
    token.add_grant(grant)

    # Return token info as JSON
    return jsonify(identity=token.identity, token=token.to_jwt().decode('utf-8'))


@app.route('/room/<room_name>/setup')
def room_setup(room_name):
    # get credentials for environment variables
    # account_sid = os.environ['TWILIO_ACCOUNT_SID']
    # api_key = os.environ['TWILIO_API_KEY']
    # api_secret = os.environ['TWILIO_API_SECRET']

    status = create_room(room_name)

    # Return token info as JSON
    return jsonify(success=status)


def create_room(room_name):
    account_sid = os.environ['account_sid']

    # Your Account Sid and Auth Token from twilio.com/console
    auth_token = os.environ['auth_token']
    client = Client(account_sid, auth_token)

    try:
        client.video.rooms('hello').fetch()
    except TwilioRestException:
        room = client.video.rooms.create(
            record_participants_on_connect=True,
            status_callback='http://weave-sg.herokuapp.com/videocallback',
            status_callback_method="POST",
            type='group',
            unique_name=room_name
        )
        return True

    return False


@app.route('/videocallback', methods=['POST'])
def room_callback():
    # get credentials for environment variables
    # account_sid = os.environ['TWILIO_ACCOUNT_SID']
    # api_key = os.environ['TWILIO_API_KEY']
    # api_secret = os.environ['TWILIO_API_SECRET']
    data = request.get_data()

    # account_sid = os.environ['account_sid']
    # api_key = os.environ['api_key']
    # api_secret = os.environ['api_secret']

    # # Your Account Sid and Auth Token from twilio.com/console
    # auth_token = os.environ['auth_token']
    # client = Client(account_sid, auth_token)

    # room = client.video.rooms.create(
    #                             record_participants_on_connect=True,
    #                             status_callback='http://weave-sg.herokuapp.com/videocallback',
    #                             status_callback_method= "POST",
    #                             type='group',
    #                             unique_name='hello'
    #                         )

    # print(room.sid)

    # Return token info as JSON
    return jsonify(success=True)
