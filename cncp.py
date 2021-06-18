import argparse
import csv
import os
import shutil

from jinja2 import Environment, FileSystemLoader


def copy_file(dir_in, dir_out):
    shutil.copytree(dir_in, dir_out, dirs_exist_ok=True)


def index(dir_in, dir_out, tmpl):
    dir_in = os.path.join(dir_in, 'news')
    items = []
    for fname in sorted(os.listdir(dir_in), reverse=True):
        with open(os.path.join(dir_in, fname)) as file:
            items.append(file.read())
    os.makedirs(dir_out, exist_ok=True)
    with open(os.path.join(dir_out, 'index.html'), 'w') as file:
        file.write(tmpl.render(items=items))


def speaker(dir_in, dir_out, tmpl):
    items = {}
    with open(os.path.join(dir_in, 'speaker2021.csv')) as file:
        reader = csv.DictReader(file)
        for row in reader:
            items[row['id']] = row
    for k, v in items.items():
        with open(os.path.join(dir_in, 'talk', '2021', f'{k}.html')) as file:
            v['talk'] = file.read()
    os.makedirs(dir_out, exist_ok=True)
    with open(os.path.join(dir_out, 'speaker', 'index.html'), 'w') as file:
        file.write(tmpl.render(items=items))


def main():
    parser = argparse.ArgumentParser(description='CNCP Website Generator')
    parser.add_argument('src', type=str, metavar='src')
    parser.add_argument('dst', type=str, metavar='dst')
    args = parser.parse_args()

    dir_out = args.dst
    copy_file(os.path.join(args.src, 'file'), dir_out)

    loader = FileSystemLoader(os.path.join(args.src, 'tmpl'))
    env = Environment(loader=loader)
    dir_in = os.path.join(args.src, 'data')
    index(dir_in, dir_out, env.get_template('index.html'))
    speaker(dir_in, dir_out, env.get_template('speaker.html'))


if __name__ == '__main__':
    main()
