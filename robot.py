"""recieves data from main,
makes a sound using a dedictaed instrument audio dir,
and controls a robot movement using serial"""

import trio
import pickle
import sys


class Robot:
    def __init__(self, instrument, port, addr):
        print(f'instantiated {instrument} bot, on port {port}')
        self.instrument = instrument
        self.PORT = port
        self.IP_ADDR = addr
        self.running = False

    async def make_sound(self, incoming_raw_data):
        pass

    async def move_bot(self, move_data):
        pass

    # async def flywheel(self):
    #     print(f'parent {self.instrument}: started!')
    #     while self.running:
    #         print(f'parent: connecting to {self.IP_ADDR}:{self.PORT}')
    #         client_stream = await trio.open_tcp_stream(self.IP_ADDR, self.PORT)
    #         async with client_stream:
    #             # self.interrupt_bang = True
    #             async with trio.open_nursery() as nursery:
    #                 # spawning socket listener
    #
    #
    #
    #                 print("parent: spawning making data ...")
    #                 nursery.start_soon(self.make_sound)
    #
    #                 # spawning affect listener and master clocks
    #                 print("parent: spawning affect listener and clocks ...")
    #                 nursery.start_soon(self.move_bot)
