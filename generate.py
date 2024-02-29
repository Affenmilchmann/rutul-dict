from jinja2 import (Environment, 
                    FileSystemLoader, 
                    Template)
from pathlib import Path
from tqdm import tqdm
import csv

def generate_html(data: dict, 
                  template: Template, 
                  out_file: Path) -> None:
    """generates a single html file and saves it at `out_file`

    Args:
        data (dict): data to give to the template
        template (Template): jinja2 template
        out_file (Path): out file name
    """
    with open(out_file, 'w') as f:
        f.write(template.render(data=data))

def main():
    template_file = 'word.html'
    data_file = 'data/RUTUL-all.csv'
    out_dir = 'words'

    root = Path(__file__).parent.absolute()
    templates_dir = root.joinpath('templates')
    out_dir = root.joinpath(out_dir)
    if not out_dir.is_dir(): out_dir.mkdir()
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template(template_file)

    with open(data_file) as f:
        reader = csv.reader(f)
        coll_names = next(reader)
        for row in tqdm(reader):
            data = {k:v for k, v in zip(coll_names, row)}
            generate_html(
                data=data,
                template=template,
                out_file=out_dir.joinpath(f"{data['lexeme_id']}.html")
            )

if __name__ == '__main__':
    main()