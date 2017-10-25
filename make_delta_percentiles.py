#!/usr/bin/env python
import argparse
import os
import pandas
import numpy as np

argparser = argparse.ArgumentParser(description='Create files containing different bin boundaries for provided quantiles.')
argparser.add_argument('input_file', help='Input CSV file.')
argparser.add_argument('output_dir', help='Where the files containing the bins will be created.')
argparser.add_argument('-q', help='Comma separated number of quantiles to create.', default='4')

args = argparser.parse_args()

print('Reading {} ...'.format(args.input_file))
df = pandas.read_csv(args.input_file)
delta = df.delta / (60 * 60 * 24)
last_time = delta.max()
quantiles = [int(x) for x in args.q.split(',')]

for num_q in quantiles:
    vals = np.percentile(delta, np.arange(0, 100, 100 / num_q))
    output_file_name = os.path.join(args.output_dir, '{}_bins'.format(num_q))
    with open(output_file_name, 'w') as f:
        f.write('\n'.join([str(x) for x in vals] + [str(last_time)]))
        print('Wrote {}.'.format(output_file_name))
