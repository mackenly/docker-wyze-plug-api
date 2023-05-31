from flask import Flask, request, jsonify
from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError
import os

app = Flask(__name__)

# Get the API key from the environment variables
api_key = os.getenv('KEY') or 'mykey'
client = None

# create client
if os.getenv('TOKEN') is None:
    try:
        print("Using environment variables for USERNAME and PASSWORD")
        print("Note: Only use this if 2FA is not enabled on your account, else it will fail")
        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        client = Client(email=username, password=password)

        # test the API
        out = {}
        for plug in client.plugs.list():
            out[plug.mac] = plug.to_dict()
        print("Connected to Wyze API")
    except WyzeApiError as e:
        print(f'Got an error: {e}')
else:
    try:
        print("Using environment variable for TOKEN")
        print("Get token from start.py")
        start_token = os.getenv('TOKEN')
        client = Client(token=start_token)

        # test the API
        out = {}
        for plug in client.plugs.list():
            out[plug.mac] = plug.to_dict()
        print("Connected to Wyze API")
    except WyzeApiError as e:
        print(f'Got an error: {e}')


@app.route('/plug/on', methods=['POST'])
def plug_on():
    if request.args.get('key') == api_key:
        try:
            macs = request.args.get('macs').split(',')
            result = None
            for mac in macs:
                plug = client.plugs.info(device_mac=mac)
                result = client.plugs.turn_on(
                    device_mac=plug.mac,
                    device_model=plug.product.model
                )
            return jsonify(message=result.data), result.status_code
        except WyzeApiError as e:
            print(f'Got an error: {e}')
    else:
        return jsonify(message="Invalid API key"), 403


@app.route('/plug/off', methods=['POST'])
def plug_off():
    if request.args.get('key') == api_key:
        try:
            macs = request.args.get('macs').split(',')
            result = None
            for mac in macs:
                plug = client.plugs.info(device_mac=mac)
                result = client.plugs.turn_off(
                    device_mac=plug.mac,
                    device_model=plug.product.model
                )
            return jsonify(message=result.data), result.status_code
        except WyzeApiError as e:
            print(f'Got an error: {e}')
    else:
        return jsonify(message="Invalid API key"), 403


@app.route('/plug', methods=['GET'])
def plug_list():
    # Check the 'X-Api-Key' header of the request
    if request.args.get('key') == api_key:
        if request.args.get('macs') is not None:
            macs = request.args.get('macs').split(',')
            result = []
            for mac in macs:
                plug = client.plugs.info(device_mac=mac)
                result.append(client.plugs.turn_off(
                    device_mac=plug.mac,
                    device_model=plug.product.model
                ))
            return jsonify(message=result.to_dict()), 200
        else:
            plugs = client.plugs.list()
            out = {}
            for plug in plugs:
                out[plug.mac] = plug.to_dict()
            return jsonify(out), 200
    else:
        return jsonify(message="Invalid API key"), 403


if __name__ == "__main__":
    # Note: Make sure to use '0.0.0.0' as the host in Docker
    app.run(host='0.0.0.0', port=5000)
