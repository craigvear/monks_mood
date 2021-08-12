# monks_mood
AI robot performance of Monks Mood

engine.py sits alone on the host laptop and chugs along feeding and outputting data using the onboard hive of RNN's. It needs to be started via its own terminal window.

main.py starts the whole shebang (except engine.py) It needs to be started by its own termimanl window. 

client.py coordinates dataflows and responses. it feeds live audio data to engine.py, and recieves its response. It then flings this to 3 child classes each of which contril the instrument sounds and send movement data to a dedicated physical robot

instrument.py is an instantiated class that is given an id/ instrument. It recieves and performs sound, from which it controls a dedicated robot

bot_robot.py sits in a robot and recieves movement data from instrument.py over a socket




