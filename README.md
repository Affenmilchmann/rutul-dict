# Генератор статичного html словаря Рутульского языка

Код состоит из:
- двух скриптов R Quarto=: [index.qmd](index.qmd) и [dictionary.qmd](dictionary.qmd)  
Они генерируют
    - главную страницу (/index.html)
    - страницу словаря со списком слов (/dictionary.html)
- Python скрипт: [generate.py](generate.py)  
Генерирует все индивидуальные страницы слов (/words/*)

И скрипты R и скирпт Python читают данные из [data/rutul_dict.tsv](data/rutul_dict.tsv). И словоизменительные данные из [data/infl_adj.tsv](data/infl_adj.tsv), [data/infl_noun.tsv](data/infl_noun.tsv) и [data/infl_verb.tsv](data/infl_verb.tsv)

## Как редактировать словарь и статический сайт
1. Внесите необходимые изменения в исходные файлы data/*.tsv.
2. Сгенерируйте статичный сайт
    - R:
        1. Откройте RStudio
        2. Установите Quarto и зависимости для [dictionary.qmd](dictionary.qmd)
        3. Запустите генерацию [index.qmd](index.qmd) и [dictionary.qmd](dictionary.qmd)
    - python:
        1. (опционально) создайне виртуальное окружение
        2. Установите зависимости:   
        `pip install -r requirements.txt`  
        или  
        `pip3 install -r requirements.txt`
        3. Запустите скрипт:  
        `python3 generate.py`  

Авторы: Ася Алексеева, Иван Осоргин

- Ася Алексеева: создание и обработка *.tsv таблиц словаря
- Иван Осоргин: скрипты генерации R и Python