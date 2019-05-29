def sampling(channel=0, seconds=1, freq_hz=1000, max_speed_hz=1350000):
    from datetime import datetime
    import spidev, time
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz = max_speed_hz 

    def do_sample(s=0):
        begin = datetime.now()
        samples = []
        while (datetime.now() - begin).total_seconds() <= seconds:
            r = spi.xfer2([1, (0x08+channel)<<4, 0])
            samples.append(((r[1]&0x03)<<8) + r[2])
            if s > 0:
                time.sleep(s)
        return samples

    expected = freq_hz * seconds

    result = []
    samples = do_sample(0)
    step = len(samples) / expected
    for i in range(expected):
        result.append(samples[int(i * step)])
    return result

def display(ts):
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt

    fs=np.fft.fft(ts)
    fsr=list(map(lambda e:e.real, fs))
    plt.subplot(211)
    plt.plot(ts)
    plt.subplot(212)
    plt.plot(fsr)
    plt.show()