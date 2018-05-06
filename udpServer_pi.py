import socket
import sys
import serial
import serial.tools.list_ports
from serial.serialutil import SerialException
import time

baudrate = 57600

#==== find COM port for Teensy ====
def get_teensy_port():
    teensy_port = list(serial.tools.list_ports.grep("16c0"))
    if len(teensy_port) == 1:
        print("Automatically found Teensy: {}".format(teensy_port[0]))
        return teensy_port[0][0]
    else:
        ports = list(serial.tools.list_ports.comports())
        port_dict = {i:[ports[i],ports[i].vid] for i in range(len(ports))}
        teensy_id=None
        for p in port_dict:
            print("{}:   {} (Vendor ID: {})".format(p,port_dict[p][0],port_dict[p][1]))
            if port_dict[p][1]==5824:
                teensy_id = p
        if teensy_id== None:
            return False
        else:
            print("Teensy Found: Device {}".format(p))
            return port_dict[teensy_id][0][0]

#connect to COM port
teensyPort = get_teensy_port()

ser = serial.Serial(teensyPort, timeout = 0.1, baudrate = baudrate)
print("Connected to Teensy at " + str(teensyPort))
#sleep for 2 seconds

time.sleep(2)


def main():
    #DGRAM = datagram
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #by default, socket is TCP so we should specify it is UDP
    host = '192.168.1.100'
    port = 5000
    
    #bind socket to port
    s.bind((host, port))

    print("Server started.")

    #UDP is connectionless
    while True:
        #no connection to receive from. just store data and addr
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print("Message from: " + str(addr))
        print("From connected user: " + data)
        data.upper()

        print("Sending: " + data)
        s.sendto(data.encode('utf-8'), addr)
        
        ser.write(data.encode("utf-8"))
        #sleep for 100 ms
        time.sleep(0.1)
        ser.flush()

    s.close()

if __name__ == '__main__':
    main()
