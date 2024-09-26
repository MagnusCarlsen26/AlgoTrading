from utility.api import buy,buyBook,cancel_order,sell,trade_status,getBuyPrice,collectBitcoinPriceFromProbo, collectEventPrice, collectBitcoinData ,collectBitcoinPriceFromBinance
import threading

thread1 = threading.Thread(target=collectBitcoinPriceFromProbo, args=())
thread2 = threading.Thread(target=collectBitcoinPriceFromBinance, args=())
thread3 = threading.Thread(target=collectBitcoinData,args=([2449]))

thread1.start()
thread2.start()
thread3.start()