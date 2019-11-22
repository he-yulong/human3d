import os
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--image_dir', default='./data/2019-11-22-10-48-39/', help='image directory.')
args = parser.parse_args()

idx = 1
path = args.image_dir + 'color-' + str(idx) + '.jpg'
keypoints_file = args.image_dir + 'annot.txt'
print(keypoints_file)

pos = []
confidence = []
for line in open(keypoints_file, 'r'):
    li = line.replace('|', '').replace(',', '').replace('>>>', '').replace('<<<', '').strip().split(' ')

    if len(li) == 256:
        for i in range(256):
            li[i] = float(li[i])
        pos.append(li[:32*3])
        confidence.append(li[32*3+32*4:])
    else:
        print('Not use it.')

print(pos[0])
print(pos[-1])
print(len(pos[-1]))
print('-' * 20)
print(confidence[0])
print(confidence[-1])
print(len(confidence[-1]))

pos_data = np.array(pos).reshape((-1, 32, 3))
confidence_data = np.array(confidence).reshape((-1, 32, 1))
data = np.concatenate((pos_data, confidence_data), axis=2)
print(data)
print(data.shape)
np.save(args.image_dir + 'parsed_data', data)
