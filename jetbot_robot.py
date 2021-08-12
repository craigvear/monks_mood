"""this script sits in a robot, opens a socket
 and recieves raw date that it translates into movement """

from jetbot.robot import Robot
import socket
import sys

class Server:
    def __init__(self):
        # get IP address
        host_name = socket.gethostname()
        # self.HOST = socket.gethostbyname(host_name)
        self.HOST = '192.168.1.123'
        self.PORT = 54321
        print(f'name {host_name}, ip addr is {self.HOST}, port = {self.PORT}')
        # instantiate a class object to control the jetbot
        self.bot = Robot()
        self.running = True

    # open server and wait for commands
    def start(self):
        # open server
        while self.running:
            print(f"client: connecting to {self.HOST}:{self.PORT}")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
                self.s.bind((self.HOST, self.PORT))
                self.s.listen()
                client_stream, addr = self.s.accept()
                with client_stream:
                    print('Connected by', addr)
                    self.connected = True
                    while self.connected:
                        # get data from stream
                        raw_data = client_stream.recv(1024)

                        # convert to decimal
                        data = int(raw_data, 16)
                        print(f"receiver: got data {data}")

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


