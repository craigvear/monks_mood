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
for n in range(1000):

    data = n / 1000
    # new_value = ( (old_value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min

    scaled_data = ((data - 0) / (1 - 0)) * (10 - -10) + -10

    print (data, scaled_data)




