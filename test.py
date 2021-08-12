# CLIENT SIDE


import socket


def Main():
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


if __name__ == '__main__':
    Main()



# import socket
# from random import random
# from time import sleep
#
# HOST = "192.168.1.123"
# PORT = 8888
#
# while True:
#     print(f"client: connecting to {HOST}:{PORT}")
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind((HOST, PORT))
#         s.listen()
#         client_stream, addr = s.accept()
#         with client_stream:
#             print('Connected by', addr)
#             connected = True
#             while connected:
#
#                 # send out-going data to server
#                 while True:
#                     rnd = random()
#                     raw = rnd * 100
#                     data = int.to_bytes(raw, 'big')
#
#                     client_stream.sendall(data)
#                     sleep(1)





# import socket
# host = socket.gethostname()
# ip = socket.gethostbyname(host)
#
# print(ip)
#




# from glob import glob
#
# audio_dir = glob(f'assets/sax/*.wav')
# audio_dir_len = len(audio_dir)
#
# print(audio_dir_len)
#
#
# for n in range(1000):
#
#     data = n / 1000
#     # new_value = ( (old_value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min
#
#     scaled_data = ((data - 0) / (1 - 0)) * (10 - -10) + -10
#
#     print (data, scaled_data)




