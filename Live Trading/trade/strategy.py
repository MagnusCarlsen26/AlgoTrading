def strategy(type,data,title):
    i = 0.5
    d = {}
    while i<10:
        d[i] = 0
        i += 0.5
    print(data)
    for i in range(len(data)):
        if data[i]['price'] !=  0:
            d[data[i]['price']] = data[i]['quantity']
    transposed_data = {str(key): [value] for key, value in d.items()}

    lst = []
    for i in transposed_data.keys():
        lst.append(transposed_data[i][0])
    trade(lst)
