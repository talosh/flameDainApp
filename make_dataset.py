#!/usr/bin/python

import os
import sys
import shutil
from pprint import pprint

if sys.argv < 1:
    print ('usage: make_dataset.py input.mov')
    sys.exit(1)

input_file = sys.argv[1]
if not os.path.isfile(input_file):
    print ('can not open %s' % os.path.abspath(input_file))

name, ext = os.path.splitext(os.path.basename(input_file))
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)

if os.path.isdir(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)
os.makedirs(os.path.join(output_dir, 'tmp'))
os.makedirs(os.path.join(output_dir, 'sequences'))

cmd = 'ffmpeg -i ' + os.path.abspath(input_file) + ' -qscale:v 0 ' + output_dir + os.path.sep + 'tmp' + os.path.sep + '%04d.png' 
os.system(cmd)
tmp_files = os.listdir(os.path.join(output_dir, 'tmp'))
pngs = []
for tmp_file in tmp_files:
    if tmp_file.endswith('.png'):
        pngs.append(tmp_file)

sequence = 1
triad = 1
trainlist = open(os.path.join(output_dir, 'tri_trainlist.txt'), 'a')

for x in range (0, len(pngs)):
    sequence_dir = '{0:05d}'.format(sequence)
    if not os.path.isdir(os.path.join(output_dir, 'sequences')):
        os.makedirs(os.path.join(output_dir, 'sequences', sequence_dir))
    triad_dir = '{0:04d}'.format(triad)
    if x > len(pngs) - 3:
        continue
    os.makedirs(os.path.join(output_dir, 'sequences', sequence_dir, triad_dir))
    src = os.path.join(output_dir, 'tmp', pngs[x])
    dst = os.path.join(output_dir, 'sequences', sequence_dir, triad_dir, 'im1.png')
    shutil.copyfile(src, dst)
    src = os.path.join(output_dir, 'tmp', pngs[x+1])
    dst = os.path.join(output_dir, 'sequences', sequence_dir, triad_dir, 'im2.png')
    shutil.copyfile(src, dst)
    src = os.path.join(output_dir, 'tmp', pngs[x+2])
    dst = os.path.join(output_dir, 'sequences', sequence_dir, triad_dir, 'im3.png')
    shutil.copyfile(src, dst)
    trainlist.write('%s/%s\n' % (sequence_dir, triad_dir))
    if x > 999:
        sequence += 1
        triad = 0
    triad += 1

trainlist.close()
shutil.copyfile(os.path.join(output_dir, 'tri_trainlist.txt'), os.path.join(output_dir, 'tri_testlist.txt'))
shutil.rmtree(os.path.join(output_dir, 'tmp'))