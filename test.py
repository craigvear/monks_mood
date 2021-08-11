from glob import glob

audio_dir = glob(f'assets/sax/*.wav')
audio_dir_len = len(audio_dir)

print(audio_dir_len)


for n in range(1000):

    nn = n / 1000
    # new_value = ( (old_value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min

    new_value = int( ( (nn - 0) / (1 - 0) ) * (audio_dir_len - 0) + 0)

    print (nn, new_value)




