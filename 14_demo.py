import pyb
import sensor, image, time, os, tf

uart = pyb.UART(3,9600,timeout_char=1000)
uart.init(9600,bits=8,parity = None, stop=1, timeout_char=1000)
tmp = ""

def qrcode():
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.skip_frames(time = 2000)
    sensor.set_auto_gain(False) # must turn this off to prevent image washout...
    clock = time.clock()
    flag = True
    while(flag):
        clock.tick()
        img = sensor.snapshot()
        img.lens_corr(1.8) # strength of 1.8 is good for the 2.8mm lens.
        info = img.find_qrcodes()
        if (info):
            flag = False
            for code in info:
                img.draw_rectangle(code.rect(), color = (255, 0, 0))
            print(info[0][4])
            for a in info[0][4]:
                print(a)
                uart.write(a)
                time.sleep(5)
            #uart.write(("%s" % info[0][4]).encode())
        #print(clock.fps())

        #flag = False
            #return info[0][4]

while(1):
   a = uart.readline()
   if a is not None:
      tmp += a.decode()
      print(a.decode())

   if tmp == "qrcode":
      #print("classify images")
      tmp =""
      qrcode()
      #print(label)
      #uart.write(label.encode())
      #uart.write(("FPS %f\r\n" % clock.fps()).encode())
