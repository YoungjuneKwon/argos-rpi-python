import spidev, time, datetime

def sample():
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz = 1350000 

    begin = datetime.datetime.now()
    samples = []
    channel = 0

    print("begin, ", str(datetime.datetime.now()))
    while (datetime.datetime.now() - begin).total_seconds() <= 1:
        samples.append(spi.xfer2([1, (0x08+channel)<<4, 0]))
        print(samples[-1])

    print(len(samples))
    print("end, ", str(datetime.datetime.now()))