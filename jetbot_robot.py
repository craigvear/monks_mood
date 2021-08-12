# SERVER SIDE TEST
#
# import socket
#
#
# def Main():
#     host = '192.168.1.123'  # Server ip
#     port = 5000
#
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.bind((host, port))
#
#     print("Server Started")
#     while True:
#         data, addr = s.recvfrom(1024)
#         data = data.decode('utf-8')
#         print("Message from: " + str(addr))
#         print("From connected user: " + data)
#         data = data.upper()
#         print("Sending: " + data)
#         s.sendto(data.encode('utf-8'), addr)
#     s.close()
#
#
# if __name__ == '__main__':
#     Main()
#



"""this script sits in a robot, opens a socket
 and recieves raw date that it translates into movement """

from jetbot.robot import Robot
import socket
import fcntl
import struct
import sys

class Server:
    def __init__(self):
        # get IP address
        host_name = self.get_ip_address('wlan0')
        self.HOST = socket.gethostbyname(host_name) # Server ip (own)
        self.PORT = 5000
        print(f'name {host_name}, ip addr is {self.HOST}, port = {self.PORT}')
        # instantiate a class object to control the jetbot
        self.bot = Robot()
        self.running = True

    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', bytes(ifname[:15], 'utf-8'))
        )[20:24])

    # open server and wait for commands
    def start(self):
        # open server
        while self.running:
            print(f"client: connecting to {self.HOST}:{self.PORT}")
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as self.s:
                self.s.bind((self.HOST, self.PORT))
                # self.s.listen()
                # server_stream, addr = self.s.accept()
                # with server_stream:
                #     print('Connected by', addr)
                self.connected = True
                while self.connected:
                    # get data from stream
                    raw_data, addr = self.s.recvfrom(1024)

                    # convert to from string to float
                    data = float(raw_data)
                    print(f"receiver: got data {data} from {addr}")

                    # listen for stop value from AI
                    if data == 99999:
                        self.terminate()

                    # send to parse and move bot
                    self.parse_data(data)

    def terminate(self):
        self.s.close()
        sys.exit()

    def parse_data(self, data):
        # rescale data to move
        data /= 100

        # new_value = ( (old_value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min
        # scaled_data = int(((data - 0) / (1 - 0)) * (10 - -10) + -10)
        scaled_data = ((data - 0) / (1 - 0)) * (10 - -10) + -10

        # neg number turns bot left, pos turns bot right
        if scaled_data < 0:
            self.bot.left(scaled_data * -1)
        else:
            self.bot.right(scaled_data)

if __name__ == '__main__':
    client = Server()
    client.start()


