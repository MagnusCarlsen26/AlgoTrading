def readBitcoinPrice() -> float:
    with open("output.txt", "r") as file :
        try:
            bitcoinPrice = float(file.read().strip())
            return bitcoinPrice
        except ValueError as e:
            return readBitcoinPrice()