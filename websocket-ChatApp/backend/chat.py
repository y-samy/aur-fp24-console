from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Allow cross-origin requests
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")
@app.route('/')
def index():
    return "WebSocket server is running."
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('response', {'data': 'Welcome to the WebSocket server!'})

@socketio.on('send_message')  # Listen for this event from the client
def handle_send_message(data):
    coordinates = data['message']
    if coordinates.startswith("x") and "," in coordinates:
        try:
            coordinate = coordinates.split(",")
            # Split to remove the 'x=' and 'y=' prefixes
            x_part = coordinate[0].strip() 
            y_part = coordinate[1].strip()
            # Further split to extract the values
            x_value = float(x_part.split("=")[1].strip())  # Get the value of x
            y_value = float(y_part.split("=")[1].strip())  # Get the value of y
            # Send the response to the client
            if y_value > 3:
                response_message = f"Client moved to ({x_value}, {y_value} , you need to scan.)."
            
            else:
                response_message = f"Client moved to ({x_value}, {y_value})."
        except (IndexError, ValueError):

            print("Invalid coordinate format")
            response_message = "Invalid format. Please use 'x = 15, y = 20'."

    else :
        response_message = f"Server received: {coordinates}"

    print(f"Message received from client: {coordinates}")
    emit('response', {'data': response_message}, broadcast=True) # Send response back to the client

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
