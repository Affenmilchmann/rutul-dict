from pathlib import Path
import csv

root = Path(__file__).parent.parent
data_dir = root.joinpath('data')
dict_file = data_dir.joinpath('rutul_dict.tsv')

def check_meanings():
    def filter_keys(d: dict, keys: list) -> dict:
        return {k: v  for k, v in d.items() if k in keys}
    bad_rows = []
    with open(dict_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        cols = next(reader)
        for row in reader:
            data = dict(zip(cols, row))
            for i in range(1, 5):
                if bool(data[f'meaning_{i}']) != bool(data[f'meaning_{i}_rus']):
                    bad_rows.append(filter_keys(data, [f'meaning_{i}',
                                                       f'meaning_{i}_rus',
                                                       'lexeme_id']))
    return bad_rows
                    
if __name__ == '__main__':
    check_meanings()