import socket

def main():
    host = '127.0.0.1'
    port = 5000 #port for server

    #pass tuple of host and port
    #DGRAM = datagram
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #by default, socket is TCP so we should specify it is UDP
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

    s.close()

if __name__ == '__main__':
    main()
