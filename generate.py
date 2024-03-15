from jinja2 import (Environment, 
                    FileSystemLoader, 
                    Template)
from pathlib import Path
from tqdm import tqdm
import csv
import re
from pprint import pprint

def generate_html(data: dict, 
                  template: Template, 
                  out_file: Path,
                  **kwargs) -> None:
    """generates a single html file and saves it at `out_file`

    Args:
        data (dict): data to give to the template
        template (Template): jinja2 template
        out_file (Path): out file name
    """
    with open(out_file, 'w') as f:
        f.write(template.render(data=data,
                                **kwargs))

def merge_meanings(data: dict) -> None:
    data['meanings'] = []
    for i in range(1, 5):
        data['meanings'].append({
            'meaning': data[f'meaning_{i}'],
            'meaning_rus': data[f'meaning_{i}_rus'],
            'example': data[f'example_{i}'],
            'example_rus': data[f'example_{i}_rus'],
            'diathesis': data[f'diathesis_{i}']
        })
        del data[f'meaning_{i}'], data[f'meaning_{i}_rus'], \
            data[f'example_{i}'], data[f'example_{i}_rus'], data[f'diathesis_{i}']

def split_examples(data: dict) -> None:
    for meaning in data['meanings']:
        examples = meaning['example'].split(' ; ')
        examples = [x.strip() for x in examples]
        examples_rus = meaning['example_rus'].split(' ; ')
        examples_rus = [x.strip() for x in examples_rus]
        del meaning['example'], meaning['example_rus']
        meaning['examples'] = [{'original': orig, 'rus': rus}
                               for orig, rus in zip(examples, examples_rus)]
        
def load_inflection(*files) -> dict:
    inflection_data = {}
    for f_name in files:
        with open(f_name, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            col_names = next(reader)
            for row in reader:
                data = {k:v for k, v in zip(col_names, row)}
                lex_id = data['lexeme_id']
                del data['lexeme_id']
                inflection_data[lex_id] = data
    return inflection_data

def insert_inflection(data: dict, inflection_data: dict) -> None:
    if data['lexeme_id'] in inflection_data:
        data['inflection_data'] = inflection_data[data['lexeme_id']]
    else: 
        data['inflection_data'] = None

glossing_labels = set()
def check_glossing_label(label: str) -> None:
    if not re.match(r'^[a-z]+(?:, )?[a-z]*$', label):
        raise Exception(f"Invalid format of glossing label: '{label}'")
    if label in glossing_labels:
        raise Exception(f"Not unique glossing label: '{label}'. There is already an entry with such label")
    glossing_labels.add(label)

def main():
    template_file = 'word.html'
    data_file = 'data/rutul_dict.tsv'
    infl_files = ['data/infl_adj.tsv',
                  'data/infl_noun.tsv',
                  'data/infl_verb.tsv']
    out_dir = 'words'
    complex_pos = {
        f'complex {pos}': f'This is a complex {pos} consisting of the words:'
        for pos in ['verb', 'noun']
    }

    root = Path(__file__).parent.absolute()
    templates_dir = root.joinpath('templates')
    out_dir = root.joinpath(out_dir)
    if not out_dir.is_dir(): out_dir.mkdir()
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template(template_file)

    inflection_data = load_inflection(*infl_files)

    with open(data_file) as f:
        reader = csv.reader(f, delimiter='\t')
        col_names = next(reader)
        for row in tqdm(reader):
            data = {k:v for k, v in zip(col_names, row)}
            merge_meanings(data)
            split_examples(data)
            insert_inflection(data, inflection_data)
            pprint(data)
            check_glossing_label(data['Glossing label'])

            out_file = out_dir.joinpath("{name}.html".format(
                name=data['Glossing label'].replace(', ', '-')
            ))
            generate_html(
                data=data,
                template=template,
                out_file=out_file,
                complex_pos=complex_pos
            )

if __name__ == '__main__':
    main()