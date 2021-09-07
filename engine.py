"""main server script
will sit onboard host and operate as Nebula --- its dynamic soul"""

# --------------------------------------------------
#
# Embodied AI Engine Prototype v0.10
# 2021/01/25
#
# © Craig Vear 2020
# cvear@dmu.ac.uk
#
# Dedicated to Fabrizio Poltronieri
#
# --------------------------------------------------

from random import randrange
from time import time
from tensorflow.keras.models import load_model

import pyaudio
import numpy as np
import concurrent.futures
from random import random
from time import sleep
from pydub import AudioSegment
from pydub.playback import play


# --------------------------------------------------
#
# instantiate an object for each neural net
#
# --------------------------------------------------


# v4 models were trained with 1st batch of Blue Haze datasets

class MoveRNN:
    def __init__(self):
        print('MoveRNN initialization')
        self.move_rnn = load_model('models/EMR-v4_RNN_skeleton_data.nose.x.h5')

    def predict(self, in_val):
        # predictions and input with localval
        self.pred = self.move_rnn.predict(in_val)
        return self.pred

class AffectRNN:
    def __init__(self):
        print('AffectRNN initialization')
        self.affect_rnn = load_model('models/EMR-v4_RNN_bitalino.h5')

    def predict(self, in_val):
        # predictions and input with localval
        self.pred = self.affect_rnn.predict(in_val)
        return self.pred

class MoveAffectCONV2:
    def __init__(self):
        print('MoveAffectCONV2 initialization')
        self.move_affect_conv2 = load_model('models/EMR-v4_conv2D_move-affect.h5')

    def predict(self, in_val):
        # predictions and input with localval
        self.pred = self.move_affect_conv2.predict(in_val)
        return self.pred

class AffectMoveCONV2:
    def __init__(self):
        print('AffectMoveCONV2 initialization')
        self.affect_move_conv2 = load_model('models/EMR-v4_conv2D_affect-move.h5')

    def predict(self, in_val):
        # predictions and input with localval
        self.pred = self.affect_move_conv2.predict(in_val)
        return self.pred

# --------------------------------------------------
#
# controls all thought-trains and affect responses
#
# --------------------------------------------------

class AiDataEngine():
    def __init__(self, speed=1):
        print('building engine server')
        self.interrupt_bang = False
        # self.running = False
        # self.PORT = 8000
        # self.IP_ADDR = "127.0.0.1"
        self.global_speed = speed
        self.rnd_stream = 0

        # make a default dict for the engine
        self.datadict = {'move_rnn': 0,
                         'affect_rnn': 0,
                         'move_affect_conv2': 0,
                         'affect_move_conv2': 0,
                         'master_output': 0,
                         'user_in': 0,
                         'rnd_poetry': 0,
                         'rhythm_rnn': 0,
                         'affect_net': 0,
                         'self_awareness': 0,
                         'affect_decision': 0,
                         'rhythm_rate': 0.1}

        # name list for nets
        self.netnames = ['move_rnn',
                         'affect_rnn',
                         'move_affect_conv2',
                         'affect_move_conv2',
                         'self_awareness',  # Net name for self-awareness
                         'master_output']  # input for self-awareness

        # names for affect listening
        self.affectnames = ['user_in',
                            'rnd_poetry',
                            'affect_net',
                            'self_awareness']

        self.rhythm_rate = 0.1
        self.affect_listen = 0

        # fill with random values
        self.dict_fill()
        print(self.datadict)

        # instantiate nets as objects and make  models
        self.move_net = MoveRNN()
        self.affect_net = AffectRNN()
        self.move_affect_net = MoveAffectCONV2()
        self.affect_move_net = AffectMoveCONV2()
        self.affect_perception = MoveAffectCONV2()

        # logging on/off switches
        self.net_logging = False
        self.master_logging = False
        self.streaming_logging = False
        self.affect_logging = False

    # --------------------------------------------------
    #
    # prediction and rnd num gen zone
    #
    # --------------------------------------------------

    # makes a prediction for a given net and defined input var
    def make_data(self):
        while True:

            # calc rhythmic intensity based on self-awareness factor & global speed
            intensity = self.datadict.get('self_awareness')
            self.rhythm_rate = (self.rhythm_rate * intensity) * self.global_speed
            self.datadict['rhythm_rate'] = self.rhythm_rate

            # get input vars from dict (NB not always self)
            in_val1 = self.get_in_val(0) # move RNN as input
            in_val2 = self.get_in_val(1) # affect RNN as input
            in_val3 = self.get_in_val(2) # move - affect as input
            in_val4 = self.get_in_val(1) # affect RNN as input

            # send in vals to net object for prediction
            pred1 = self.move_net.predict(in_val1)
            pred2 = self.affect_net.predict(in_val2)
            pred3 = self.move_affect_net.predict(in_val3)
            pred4 = self.affect_move_net.predict(in_val4)

            # special case for self awareness stream
            self_aware_input = self.get_in_val(5) # main movement as input
            self_aware_pred = self.affect_perception.predict(self_aware_input)

            if self.net_logging:
                print(f"  'move_rnn' in: {in_val1} predicted {pred1}")
                print(f"  'affect_rnn' in: {in_val2} predicted {pred2}")
                print(f"  move_affect_conv2' in: {in_val3} predicted {pred3}")
                print(f"  'affect_move_conv2' in: {in_val4} predicted {pred4}")
                print(f"  'self_awareness' in: {self_aware_input} predicted {self_aware_pred}")

            # put predictions back into the dicts and master
            self.put_pred(0, pred1)
            self.put_pred(1, pred2)
            self.put_pred(2, pred3)
            self.put_pred(3, pred4)
            self.put_pred(4, self_aware_pred)

            # outputs a stream of random poetry
            rnd_poetry = random()
            self.datadict['rnd_poetry'] = random()
            if self.streaming_logging:
                print(f'random poetry = {rnd_poetry}')

            sleep(self.rhythm_rate)

    # function to get input value for net prediction from dictionary
    def get_in_val(self, which_dict):
        # get the current value and reshape ready for input for prediction
        input_val = self.datadict.get(self.netnames[which_dict])
        input_val = np.reshape(input_val, (1, 1, 1))
        return input_val

    # function to put prediction value from net into dictionary
    def put_pred(self, which_dict, pred):
        # randomly chooses one of te 4 predicted outputs
        out_pred_val = pred[0][randrange(4)]
        if self.master_logging:
            print(f"out pred val == {out_pred_val},   master move output == {self.datadict['master_output']}")
        # save to data dict and master move out ONLY 1st data
        self.datadict[self.netnames[which_dict]] = out_pred_val
        self.datadict['master_output'] = out_pred_val

    # fills the dictionary with rnd values for each key of data dictionary
    def dict_fill(self):
        for key in self.datadict.keys():
            rnd = random()
            self.datadict[key] = rnd

    # --------------------------------------------------
    #
    # affect and streaming methods
    #
    # --------------------------------------------------

    # define which feed to listen to, and duration
    # and a course of affect response
    def affect(self):
        # daddy cycle = is the master running on?
        while True:
            if self.affect_logging:
                print('\t\t\t\t\t\t\t\t=========HIYA - DADDY cycle===========')

            # flag for breaking on big affect signal
            self.interrupt_bang = True

            # calc master cycle before a change
            master_cycle = randrange(6, 26) * self.global_speed
            loop_dur = time() + master_cycle
            if self.affect_logging:
                print(f"                 interrupt_listener: started! sleeping now for {loop_dur}...")

            # refill the dicts?????
            self.dict_fill()

            # child cycle - waiting for interrupt  from master clock
            while time() < loop_dur:
                if self.affect_logging:
                        print('\t\t\t\t\t\t\t\t=========Hello - child cycle 1 ===========')

                # if a major break out then go to Daddy cycle
                if not self.interrupt_bang:
                    break

                # randomly pick an input stream for this cycle
                rnd = randrange(4)
                self.rnd_stream = self.affectnames[rnd]
                self.datadict['affect_decision'] = rnd
                print(self.rnd_stream)
                if self.affect_logging:
                    print(self.rnd_stream)

                # hold this stream for 1-4 secs, unless interrupt bang
                end_time = time() + (randrange(1000, 4000) / 1000)
                if self.affect_logging:
                    print('end time = ', end_time)

                # baby cycle 2 - own time loops
                while time() < end_time:
                    if self.affect_logging:
                        print('\t\t\t\t\t\t\t\t=========Hello - baby cycle 2 ===========')

                    # go get the current value from dict
                    affect_listen = self.datadict[self.rnd_stream]
                    if self.affect_logging:
                        print('current value =', affect_listen)

                    # make the master output the current value of the stream
                    self.datadict['master_output'] = affect_listen
                    if self.master_logging:
                        print(f'\t\t ==============  master move output = {affect_listen}')

                    # calc affect on behaviour
                    # if input stream is LOUD then smash a random fill and break out to Daddy cycle...
                    if affect_listen > 0.50:
                        if self.affect_logging:
                            print('interrupt > HIGH !!!!!!!!!')

                        # A - refill dict with random
                        self.dict_fill()

                        # B - jumps out of this loop into daddy
                        self.interrupt_bang = False
                        if self.affect_logging:
                            print('interrupt bang = ', self.interrupt_bang)

                        # C break out of this loop, and next (cos of flag)
                        break

                    # if middle loud fill dict with random, all processes norm
                    elif 0.20 < affect_listen < 0.49:
                        if self.affect_logging:
                            print('interrupt MIDDLE -----------')
                            print('interrupt bang = ', self.interrupt_bang)

                        # refill dict with random
                        self.dict_fill()

                    elif affect_listen <= 0.20:
                        if self.affect_logging:
                            print('interrupt LOW_______________')
                            print('interrupt bang = ', self.interrupt_bang)

                    # and wait for a cycle
                    sleep(self.rhythm_rate)

    def parse_got_dict(self, got_dict):
        self.datadict['user_in'] = got_dict['mic_level']

        # user change the overall speed of the engine
        self.global_speed = got_dict['speed']

        # user change tempo of outputs and parsing
        self.rhythm_rate = got_dict['tempo']

    # # stop start methods
    # def go(self):
    #     # self.running = True
    #     trio.run(self.flywheel)
    #     print('I got here daddy')

    def quit(self):
        self.running = False




"""main client script
controls microphone stream and organise all audio responses"""



class Client:
    def __init__(self, library):
        self.running = True
        self.connected = False
        self.logging = False

        # is the robot connected
        self.robot_connected = True
        self.direction = 1

        if self.robot_connected:
            # import robot scripts
            from arm.arm import Arm
            from robot.rerobot import Robot

            # instantiate robot comms
            self.robot_robot = Robot()
            self.arm_arm = Arm()
            # self.robot_robot.reset_arm()

            # prepare for movement
            # LED's ready fpr drawing
            self.arm_arm.led_blue()

            # get arm into draw mode
            self.arm_arm.draw_mode_status = True
            self.arm_arm.first_draw_move = True
            self.arm_arm.pen_drawing_status = False

            # goto position
            self.arm_arm.wait_ready()

            # move gripper arm up
            for n in range(12):
                self.robot_robot.gripper_up()

        if library == 'jazz':
            self.audio_file_sax = AudioSegment.from_mp3('assets/alfie.mp3')
            self.audio_file_bass = AudioSegment.from_mp3('assets/bass.mp3') + 4

        elif library == 'pop':
            self.audio_file_sax = AudioSegment.from_wav('assets/vocals.wav')
            self.audio_file_bass = AudioSegment.from_wav('assets/accompaniment.wav')

        # robot instrument vars
        # globs for sax
        self.pan_law_sax = -0.5
        self.audio_file_len_ms_sax = self.audio_file_sax.duration_seconds * 1000

        # globs for bass
        self.pan_law_bass = 0
        self.audio_file_len_ms_bass = self.audio_file_bass.duration_seconds * 1000

        # self.HOST = '127.0.0.1'  # Client IP (this)
        # self.PORT = 8000
        # Port to listen on (non-privileged ports are > 1023)

        self.CHUNK = 2 ** 11
        self.RATE = 44100
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)

        # build send data dict
        self.send_data_dict = {'mic_level': 0,
                               'speed': 1,
                               'tempo': 0.1
                               }


        # init got dict
        self.got_dict = {}

        # instantiate the server
        self.engine = AiDataEngine()

        # # set the ball rolling
        # self.main()

    def snd_listen(self):
        print("mic listener: started!")
        while True:
            data = np.frombuffer(self.stream.read(self.CHUNK,exception_on_overflow = False),
                                 dtype=np.int16)
            peak = np.average(np.abs(data)) * 2
            if peak > 2000:
                bars = "#" * int(50 * peak / 2 ** 16)
                print("%05d %s" % (peak, bars))
            self.send_data_dict['mic_level'] = peak / 30000

    def terminate(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def data_exchange(self):
        print("data exchange: started!")
        while True:
            # send self.send_data_dict
            self.engine.parse_got_dict(self.send_data_dict)

            # get self.datadict from engine
            self.got_dict = self.engine.datadict

            # sync with engine & stop freewheeling
            sleep_dur = self.got_dict['rhythm_rate']
            # print('data exchange')
            sleep(sleep_dur)

    def engine(self):
        # set the engine off
        self.engine.go()

    def main(self):
        # snd_listen and client need dependent threads.
        # All other IO is ok as a single Trio thread inside self.client
        tasks = [self.engine.make_data,
                 self.engine.affect,
                 self.snd_listen,
                 self.data_exchange,
                 self.robot_sax,
                 self.robot_bass]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(task): task for task in tasks}

    def robot_sax(self):
        # make a serial port connection here
        print('im here SAX - sleeping for 3')
        sleep(3)
        # loop here
        # while self.running:
        #     print('im here2')

        # while not self.improv_go:
        #     print('im here3')
        #     sleep(1)
        #     print('sleeping robot')

    # then start improvisers
        while True:
            print('im here4')
            # grab raw data from engine stream
            raw_data_from_dict = self.got_dict['master_output']
            rhythm_rate = self.got_dict['rhythm_rate']
            print('sax', raw_data_from_dict, rhythm_rate)

            # add variability to the individual instrument
            rnd_dur_delta = random()
            rhythm_rate *= rnd_dur_delta * 8
            print('sax', raw_data_from_dict, rhythm_rate)

            # make a sound & move bot
            self.make_sound('sax', raw_data_from_dict, rhythm_rate)
            print('making a new one')

    def robot_bass(self):
        # make a serial port connection here
        print('im here Bass - sleeping for 3')
        sleep(3)
        # loop here
        # while self.running:
        #     print('im here2')

        # while not self.improv_go:
        #     print('im here3')
        #     sleep(1)
        #     print('sleeping robot')

    # then start improvisers
        while True:
            print('im here4')
            # grab raw data from engine stream
            raw_data_from_dict = self.got_dict['master_output']

            # trying different part of the dict
            raw_data_from_dict = self.got_dict['move_rnn']

            rhythm_rate = self.got_dict['rhythm_rate']
            print('bass', raw_data_from_dict, rhythm_rate)

            # add variability to the individual instrument
            rnd_dur_delta = random() * 4
            rhythm_rate *= rnd_dur_delta
            print('bass', raw_data_from_dict, rhythm_rate)

            # make a sound & move bot
            self.make_sound('bass', raw_data_from_dict, rhythm_rate)
            print('making a new one')

    def make_sound(self, instrument, incoming_raw_data, rhythm_rate):
        # # temp random num gen
        # rnd = randrange(self.audio_dir_len)
        # print(self.audio_dir[rnd])
        print('making sound')

        if instrument == 'sax':
            audio_file = self.audio_file_sax
            audio_file_len_ms = self.audio_file_len_ms_sax
            pan_law = self.pan_law_sax
            len_delta = random() * 1000

        elif instrument == 'bass':
            audio_file = self.audio_file_bass
            audio_file_len_ms = self.audio_file_len_ms_bass
            pan_law = self.pan_law_bass
            len_delta = random() * 1000

        # rescale incoming raw data
        audio_play_position = int(((incoming_raw_data - 0) / (1 - 0)) * (audio_file_len_ms - 0) + 0)
        duration = rhythm_rate * len_delta
        if duration < 0.1:
            duration = 0.1
        end_point = audio_play_position + duration
        print(audio_play_position, end_point, duration)

        # make a sound from incoming data
        snippet = audio_file[audio_play_position: end_point]
        print('snippet')

        # pan snippet
        pan_snippet = snippet.pan(pan_law)
        print('pan')

        # move bot before making sound
        if self.robot_connected:
            if instrument == 'sax':
                self.move_robot(incoming_raw_data, duration)

        # get the robot to move with
        play(pan_snippet)
        print('play')

        # sleep(duration/ 1000)
        print('fininshed a play')

    def move_robot(self, incoming_data, duration):
        # top previous movements
        # self.robot_robot.gripper_stop()
        # self.robot_robot.paddle_stop()
        # self.robot_robot.stop()

        # which movement
        if duration > 0.5:

            # select a joint (1-16 % 4)
            # or move bot left or right (17)
            # or move gripper up or down (18)
            rnd_joint = randrange(19)

            rnd_direction = randrange(2)
            if rnd_direction == 1:
                direction = -20
            else:
                direction = 20

            rnd_speed = randrange(10)
            rnd_speed *= 10

            # move an arm joint
            if rnd_joint <= 15:
                joint = (rnd_joint % 4) + 1
                self.arm_arm.move_joint_relative_speed(joint, direction, rnd_speed)

            # move the gripper
            elif rnd_joint == 16:
                if rnd_direction == 1:
                    self.robot_robot.gripper_up()
                else:
                    self.robot_robot.gripper_down()

            # or move the wheels
            elif rnd_joint == 17:
                if rnd_direction == 1:
                    self.robot_robot.step_forward()
                else:
                    self.robot_robot.step_backward()

            # or move the wheels
            elif rnd_joint == 18:
                if rnd_direction == 1:
                    self.robot_robot.paddle_open()
                else:
                    self.robot_robot.paddle_close()


if __name__ == '__main__':
    library = 'jazz'
    # library = 'pop'
    cl = Client(library)

    # set the ball rolling
    cl.main()

