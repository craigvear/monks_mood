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
from pydub.playback import _play_with_simpleaudio as play
from pydub.playback import play
from instrument import Robot
import trio
import concurrent.futures
import socket
from engine_client import Client
import pickle
import pyaudio
import numpy as np
from random import random
from time import sleep, time

class Master:
    def __init__(self):
        self.running = False

        # get own ip address
        ip = socket.gethostbyname(socket.gethostname())
        self.HOST = ip  # Client IP (this)
        self.PORT = 5000


        # # instantiate all performer class's
        # sax_ip = input('please enter sax bot IP e.g. 192.168.1.123 (x if not available)')
        # if sax_ip != 'x':
        #     self.sax_bot = Robot(instrument='sax', port=5000, addr=sax_ip)
        #     self.sax_bot_flag = True
        #     self.make_connection()
        #
        # tromb_ip = input('please enter tromb bot IP e.g. 192.168.1.123 (x if not available)')
        # if tromb_ip != 'x':
        #     self.tromb_bot = Robot(instrument='trombone', port=5000, addr=tromb_ip)
        #     self.tromb_bot_flag = True
        #
        # bass_ip = input('please enter bass bot IP e.g. 192.168.1.123 (x if not available)')
        # if bass_ip != 'x':
        #     self.bass_bot = Robot(instrument='bass', port=5000, addr=bass_ip)
        #     self.bass_bot_flag = True

        # # build send data dict
        # self.send_data_dict = {'mic_level': 0,
        #                        'speed': 1,
        #                        'tempo': 0.1
        #                        }
        #
        # # init got dict
        # self.got_dict = {}

    def make_connection(self, port, host):
        host = '192.168.1.79'  # client ip
        port = 4005

        server_ip = input('server IP ...')

        server = (server_ip, 5000)

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, port))

        message = input("-> ")
        while message != 'q':
            s.sendto(message.encode('utf-8'), server)
            data, addr = s.recvfrom(1024)
            data = data.decode('utf-8')
            print("Received from server: " + data)
            message = input("-> ")
        s.close()

    def engine_stream(self):
        # initiate engine client-server comms
        self.engine = Client()
        self.engine.main()

    async def parent(self):
        print("parent: started!")
        while self.connected:
            async with trio.open_nursery() as nursery:
                # spawning bass soundbot
                if self.bass_bot_flag:
                    print("parent: spawning bass bot ...")
                    nursery.start_soon(self.improv(self.bass_bot))

                # spawning sax soundbot
                if self.sax_bot_flag:
                    print("parent: spawning sax bot ...")
                    nursery.start_soon(self.improv(self.sax_bot))

                # spawning tromb soundbot
                if self.tromb_bot_flag:
                    print("parent: spawning tromb bot ...")
                    nursery.start_soon(self.improv(self.tromb_bot))

    def improv(self, bot):
        # grab raw data from engine stream
        raw_data_from_dict = self.engine.got_dict['master_output']

        # hand it to which ever bot is calling for it
        bot.make_sound(raw_data_from_dict)

    # def parent_go(self):
    #     # wait for intro to finish
    #     while self.running:
    #         if not self.improv:
    #             sleep(0.1)
    #
    #     # then start improvisers
    #         else:
    #             trio.run(self.parent)

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
        play(mixed_intro)

    def main(self):
        # Thread the conductor, engine stream and each of the robot objects
        tasks = [self.conducter, self.engine_stream]

        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            futures = {executor.submit(task): task for task in tasks}

    # this func organises the overall composition of the performance
    def conducter(self):
        # wait for engine stream to work
        while self.engine.connected:
            self.running = True
            # start the whole performance with the intro
            self.play_intro()

            # then opens the conditions for improv,
            now = time()
            while time() < now + 180: # = 3 min improv
                self.improv = True

            # then closes them for outro
            self.improv = False
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
