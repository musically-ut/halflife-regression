#!/usr/bin/env python
import glob
import re
import os

import click
import pandas as pd
import numpy as np

from sklearn.metrics import roc_auc_score
from scipy.stats import spearmanr


ARGS_REGEX = {
    'hlwt': (re.compile(r'hlwt-([0-9.e-]*)\.'), float),
    'l2wt': (re.compile(r'l2wt-([0-9.e-]*)\.'), float),
    'epochs': (re.compile(r'epochs-([0-9]*)'), int),
    'method': (re.compile(r'method-([^.]*)'), str),
    'shuffle': (re.compile(r'shuffle-([0-9]*)'), int),
    'training_fraction': (re.compile(r'training_fraction-([0-9.e-]*)\.'), float),
}


def parse_args(file_name):
    """Extract dictionary of arguments from a given file_name."""
    args = {}
    for arg_name, (arg_regex, arg_type) in ARGS_REGEX.items():
        match_obj = arg_regex.search(file_name)
        if match_obj:
            args[arg_name] = arg_type(match_obj[1])
        else:
            args[arg_name] = None
    return args


@click.command()
@click.argument('results_dir', type=click.Path())
@click.argument('output_csv', type=click.Path())
def run(results_dir, output_csv):
    """Read all *.detailed files from RESULTS_DIR, calculate the metrics, and
    save output to OUTPUT_CSV."""
    op_files = glob.glob(os.path.join(results_dir, '*.detailed'))

    data = []

    for op_file in op_files:
        preds = pd.read_csv(op_file, sep='\t')
        args = parse_args(op_file)

        args['MAE'] = np.mean(np.abs(preds['p'] - preds['pp']))
        args['AUC'] = roc_auc_score(preds['p'], preds['pp'])
        args['COR_p'] = spearmanr(preds['p'], preds['pp'])[0]
        args['COR_h'] = spearmanr(preds['h'], preds['hh'])[0]

        data.append(args)

    pd.DataFrame(data).to_csv(output_csv, index=False)


if __name__ == '__main__':
    run()
