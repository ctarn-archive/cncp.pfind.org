import argparse
import os
import shutil

from jinja2 import Environment, FileSystemLoader


def copy_file(dir_in, dir_out):
    shutil.rmtree(dir_out, ignore_errors=True)
    shutil.copytree(dir_in, dir_out)


def index(dir_in, dir_out, tmpl):
    items = []
    for fname in sorted(os.listdir(dir_in), reverse=True):
        with open(os.path.join(dir_in, fname)) as file:
            items.append(file.read())
    with open(os.path.join(dir_out, 'index.html'), 'w') as file:
        file.write(tmpl.render(items=items))


def main():
    parser = argparse.ArgumentParser(description='CNCP Website Generator')
    parser.add_argument('src', type=str, metavar='src')
    parser.add_argument('dst', type=str, metavar='dst')
    args = parser.parse_args()

    copy_file(os.path.join(args.src, 'file'), args.dst)

    loader = FileSystemLoader(os.path.join(args.src, 'tmpl'))
    env = Environment(loader=loader)
    index(os.path.join(args.src, 'data', 'news'), args.dst, env.get_template('index.html'))


if __name__ == '__main__':
    main()
