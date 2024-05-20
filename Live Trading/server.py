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


buy = 0
@socketio.on('order_book_data')  
def handle_order_book_data(data):
    try:
        yes_data, no_data, title, time = extractDate(data)
        yesdf = transform('yes',data,title,time)
        # nodf = transform('no',data,title,time)

        if buy:
            x = exampleTradeSell(yesdf)
            if x:
                buy = 0
                socketio.emit('trade',['sell',x])
        else:
            x = exampleTradeSell(yesdf)
            if x:
                buy = 1
                socketio.emit('trade',['buy',x])
    except Exception as e:
        print("Error processing data:", e)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=6000)  