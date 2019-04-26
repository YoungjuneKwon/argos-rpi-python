def sampling(channel=0, seconds=1, freq_hz=1000, max_speed_hz=1350000, retry=30, adjust_strength=1.5, tolerance=0):
    from datetime import datetime
    import spidev, time
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz = max_speed_hz 

    def estimate_time():
        arr = []
        begin = datetime.now()
        arr.append(spi.xfer2([1, (0x08+channel)<<4, 0]))
        return (datetime.now() - begin).total_seconds()

    def do_sample(s):
        begin = datetime.now()
        samples = []
        while (datetime.now() - begin).total_seconds() <= seconds:
            samples.append(spi.xfer2([1, (0x08+channel)<<4, 0]))
            if s > 0:
                time.sleep(s)
        return samples

    s = (1 / freq_hz) - estimate_time()
    expected = freq_hz * seconds

    result = []
    if s >= 0:
        for i in range(retry):
            result = do_sample(s)
            print(len(result))
            dr = abs(len(result) - expected) / expected
            if dr <= tolerance:
                break
            s *= 1 + dr * adjust_strength * (1 if len(result) > expected else -1)
    else:
        samples = do_sample(0)
        step = len(samples) / expected
        for i in range(expected):
            result.append(samples[int(i * step)])
    return result
