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
from robots import Robot
import trio
import concurrent.futures
import socket
from engine_client import Client
from time import sleep, time
from subprocess import Popen, PIPE

class Master:
    def __init__(self):
        # get own ip address
        self.ip = socket.gethostbyname(socket.gethostname())
        self.HOST = self.ip  # Client IP (this)
        self.PORT = 5000
        self.running = False
        Popen('python3 engine_server.py', shell=True)

    def engine_stream(self):
        # initiate engine client-server comms
        self.engine = Client()
        self.engine.main()

    def improv(self, bot):
        # grab raw data from engine stream
        raw_data_from_dict = self.engine.got_dict['master_output']

        # hand it to which ever bot is calling for it
        bot.make_sound(raw_data_from_dict)

    def robots(self):
        # make instrument bots here
        # instantiate the robots
        self.bass_bot = Robot('bass', '192.168.1.124', 4005)
        self.sax_bot = Robot('sax', '192.168.1.123', 4006)
        self.tromb_bot = Robot('tromb', '192.168.1.125', 4007)

        trio.run(self.parent)

    async def parent(self):
        while True:
            print("parent: started!")
            async with trio.open_nursery() as nursery:
                # spawning sax soundbot
                print("parent: spawning sax bot ...")
                nursery.start_soon(self.bot_stuff, self.sax_bot)

                # spawning bass soundbot
                print("parent: spawning bass bot ...")
                nursery.start_soon(self.bot_stuff, self.bass_bot)

                # spawning tromb soundbot
                print("parent: spawning tromb bot ...")
                nursery.start_soon(self.bot_stuff, self.tromb_bot)


    async def bot_stuff(self, bot):
        # while True:
        #     print(f'waiting {bot}')
        #     await trio.sleep(1)

    # async def bot_stuffB(self, bot):
    #     while True:
    #         print(f'waiting {bot}')
    #         sleep(1)
    #
    # async def bot_stuffC(self, bot):
    #     while True:
    #         print(f'waiting {bot}')
    #         sleep(1)

        # wait for intro to finish
        print(f'1. running bot stuff for {bot.name}')
        while True:
            if not self.improv:
                await trio.sleep(0.1)

        # then start improvisers
            else:
                print(f'2. improvising bot stuff for {bot.name}')
                self.improv(bot)

    # play the intro head and wait to finish
    def play_intro(self):
        # get sax's part
        alfie = AudioSegment.from_wav('../assets/alfie_intro.wav')

        # pan sax
        alfieLeft = alfie.pan(-0.5)

        # get bass part
        bass = AudioSegment.from_wav('../assets/bass_intro.wav')

        # mix them all together
        mixed_intro = bass.overlay(alfieLeft)

        # play and wait for it to finish
        #play(mixed_intro)

        print('temporary sleep process for 10 seconds')
        sleep(10)


    def main(self):
        # Thread the conductor, engine stream and each of the robot objects
        tasks = [self.conducter,
                 self.engine_stream,
                 self.robots]

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(task): task for task in tasks}

    # this func organises the overall composition of the performance
    def conducter(self):
        # wait for engine stream to work
        while not self.running:
            sleep(1)
            if self.engine.connected:
                self.running = True

        # start the whole performance with the intro
        self.play_intro()

        # then opens the conditions for improv,
        now = time()
        while time() < now + 180: # = 3 min improv
            self.improv_go = True

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
