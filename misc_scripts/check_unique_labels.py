from pathlib import Path
import csv

root = Path(__file__).parent.parent
data_dir = root.joinpath('data')
dict_file = data_dir.joinpath('rutul_dict.tsv')

def check_unique_labels():
    labels = dict()
    dublicates = []
    with open(dict_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        cols = next(reader)
        for row in reader:
            data = dict(zip(cols, row))
            if data['Glossing label'] in labels:
                dublicates.append({
                    data['Glossing label']: [labels['Glossing label'], 
                                             data['lexeme_id']]
                })
            else:
                labels['Glossing label'] = data['lexeme_id']
    return dublicates
