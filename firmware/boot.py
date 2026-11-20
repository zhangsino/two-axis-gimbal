# boot.py —— 每次开机先执行
# 板载 WS2812（GPIO48）会锁住最后一次颜色，这里开机先清黑，免得一直亮着
try:
    from machine import Pin
    try:
        import neopixel
    except ImportError:
        import ws2812 as neopixel
    _np = neopixel.NeoPixel(Pin(48), 1)
    _np[0] = (0, 0, 0)
    _np.write()
    del _np
except Exception:
    pass

# 下面这些是原厂模板，留着而已，都没开
# import esp
# esp.osdebug(None)
# import webrepl
# webrepl.start()
