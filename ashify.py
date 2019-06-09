#!/usr/bin/env python3

import argparse
import random


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('outfile')
    parser.add_argument('-n', type=int, default=1000000)
    parser.add_argument('--bound', type=float, default=100)
    parser.add_argument('--max-radius', type=float, default=0.1)
    parser.add_argument('--min-radius', type=float, default=0.01)
    return parser.parse_args()


def random_angle():
    return random.uniform(0, 360)


ASH_TEMPLATE = """
AttributeBegin
  Translate {}
  Rotate {} 1 0 0
  Rotate {} 0 1 0
  Rotate {} 0 0 1
  Shape "disk" "float radius" {}
AttributeEnd
"""


def main(outfile, n, bound, min_radius, max_radius):
    with open(outfile, 'w') as f:
        for _ in range(n):
            s = [random.uniform(-bound, bound) for _ in range(3)]
            if sum(x ** 2 for x in s) ** 0.5 < 5:
                continue
            f.write(ASH_TEMPLATE.format(
                '{} {} {}'.format(*s),
                random_angle(), random_angle(), random_angle(),
                random.uniform(min_radius, max_radius)))
            f.write('\n')
    print('Wrote {} particles'.format(n))


if __name__ == '__main__':
    main(**vars(get_args()))
