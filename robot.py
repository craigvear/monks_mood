"""recieves data from main,
makes a sound using a dedictaed instrument audio dir,
and controls a robot movement using serial"""

from time import sleep
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play
from glob import glob
from random import randrange

class Robot:
    def __init__(self, instrument, port, addr):
        print(f'instantiated {instrument} bot, on port {port}')
        self.instrument = instrument
        self.PORT = port
        self.IP_ADDR = addr
        self.running = False
        self.audio_dir = glob(f'assets/{instrument}/*.wav')
        self.audio_dir_len = len(self.audio_dir)

        # deal with pan laws
        if instrument == 'sax':
            self.pan_law = -0.5
        elif instrument == 'tromb':
            self.pan_law = 0.5
        else:
            self.pan_law = 0

    def make_sound(self, incoming_raw_data):
        while True:
            # temp random num gen
            rnd = randrange(self.audio_dir_len)
            print(self.audio_dir[rnd])

            # make a sound from incoming data
            snippet = AudioSegment.from_wav(self.audio_dir[rnd])

            # pan snippet
            pan_snippet = snippet.pan(self.pan_law)

            # get the robot to move with
            play(pan_snippet)

            # prepare wait time and then move bot
            wait_time = snippet.duration_seconds / 10
            self.move_bot(incoming_raw_data, wait_time)

    def move_bot(self, move_data, wait_time):
        print ('made it to bot move')
        sleep(wait_time)

if __name__ == '__main__':
    bot = Robot('sax', 0, 0)
    bot.make_sound(2)