# main.py
from flask import Flask, Response
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from mqtt_client import create_mqtt_client, publish_message, stop_mqtt
from api.video_api import video_api

app = Flask(__name__)



app.register_blueprint(video_api, url_prefix='/video')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True, use_reloader=False)