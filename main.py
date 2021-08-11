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
1) the client comms with engine
2) instantiating 3 robot performers
3) parsing and organising data to each performer
4) the opverall organisation of intro, improv, outro"""

from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play
from pydub.playback import play
from robot import Robot
from client import Client

def go():
    # instantiate all performer class's
    sax_bot = Robot(instrument='sax', port=12345, addr='127.0.0.1')
    tromb_bot = Robot(instrument='trombone', port=23456, addr='127.0.0.1')
    bass_bot = Robot(instrument='bass', port=34567, addr='127.0.0.1')

    # instantiate client
    client_bot = Client()

    # set client - server going
    client_bot.main()

    # finally start the performance
    play_intro()

def play_intro():
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

    improv()

def improv():
    pass



if __name__ == '__main__':
    go()