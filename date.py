from struct import *

with open('F:\\Program Files (x86)\\newone\\vipdoc\\sz\\lday\\sz000002.day', 'rb') as fh:
    fc = fh.read()
    data_num = len(fc) / 32
    data = unpack('IIIIIfII' * data_num, fc)
    stock_per_day = []
    for i in range(data_num):
        stock_per_day.append(data[i*8:i*8+7])
        print stock_per_day[-1]
    print data_num
