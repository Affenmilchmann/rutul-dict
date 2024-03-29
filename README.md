# Rutul dictionary static website generator

This code consists of:
- two R Quarto scripts: [index.qmd](index.qmd) and [dictionary.qmd](dictionary.qmd)  
They generate
    - a frontpage (/index.html)
    - a dictionary page (/dictionary.html)
- Python script: [generate.py](generate.py)  
It generates all individual word pages (/words/*)

Both R and Python scripts take word data from [data/rutul_dict.tsv](data/rutul_dict.tsv). And inflectional data from [infl_adj.tsv](data/infl_adj.tsv), [data/infl_noun.tsv](data/infl_noun.tsv) and [infl_verb.tsv](data/infl_verb.tsv)

## How to edit the dictionary
1. Edit data you need in data/*.tsv files.
2. Generate website
    - R:
        1. Open RStudio
        2. Install Quarto and dependencies
        3. Run generation on both [index.qmd](index.qmd) and [dictionary.qmd](dictionary.qmd) individually
    - python:
        1. (optional) activate virtual enviroment
        2. Install dependencies:   
        `pip install -r requirements.txt`  
        or  
        `pip3 install -r requirements.txt`
        3. Run generation script:  
        `python3 generate.py`  

Authors: Ася Алексеева, Иван Осоргин

- Ася Алексеева: *.tsv data
- Иван Осоргин: R and Python scripts