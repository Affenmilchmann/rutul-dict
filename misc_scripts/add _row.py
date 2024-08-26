from pprint import pprint
import csv
from random import randint

infile = 'rutul_dict.tsv'
outfile = 'rutul_dict_.tsv'

targs = ['PV-slam', 'below UNDER-stay']

with open(infile, 'r', encoding='utf-8') as f_in:
    reader = csv.reader(f_in, delimiter="\t", quotechar='"')
    with open(outfile, 'w', encoding='utf-8') as f_out:
        writer = csv.writer(f_out, delimiter="\t", quotechar='"')
        cols = next(reader)
        writer.writerow(cols)
        com_id = list(cols).index('comment_to_appear')
        lab_id = list(cols).index('Glossing label')
        for row in reader:
            row_ = list(row)
            if not row_[com_id]:
                row_[com_id] = ' — '
            writer.writerow(row_)

            """ if row_[lab_id] in targs:
                pairs = zip(cols, row_)
                pairs = filter(lambda x: x[1], pairs)
                pprint(list(pairs)) """
