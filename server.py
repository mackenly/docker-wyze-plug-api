from flask import Flask, request, jsonify
from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError
from wyze_sdk.errors import WyzeClientConfigurationError
import os

app = Flask(__name__)

# Get the API password key from the environment variables
api_password = os.getenv('KEY') or 'mykey'
always_refresh = bool(os.getenv('ALWAYS_REFRESH')) or True
client = Client()

# create client
try:
    print("Using environment variables for USERNAME, PASSWORD, API_KEY, KEY_ID, and TOTP")
    print("Get an API key/id from: https://developer-api-console.wyze.com/#/apikey/view")
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    api_key = os.getenv('API_KEY')
    key_id = os.getenv('KEY_ID')
    totp = os.getenv('TOTP')
    client = Client(email=username, password=password, totp_key=totp, api_key=api_key, key_id=key_id)

    # test the API
    out_test = {}
    for plug in client.plugs.list():
        out_test[plug.mac] = plug.to_dict()
    print("Connected to Wyze API")
except WyzeApiError as error:
    print(f'Got an error: {error}')
except WyzeClientConfigurationError as error:
    print(f'Got an error. May be caused by invalid API KEY/ID: {error}')
except Exception as error:
    print(f'Got an error: {error}')


@app.route('/plug/on', methods=['GET'])
def plug_on():
    if request.args.get('key') == api_password:
        try:
            if always_refresh:
                client.refresh_token()
                print("Token refreshed")
        except WyzeApiError as e:
            print(f'Token refresh error: {e}')
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
            client.refresh_token()
            print("Token refreshed")
    else:
        return jsonify(message="Invalid API key"), 403


@app.route('/plug/off', methods=['GET'])
def plug_off():
    if request.args.get('key') == api_password:
        try:
            if always_refresh:
                client.refresh_token()
                print("Token refreshed")
        except WyzeApiError as e:
            print(f'Token refresh error: {e}')
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
            client.refresh_token()
            print("Token refreshed")
    else:
        return jsonify(message="Invalid API key"), 403


@app.route('/plug', methods=['GET'])
def plug_list():
    # Check the 'X-Api-Key' header of the request
    if request.args.get('key') == api_password:
        try:
            if always_refresh:
                client.refresh_token()
                print("Token refreshed")
        except WyzeApiError as e:
            print(f'Token refresh error: {e}')
        if request.args.get('macs') is not None:
            result = []
            try:
                macs = request.args.get('macs').split(',')
                for mac in macs:
                    plug = client.plugs.info(device_mac=mac)
                    result.append(client.plugs.turn_off(
                        device_mac=plug.mac,
                        device_model=plug.product.model
                    ))
            except WyzeApiError as e:
                print(f'Got an error: {e}')
                client.refresh_token()
                print("Token refreshed")
            return jsonify(message=result.to_dict()), 200
        else:
            out = {}
            try:
                plugs = client.plugs.list()
                for plug in plugs:
                    out[plug.mac] = plug.to_dict()
            except WyzeApiError as e:
                print(f'Got an error: {e}')
                client.refresh_token()
                print("Token refreshed")
            return jsonify(out), 200
    else:
        return jsonify(message="Invalid API key"), 403


if __name__ == "__main__":
    # Note: Make sure to use '0.0.0.0' as the host in Docker
    app.run(host='0.0.0.0', port=5000)
