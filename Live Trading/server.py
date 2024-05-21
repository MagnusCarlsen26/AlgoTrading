from flask import Flask, request, jsonify
from flask_cors import CORS
# from save import save
from flask_socketio import SocketIO, emit
from transform import transform
from exampleTrade import exampleTradeBuy,exampleTradeSell
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  

def extractDate(data):
    yes_data = data.get('yesData')
    no_data = data.get('noData')
    title = data.get('title')[-9:][:8].replace(':','-')
    time = data.get('currentTime')
    return yes_data,no_data,title,time


buy = 1
sell = 0
@socketio.on('order_book_data')  
def handle_order_book_data(data):
    global buy,sell
    yes_data, no_data, title, time = extractDate(data)
    yesdf = transform('yes',yes_data,title,time)
    # nodf = transform('no',data,title,time)
    print(buy,sell)
    if buy and not sell:
        print('Checking for buy')
        x = exampleTradeBuy(yesdf)
        if x:
            buy = 0
            socketio.emit('buy',x)
    elif not buy and sell:
        print('Checking for sell ')
        x = exampleTradeSell(yesdf)
        if x:
            print('SELL')
            buy = 1
            socketio.emit('sell',x)


@socketio.on('confirmBuy')
def confirmBuy(data):
    if data == 1:
        sell = 1
    print(buy,sell,'g')

@socketio.on('confirmSell')
def confirmSell(data):
    if data == 1 :
        sell = 0


if __name__ == '__main__':
    socketio.run(app, debug=True, port=8080)  