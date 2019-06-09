#!/usr/bin/env python3

import argparse
import os
import random
import numpy as np


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('objfile')
    parser.add_argument('rockdir')
    parser.add_argument('outfile')
    parser.add_argument('--max-scale', type=float, default=2.0)
    parser.add_argument('--min-scale', type=float, default=0.5)
    return parser.parse_args()


def random_angle():
    return random.uniform(0, 360)


def random_scale(x, y):
    return ' '.join([str(random.uniform(x, y))] * 3)


class QuadMesh(object):

    def __init__(self, file_path):
        self.file_path = file_path
        self.num_vertex = 0
        self.num_face = 0
        self.vertices = []
        self.faces = []

        self.load_obj(file_path)

    def load_obj(self, file_path):
        with open(file_path, 'r') as f:
            for line in f.read().split('\n'):
                if len(line) == 0:
                    continue
                if line[0] == 'f':
                    fgroup = line.split(' ')[1:]
                    x = [int(l.split('/')[0]) - 1 for l in fgroup]
                    if len(x) == 4:
                        self.faces.append(x)
                        self.num_face += 1
                elif line[:2] == 'v ':
                    self.vertices.append(
                        np.array([float(p) for p in line.split(' ')[1:]]))
                    self.num_vertex += 1

        print('num vertices', self.num_vertex)
        print('num faces', self.num_face)

    def sample(self):
        for face in self.faces:
            weights = np.random.uniform(0, 1, 4)
            weights /= np.sum(weights)
            vertex = np.zeros(3)
            for w, v in zip(weights, face):
                vertex += w * self.vertices[v]
            yield [round(x, 3) for x in vertex.tolist()]


ROCK_TEMPLATE = """
AttributeBegin
  Translate {}
  Scale {}
  Rotate {} 1 0 0
  Rotate {} 0 1 0
  Rotate {} 0 0 1
  Include "{}"
AttributeEnd
"""


def main(objfile, rockdir, outfile, min_scale, max_scale):
    rock_files = os.listdir(rockdir)

    mesh = QuadMesh(objfile)

    count = 0
    with open(outfile, 'w') as f:
        for s in mesh.sample():
            count += 1
            f.write(ROCK_TEMPLATE.format(
                '{} {} {}'.format(*s), random_scale(min_scale, max_scale),
                random_angle(), random_angle(), random_angle(),
                os.path.join(rockdir, random.choice(rock_files))))
            f.write('\n')
    print('Wrote {} rocks'.format(count))


if __name__ == '__main__':
    main(**vars(get_args()))
