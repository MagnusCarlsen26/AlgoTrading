def readBitcoinPrice() -> float:
    with open("output.txt", "r") as file :
        try:
            x = (file.read().strip().split(',')[1])
            bitcoinPrice = float(x)
            return bitcoinPrice
        except Exception as e:
            return readBitcoinPrice()