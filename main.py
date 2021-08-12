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
import pickle
import pyaudio
import numpy as np
from random import random
from time import sleep


class Client:
    def __init__(self):
        self.running = True
        self.connected = False

        # get own ip address
        ip = socket.gethostbyname(socket.gethostname())
        self.HOST = ip  # Client IP (this)
        self.PORT = 5000
        # Port to listen on (non-privileged ports are > 1023)

        self.CHUNK = 2 ** 11
        self.RATE = 44100
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)

        # instantiate all performer class's
        self.sax_bot = Robot(instrument='sax', port=5000, addr='192.168.1.123')
        self.tromb_bot = Robot(instrument='trombone', port=5000, addr='192.168.1.124')
        self.bass_bot = Robot(instrument='bass', port=5000, addr='192.168.1.125')

        # build send data dict
        self.send_data_dict = {'mic_level': 0,
                               'speed': 1,
                               'tempo': 0.1
                               }

        # init got dict
        self.got_dict = {}

    def client_stream(self):
        print("client: started!")
        while self.running:
            print(f"client: connecting to {self.HOST}:{self.PORT}")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.HOST, self.PORT))
                s.listen()
                client_stream, addr = s.accept()
                with client_stream:
                    print('Connected by', addr)
                    self.connected = True
                    while self.connected:
                        # get data from stream
                        data = client_stream.recv(1024)
                        self.got_dict = pickle.loads(data)
                        print(f"receiver: got data {self.got_dict}")

                        # send it to the mincer for soundBot control
                        # NB play_with_simpleaudio does not hold thread
                        # master_data = self.got_dict['master_output']
                        # rhythm_rate = self.got_dict['rhythm_rate']
                        # self.mincer(master_data, rhythm_rate)

                        # send out-going data to server
                        send_data = pickle.dumps(self.send_data_dict, -1)
                        client_stream.sendall(send_data)

    def snd_listen(self):
        print("mic listener: started!")
        while self.running:
            data = np.frombuffer(self.stream.read(self.CHUNK),
                                 dtype=np.int16)
            peak = np.average(np.abs(data)) * 2
            if peak > 2000:
                bars = "#" * int(50 * peak / 2 ** 16)
                print("%05d %s" % (peak, bars))
            self.send_data_dict['mic_level'] = peak / 30000

    async def parent(self):
        print("parent: started!")
        while self.connected:
            async with trio.open_nursery() as nursery:
                # spawning bass soundbot
                print("parent: spawning bass bot ...")
                nursery.start_soon(self.improv(self.bass_bot))

                # spawning sax soundbot
                print("parent: spawning sax bot ...")
                nursery.start_soon(self.improv(self.sax_bot))

                # # spawning tromb soundbot
                # print("parent: spawning tromb bot ...")
                # nursery.start_soon(self.improv(self.tromb_bot))


    def improv(self, bot):
        raw_data_from_dict = self.got_dict['master_output']
        bot.make_sound(raw_data_from_dict)

    def parent_go(self):
        # start the whole performance with the intro
        # then into drum solo ready for threading to kick in
        self.play_intro()

        # then start inprovisers
        while self.running:
            if not self.connected:
                sleep(1)
            else:
                trio.run(self.parent)

    def play_intro(self):
        # play the intro head and wait to finish

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
        # All other IO is ok as a single Trio thread inside self.client
        tasks = [self.snd_listen, self.client_stream, self.parent_go]

        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            futures = {executor.submit(task): task for task in tasks}

if __name__ == '__main__':
    cl = Client()
    cl.main()
