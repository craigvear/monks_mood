####################################
#
# Monks Mood - main script
# © CVEAR 2021
# cvear@dmu.ac.uk
# 11 August 2021
#
####################################



"""engine works in isolation from Terminal bash
this script coordinates
1) the client comms with engine - mic listener tx and dataset rx
2) instantiating 3 robot performers
3) parsing and organising data to each performer
4) the opverall organisation of intro, improv, outro"""

from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as playsim
from pydub.playback import play
from robots import Robot
import trio
import concurrent.futures
import socket
from engine_client import Client
from time import sleep, time
from subprocess import Popen

class Master:
    def __init__(self):
        # get own ip address
        self.ip = socket.gethostbyname(socket.gethostname())
        self.HOST = self.ip  # Client IP (this)
        self.PORT = 5000

        # inits
        self.running = False
        self.improv_go = False

        # robot instrument vars
        self.pan_law = 0
        audio_path = 'assets/alfie.mp3'
        self.audio_file = AudioSegment.from_mp3(audio_path)
        self.audio_file_len_ms = self.audio_file.duration_seconds * 1000
        print(f'audio dur in msecs = {self.audio_file_len_ms}')
        Popen('python3 engine_server.py', shell=True)

    def engine_stream(self):
        # initiate engine client-server comms
        self.engine = Client()
        self.engine.main()

    def make_sound(self, incoming_raw_data, rhythm_rate):
        # # temp random num gen
        # rnd = randrange(self.audio_dir_len)
        # print(self.audio_dir[rnd])
        print('making sound')

        # rescale incoming raw data
        audio_play_position = int(((incoming_raw_data - 0) / (1 - 0)) * (self.audio_file_len_ms - 0) + 0)
        duration = rhythm_rate + 1000
        end_point = audio_play_position + duration
        print(audio_play_position, end_point, duration)

        # make a sound from incoming data
        snippet = self.audio_file[audio_play_position: end_point]
        print('snippet')

        # pan snippet
        pan_snippet = snippet.pan(self.pan_law)
        print('pan')

        # get the robot to move with
        playsim(snippet)
        print('play')

        # prepare wait time and then move bot
        # wait_time = snippet.duration_seconds / 1000
        # self.move_bot(incoming_raw_data, duration)

        sleep(duration/ 1000)
        print('fininshed a play')

    def move_bot(self, move_data, wait_time):
        print ('made it to bot move')
        #
        # self.s.sendto(move_data.encode('utf-8'), self.server)
        # data, addr = self.s.recvfrom(1024)
        # data = data.decode('utf-8')
        # print("Received from server: " + data)

        sleep(wait_time * 10)

    def robot(self):
        # make a serial port connection here
        print('im here1')
        # loop here
        # while self.running:
        #     print('im here2')

        while not self.improv_go:
            print('im here3')
            sleep(1)
            print('sleeping robot')

    # then start improvisers
        while self.improv_go:
            print('im here4')
            # grab raw data from engine stream
            raw_data_from_dict = self.engine.got_dict['master_output']
            rhythm_rate = self.engine.got_dict['rhythm_rate']
            print(raw_data_from_dict, rhythm_rate)

            # make a sound & move bot
            self.make_sound(raw_data_from_dict, rhythm_rate)
            print('making a new one')

    # play the intro head and wait to finish
    def play_intro(self):
        # get sax's part
        alfie = AudioSegment.from_wav('assets/alfie_intro.wav')

        # pan sax
        alfieLeft = alfie.pan(-0.5)

        # get bass part
        bass = AudioSegment.from_wav('assets/bass_intro.wav')

        # mix them all together
        mixed_intro = bass.overlay(alfieLeft)

        # play and wait for it to finish
        # play(mixed_intro)
        print('gonna sleep for 10 as temp intro')
        sleep(10)

    def main(self):
        # self.running = True
        # Thread the conductor, engine stream and each of the robot objects
        tasks = [self.conducter,
                 self.engine_stream]
                 # self.robot] #

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(task): task for task in tasks}

    # this func organises the overall composition of the performance
    def conducter(self):
        # wait for engine stream to work
        while not self.running:
            sleep(1)
            if self.engine.connected:
                self.running = True
                print('engine running = true')

        # start the whole performance with the intro
        self.play_intro()
        print('I======================   IMPROV GOOOOOOOOOOOOO')
        self.improv_go = True

        # then opens the conditions for improv,
        now = time()
        while time() < now + 180: # = 3 min improv
            # self.improv_go = True
            print('improving')
            sleep(1)

        # then closes them for outro
        self.improv_go = False
        #self.play_outro()

        # terminate all threads etc
        self.engine.terminate()
        self.terminate()

    def terminate(self):
        #self.executor.shutdown()
        pass

if __name__ == '__main__':
    mstr = Master()
    mstr.main()
    # mstr.make_sound(0.12345, 0.12)