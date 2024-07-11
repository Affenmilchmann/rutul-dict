from pprint import pprint
from pathlib import Path
import csv
import re
import os

from jinja2 import (Environment,
                    FileSystemLoader,
                    Template)
from tqdm import tqdm

def generate_html(data: dict,
                  template: Template,
                  out_file: Path,
                  **kwargs) -> None:
    """Generates a single html file and saves it at `out_file`

    Args:
        data (dict): data to give to the template
        template (Template): jinja2 template
        out_file (Path): out file name
    """
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(template.render(data=data,
                                **kwargs))

def merge_meanings(data: dict) -> None:
    """Merges meanings in a dict.

    {'meaning_1': 'a', 'meaning_2': 'b',
     'meaning_1_rus': 'c', 'meaning_1_rus': 'd',
     'example_1': 'e', 'example_1': 'f',
     'example_1_rus': 'g', 'example_2_rus': 'h'б
     'diathesis_1': 'i', 'diathesis_2': 'j'}
    
    will become

    {'meanings': [
        {'meaning': 'a', 'meaning_rus': 'c',
         'example': 'e', 'example_rus': 'g',
         'diathesis': 'i'},
        {'meaning': 'b', 'meaning_rus': 'd',
         'example': 'f', 'example_rus': 'h',
         'diathesis': 'j'}
    ]}

    Args:
        data (dict): dict that will be modified in-place
    """
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
    """Splits examples in a dict

    {'meanings': [{
        ...
        'example': "mašinbɨr ara jiˁlχɨra; q'ʷaˁd čabɨlešdɨ süri ara jiˁlχɨraj',
        'example_rus': 'Машины столкнулись; Две отары баранов смешались'
        ...
    }]}

    will become 

    {'meanings': [{
        ...
        'examples': [
            'examples': [
                {'original': 'mašinbɨr ara jiˁlχɨra',
                 'rus': 'Машины столкнулись'},
                {'original': "q'ʷaˁd čabɨlešdɨ süri ara jiˁlχɨraj",
                 'rus': 'Две отары баранов смешались'}]
        ...
    }]}

    Args:
        data (dict): dict that will be modified in-place
    """
    for meaning in data['meanings']:
        examples = meaning['example'].split(' ; ')
        examples = [x.strip() for x in examples]
        examples_rus = meaning['example_rus'].split(' ; ')
        examples_rus = [x.strip() for x in examples_rus]
        del meaning['example'], meaning['example_rus']
        meaning['examples'] = [{'original': orig, 'rus': rus}
                               for orig, rus in zip(examples, examples_rus)]

def load_inflection(*files) -> dict:
    """Loads inflection data

    Returns:
        dict: Inflection data dict. Keys - lexeme ids; values - data dict
    """
    inflection_data = {}
    for f_name in files:
        with open(f_name, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            col_names = next(reader)
            for row in reader:
                data = dict(zip(col_names, row))
                lex_id = data['lexeme_id']
                del data['lexeme_id']
                inflection_data[lex_id] = data
    return inflection_data

def load_glossing_labels(file: str) -> dict:
    """Loads key-value glossing labels dict

    Args:
        file (str): dict file

    Returns:
        dict: key - lexeme_id; value - glossing label
    """
    labels = {}
    with open(file, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        col_names = next(reader)
        for row in tqdm(reader):
            data = dict(zip(col_names, row))
            labels[data['lexeme_id']] = data['Glossing label']
    return labels

def insert_inflection(data: dict, inflection_data: dict) -> None:
    """Inserts corresponding inflection data and filters out 
    blacklisted keys.

    Args:
        data (dict): current word data. Will be modified in-place
        inflection_data (dict): all words inflection data
    """
    blacklist = ['Orthography',
                 'Glossing label',
                 'Lexical entry']
    if data['lexeme_id'] in inflection_data:
        data['inflection_data'] = inflection_data[data['lexeme_id']]
        for k in blacklist:
            del data['inflection_data'][k]
    else:
        data['inflection_data'] = None

page_names = set()
def check_page_name(label: str) -> None:
    """Checkpage name if it
    
    1) has the right format

    2) is unique

    Args:
        label (str): page name

    Raises:
        ValueError: format is incorrect
        ValueError: label is not unique (this func met it before)
    """
    chars = "[a-zA-Z0-9_\-'.]"
    if not re.match(f'^{chars}+(?:, )?{chars}*$', label):
        raise ValueError(f"Invalid format of page name: '{label}'")
    if label in page_names:
        raise ValueError(
            f"Not unique page name: '{label}'. There is already an entry with such name"
        )
    page_names.add(label)

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
    if not out_dir.is_dir():
        out_dir.mkdir()
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template(template_file)

    inflection_data = load_inflection(*infl_files)
    glossing_labels = load_glossing_labels(data_file)

    os.system(f'rm {out_dir}/*')

    with open(data_file, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        col_names = next(reader)
        for row in tqdm(reader):
            data = dict(zip(col_names, row))
            merge_meanings(data)
            split_examples(data)
            insert_inflection(data, inflection_data)
            pprint(data)

            check_page_name(data['lexeme_id'])

            out_file = out_dir.joinpath(
                f"{data['lexeme_id'].replace(', ', '-')}.html"
            )
            generate_html(
                data=data,
                template=template,
                out_file=out_file,
                complex_pos=complex_pos,
                glossing_labels=glossing_labels
            )

if __name__ == '__main__':
    main()
