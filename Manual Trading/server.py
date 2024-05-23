from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from transform import transform

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  


ratio = 5

def startegy(lst):
    lowest = lst[0]['quantity']
    lowerBuy = lst[0]['price']
    if lowest == 0:
        return 
    higher = 0
    for i in range(1,len(lst)):
        higher += lst[i]['quantity']
    if higher/lowest > ratio:
        print(f'Buy {lowerBuy} ,{lowest}')

@socketio.on('order_book_data')  
def handle_order_book_data(data):
    global buy,sell
    yes_data = data.get('yesData')
    startegy(yes_data)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=8080)  