"""recieves data from main,
makes a sound using a dedictaed instrument audio dir,
and controls a robot movement using serial.

NOTE - this will need to be initiated as an independent thread or Trio nursery"""

import socket
from time import sleep
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play
from glob import glob

class Robot:
    def __init__(self, local_ip, instrument, port, addr):
        print(f'instantiated {instrument} bot, on port {port}')
        this_ip = local_ip
        self.instrument = instrument
        self.PORT = port
        self.IP_ADDR = addr
        self.running = False
        self.audio_dir = glob(f'assets/{instrument}/*.wav')
        self.audio_dir_len = len(self.audio_dir)

        # todo start serial connection with actual robot

        # deal with pan laws
        if instrument == 'sax':
            self.pan_law = -0.5
        elif instrument == 'tromb':
            self.pan_law = 0.5
        else:
            self.pan_law = 0


        host = this_ip  # client ip (this laptop)
        self.server = (self.IP_ADDR, self.PORT)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((host, port))

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

if __name__ == '__main__':
    bot = Robot('bass', 0, 0)
    bot.make_sound(0.2)