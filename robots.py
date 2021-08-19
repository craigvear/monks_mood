"""recieves data from main,
makes a sound using a dedictaed instrument audio dir,
and controls a robot movement using serial.

NOTE - this will need to be initiated as an independent thread or Trio nursery"""

import socket
from time import sleep
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play
from glob import glob
import trio

# controls comms socket
class Robot:
    def __init__(self, name, ip, port):
        print(f'making robot {name} daddio, with {ip, port}')
        self.NAME = name
        self.HOST = ip
        self.PORT = 5000

        # get own ip address
        self.this_host = socket.gethostbyname(socket.gethostname())
        self.port = port

        self.server = (self.HOST, self.PORT)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.this_host, port))

        self.pan_law = 0


    def transmit(self, message):
        self.s.sendto(message.encode('utf-8'), self.server)
        # data, addr = self.s.recvfrom(1024)
        # data = data.decode('utf-8')
        # print("Received from server: " + data)
        # message = input("-> ")
        # self.s.close()

    def make_sound(self, incoming_raw_data):
        while True:
            # # temp random num gen
            # rnd = randrange(self.audio_dir_len)
            # print(self.audio_dir[rnd])

            # rescale incoming raw data
            audio_dir_position = int(((incoming_raw_data - 0) / (1 - 0)) * (self.audio_dir_len - 0) + 0)

            # make a sound from incoming data
            snippet = AudioSegment.from_wav(self.audio_dir[audio_dir_position])

            # pan snippet
            pan_snippet = snippet.pan(self.pan_law)

            # get the robot to move with
            play(pan_snippet)

            # prepare wait time and then move bot
            wait_time = snippet.duration_seconds / 10
            self.move_bot(incoming_raw_data, wait_time)

    def move_bot(self, move_data, wait_time):
        # print ('made it to bot move')

        self.s.sendto(move_data.encode('utf-8'), self.server)
        data, addr = self.s.recvfrom(1024)
        data = data.decode('utf-8')
        print("Received from server: " + data)

        sleep(wait_time)


# instantiate all the robots comms
class Control:
    def __init__(self):
        # instantiate the robots
        bass_bot = Robot('bass', '192.168.1.124', 4005)
        sax_bot = Robot('sax', '192.168.1.123', 4006)
        tromb_bot = Robot('tromb', '192.168.1.125', 4007)

    async def build_bots(self):
        # init all bots
        print("parent: started!")

        async with trio.open_nursery() as nursery:
            # spawning sax soundbot
            print("parent: spawning sax bot ...")
            nursery.start_soon(self.bot_comms(self.robot_data[0]))

            # spawning bass soundbot
            print("parent: spawning bass bot ...")
            nursery.start_soon(self.bot_comms(self.robot_data[1]))

            # spawning tromb soundbot
            print("parent: spawning tromb bot ...")
            nursery.start_soon(self.bot_comms(self.robot_data[2]))

    async def bot_comms(self, info):
        # listens to the main.py ready to recieve data to a) move bot and b) make a sound
        #
        # open a socket for comms
        self.NAME = info[0]  # name of bot/ instrument
        self.HOST = info[1]  # Client IP (there)
        self.PORT = 5000

        # get own ip address
        host = socket.gethostbyname(socket.gethostname())
        port = info[2]  # port here

        self.server = (self.HOST, self.PORT)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((host, port))


if __name__ == '__main__':
    bot = Robot('bass', 0, 0)
    bot.make_sound(0.2)