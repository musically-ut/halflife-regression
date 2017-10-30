#!/usr/bin/env python
import argparse
import re
import csv
import os

argparser = argparse.ArgumentParser(description='Compile stdout into a csv format after grid search is complete.')
argparser.add_argument('std_output_dir', action='store', help='Folder where to read the stdout files from.')
argparser.add_argument('output_file', action='store', help='CSV file where the output should be written.')

if __name__ == '__main__':
    args = argparser.parse_args()

    csv_writer = None
    with open(args.output_file, 'w') as output_file:
        for stdout_file in os.listdir(args.std_output_dir):
            print('Processing {} ... '.format(stdout_file), end='')

            file_path = os.path.join(args.std_output_dir, stdout_file)
            if not os.path.isfile(file_path):
                print('Ignoring: Not a file')
            else:
                try:
                    with open(file_path, 'r') as open_file:
                        output_lines = open_file.readlines()
                        match_lines = [x for x in output_lines if x.startswith('test')]
                        if len(match_lines) < 1:
                            print('Ignoring due to no line match.')
                        elif len(match_lines) > 1:
                            print('Ignoring due to too many lines matching.')
                        else:
                            row = dict(re.findall(r'[(]?([^\s]*)=([^\s,\)]*)', match_lines[0]))

                            if csv_writer is None:
                                field_names = ['file'] + sorted(row.keys())
                                csv_writer = csv.DictWriter(output_file, field_names)
                                csv_writer.writeheader()

                            row['file'] = stdout_file
                            csv_writer.writerow(row)
                            print('Done.')
                except Exception as e:
                    print('Ignoring due to error: {}'.format(e))

    print('Finished.')
