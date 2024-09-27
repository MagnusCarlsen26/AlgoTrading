def readBitcoinPrice() -> float:
    with open("logs/binancePrice.txt", "r") as file :
        try:
            x = (file.read().strip())
            bitcoinPrice = float(x)
            return bitcoinPrice
        except Exception as e:
            return readBitcoinPrice()