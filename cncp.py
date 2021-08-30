import argparse
import csv
import os
import shutil

from jinja2 import Environment, FileSystemLoader


def copy_file(dir_in, dir_out):
    shutil.copytree(dir_in, dir_out, dirs_exist_ok=True)


def index(dir_out, tmpl):
    dir_in = os.path.join('data', 'news')
    items = []
    for fname in sorted(os.listdir(dir_in), reverse=True):
        with open(os.path.join(dir_in, fname)) as file:
            items.append(file.read())
    os.makedirs(dir_out, exist_ok=True)
    with open(os.path.join(dir_out, 'index.html'), 'w') as file:
        file.write(tmpl.render(items=items))


def speaker(dir_out, tmpl):
    items = {}
    with open(os.path.join('data', 'speaker2021.csv')) as file:
        reader = csv.DictReader(file)
        for row in reader:
            items[row['id']] = row
    for k, v in items.items():
        with open(os.path.join('data', 'talk', '2021', f'{k}.html')) as file:
            v['talk'] = file.read()
    os.makedirs(os.path.join(dir_out, 'speaker'), exist_ok=True)
    with open(os.path.join(dir_out, 'speaker', 'index.html'), 'w') as file:
        file.write(tmpl.render(items=items))


def schedule(dir_out, tmpl):
    items = {}
    with open(os.path.join('data', 'speaker2021.csv')) as file:
        reader = csv.DictReader(file)
        for row in reader:
            items[row['id']] = f'''
        <td class="title"><a href="/speaker#{row['id']}">{row['title']}</a></td>
        <td class="name">{row['name']}</td>
        <td class="affiliation">{row['affiliation']}</td>
'''
    os.makedirs(os.path.join(dir_out, 'schedule'), exist_ok=True)
    with open(os.path.join(dir_out, 'schedule', 'index.html'), 'w') as file:
        file.write(tmpl.render(items=items))


def main():
    parser = argparse.ArgumentParser(description='CNCP Website Generator')
    parser.add_argument('dst', type=str, metavar='dst')
    args = parser.parse_args()

    dir_out = args.dst
    copy_file('file', dir_out)

    loader = FileSystemLoader('tmpl')
    env = Environment(loader=loader)
    index(dir_out, env.get_template('index.html'))
    speaker(dir_out, env.get_template('speaker.html'))
    schedule(dir_out, env.get_template('schedule.html'))
    for page in ['about', 'register', 'analysis', 'cxms/register']:
        os.makedirs(os.path.join(dir_out, page), exist_ok=True)
        with open(os.path.join(dir_out, page, 'index.html'), 'w') as file:
            file.write(env.get_template(f'{page}.html').render())


if __name__ == '__main__':
    main()
